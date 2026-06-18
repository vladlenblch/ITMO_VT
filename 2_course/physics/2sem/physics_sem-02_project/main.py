"""PyVista + PyVistaQt + PySide6 app that renders a city block from OSM.

Run:
    python main.py
"""

from __future__ import annotations

import os
import sys
import traceback
from pathlib import Path

from city.osm_parser import UAV_ACTIVE_SECONDS

PROJECT_ROOT = Path(__file__).parent
os.environ.setdefault("XDG_CACHE_HOME", str(PROJECT_ROOT / ".cache"))
os.environ.setdefault("MPLCONFIGDIR", str(PROJECT_ROOT / ".cache" / "matplotlib"))

IMPORT_ERROR: ModuleNotFoundError | None = None

try:
    import pyvista as pv
    from PySide6.QtCore import QObject, QRunnable, Qt, QThreadPool, QTimer, Signal
    from PySide6.QtWidgets import (
        QApplication,
        QButtonGroup,
        QCheckBox,
        QDoubleSpinBox,
        QFrame,
        QHBoxLayout,
        QLabel,
        QMainWindow,
        QPushButton,
        QRadioButton,
        QSlider,
        QSpinBox,
        QVBoxLayout,
        QWidget,
    )
    from pyvistaqt import QtInteractor
except ModuleNotFoundError as exc:
    IMPORT_ERROR = exc
    QObject = object  # type: ignore[assignment,misc]
    QRunnable = object  # type: ignore[assignment,misc]
    QMainWindow = object  # type: ignore[assignment,misc]
    QThreadPool = object  # type: ignore[assignment,misc]

    def Signal(*_: object, **__: object) -> object:  # type: ignore[misc]
        return object()


OSM_PATH = PROJECT_ROOT / "districts" / "willis_mega.osm"
SLIDER_MAX = 1000
TOWER_UPDATE_DELAY_MS = 16
FERRY_UPDATE_INTERVAL_MS = 200
FERRY_PROGRESS_STEP = 0.01 / 3.0
UAV_UPDATE_INTERVAL_MS = 200
WAVE_UPDATE_INTERVAL_MS = 200
WAVE_PROGRESS_STEP_M = 8.0
TOWER_ACTOR_PREFIXES = ("tower_enabled", "tower_disabled")
FERRY_ACTOR_PREFIXES = ("ferry_body", "ferry_edges")
UAV_ACTOR_PREFIXES = ("uav_body", "uav_edges")
WAVE_ACTOR_PREFIXES = ("tower_waves",)
RADIO_RAYS_ACTOR = "radio_rays"
COVERAGE_SLICE_ACTOR = "coverage_slice"
VISUAL_MODE_WAVES = "waves"
VISUAL_MODE_RAYS = "rays"
VISUAL_MODE_COVERAGE = "coverage"


class CoverageComputeSignals(QObject):  # type: ignore[misc]
    finished = Signal(int, object, object)
    failed = Signal(int, str)


class CoverageComputeTask(QRunnable):  # type: ignore[misc]
    """Background coverage calculation detached from the GUI thread."""

    def __init__(self, request_id: int, data_snapshot: object) -> None:
        super().__init__()
        self.request_id = request_id
        self.data_snapshot = data_snapshot
        self.signals = CoverageComputeSignals()
        self.setAutoDelete(True)

    def run(self) -> None:
        try:
            from city.builder import compute_coverage_result

            signature, coverage_result = compute_coverage_result(self.data_snapshot)
        except Exception:
            self.signals.failed.emit(self.request_id, traceback.format_exc())
            return

        self.signals.finished.emit(self.request_id, signature, coverage_result)


class MainWindow(QMainWindow):  # type: ignore[misc]
    """Main window that renders the city scene from an OSM file."""

    def __init__(self, osm_path: Path) -> None:
        super().__init__()
        self.setWindowTitle("City 3D — OSM preview")
        self.resize(1200, 760)
        self._scene_ready = False
        self._pending_tower_position: float | None = None
        self._tower_update_timer = QTimer(self)
        self._tower_update_timer.setSingleShot(True)
        self._tower_update_timer.timeout.connect(self._apply_pending_tower_position)
        self._ferry_timer = QTimer(self)
        self._ferry_timer.timeout.connect(self._advance_ferry)
        self._uav_timer = QTimer(self)
        self._uav_timer.timeout.connect(self._advance_uav)
        self._wave_timer = QTimer(self)
        self._wave_timer.timeout.connect(self._advance_waves)
        self._coverage_thread_pool = QThreadPool.globalInstance()
        self._coverage_request_id = 0
        self._coverage_job_running = False
        self._coverage_pending = False

        root = QWidget()
        self.setCentralWidget(root)
        root_layout = QHBoxLayout(root)

        self.plotter = QtInteractor(self)
        root_layout.addWidget(self.plotter.interactor)
        self.tower_slider = QSlider(Qt.Orientation.Horizontal)
        self.tower_1_checkbox = QCheckBox("Вышка 1")
        self.tower_2_checkbox = QCheckBox("Вышка 2")
        self.ferry_checkbox = QCheckBox("Паром")
        self.visual_mode_group = QButtonGroup(self)
        self.waves_radio = QRadioButton("Динамические волны")
        self.rays_radio = QRadioButton("Лучи")
        self.coverage_radio = QRadioButton("Карта покрытия")
        self.ray_count_spin = QSpinBox()
        self.bounce_spin = QSpinBox()
        self.slice_height_spin = QDoubleSpinBox()
        self.launch_uav_button = QPushButton("Запустить БПЛА")
        self.recompute_button = QPushButton("Пересчитать")
        self._init_controls(root_layout)

        self._init_scene(osm_path)
        self._scene_ready = True
        self._sync_radio_settings_from_ui()
        if self.ferry_checkbox.isChecked():
            self._ferry_timer.start(FERRY_UPDATE_INTERVAL_MS)
        self._refresh_visual_mode()

    def _init_controls(self, root_layout: QHBoxLayout) -> None:
        controls = QWidget()
        controls.setFixedWidth(230)
        controls_layout = QVBoxLayout(controls)

        title = QLabel("Положение вышек")
        controls_layout.addWidget(title)

        self.tower_slider.setRange(0, SLIDER_MAX)
        self.tower_slider.setValue(0)
        self.tower_slider.valueChanged.connect(self._on_tower_slider_changed)
        controls_layout.addWidget(self.tower_slider)

        self.tower_1_checkbox.setChecked(True)
        self.tower_2_checkbox.setChecked(True)
        self.tower_1_checkbox.stateChanged.connect(self._on_tower_enabled_changed)
        self.tower_2_checkbox.stateChanged.connect(self._on_tower_enabled_changed)
        controls_layout.addWidget(self.tower_1_checkbox)
        controls_layout.addWidget(self.tower_2_checkbox)

        self.ferry_checkbox.setChecked(True)
        self.ferry_checkbox.stateChanged.connect(self._on_ferry_enabled_changed)
        controls_layout.addWidget(self.ferry_checkbox)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        controls_layout.addWidget(separator)
        controls_layout.addWidget(QLabel("Радио"))

        self.ray_count_spin.setRange(50, 50000)
        self.ray_count_spin.setSingleStep(100)
        self.ray_count_spin.setValue(self.data.ray_count if hasattr(self, "data") else 1500)
        self.ray_count_spin.setPrefix("Лучей: ")
        controls_layout.addWidget(self.ray_count_spin)

        self.bounce_spin.setRange(0, 6)
        self.bounce_spin.setValue(self.data.ray_max_bounces if hasattr(self, "data") else 2)
        self.bounce_spin.setPrefix("Отражений: ")
        controls_layout.addWidget(self.bounce_spin)

        self.slice_height_spin.setRange(0.0, 400.0)
        self.slice_height_spin.setDecimals(1)
        self.slice_height_spin.setSingleStep(1.0)
        self.slice_height_spin.setValue(
            self.data.coverage_slice_z_m if hasattr(self, "data") else 0.0
        )
        self.slice_height_spin.setSuffix(" м (срез)")
        controls_layout.addWidget(self.slice_height_spin)

        self.visual_mode_group.setExclusive(True)
        for button in (self.waves_radio, self.rays_radio, self.coverage_radio):
            self.visual_mode_group.addButton(button)
            button.toggled.connect(self._on_visual_mode_toggled)
            controls_layout.addWidget(button)
        self.waves_radio.setChecked(True)

        self.launch_uav_button.clicked.connect(self._on_launch_uav_clicked)
        controls_layout.addWidget(self.launch_uav_button)

        self.recompute_button.clicked.connect(self._on_recompute_clicked)
        controls_layout.addWidget(self.recompute_button)

        self.ray_count_spin.valueChanged.connect(self._on_radio_quality_changed)
        self.bounce_spin.valueChanged.connect(self._on_radio_quality_changed)
        self.slice_height_spin.valueChanged.connect(self._on_slice_height_changed)

        controls_layout.addStretch(1)
        root_layout.addWidget(controls)

    def _init_scene(self, osm_path: Path) -> None:
        self.plotter.set_background("#1e1e1e")
        self.plotter.add_axes()
        self.plotter.show_grid(color="gray")
        self.plotter.enable_terrain_style(mouse_wheel_zooms=True)
        self.plotter.camera.up = (0.0, 0.0, 1.0)

        from city import add_city_to_plotter, build_city_scene

        self.data, meshes = build_city_scene(osm_path)
        add_city_to_plotter(self.plotter, meshes)

        self.plotter.reset_camera()
        self.plotter.camera_position = "iso"
        self.plotter.render()

    def _on_tower_slider_changed(self, _: int) -> None:
        if not self._scene_ready:
            return

        self._pending_tower_position = self.tower_slider.value() / SLIDER_MAX
        if not self._tower_update_timer.isActive():
            self._tower_update_timer.start(TOWER_UPDATE_DELAY_MS)

    def _on_tower_enabled_changed(self, _: int) -> None:
        if not self._scene_ready:
            return

        from city.scene import set_perimeter_tower_enabled

        previous_states = {
            1: self._is_perimeter_tower_enabled(1),
            2: self._is_perimeter_tower_enabled(2),
        }
        next_states = {
            1: self.tower_1_checkbox.isChecked(),
            2: self.tower_2_checkbox.isChecked(),
        }
        set_perimeter_tower_enabled(self.data, 1, self.tower_1_checkbox.isChecked())
        set_perimeter_tower_enabled(self.data, 2, self.tower_2_checkbox.isChecked())
        for tower_index, is_enabled in next_states.items():
            if previous_states[tower_index] != is_enabled:
                self.data.tower_wave_phases_m[str(tower_index)] = 0.0
        self._invalidate_radio_cache()
        self._refresh_towers()
        self._refresh_visual_mode(force_compute=True)

    def _apply_pending_tower_position(self) -> None:
        if self._pending_tower_position is None:
            return

        from city.scene import set_perimeter_towers

        position = self._pending_tower_position
        self._pending_tower_position = None
        set_perimeter_towers(self.data, position)
        self.data.wave_phase_m = 0.0
        self.data.tower_wave_phases_m.clear()
        self._invalidate_radio_cache()
        self._refresh_towers()
        self._refresh_visual_mode(force_compute=True)

        if self._pending_tower_position is not None:
            self._tower_update_timer.start(TOWER_UPDATE_DELAY_MS)

    def _refresh_towers(self) -> None:
        from city import add_city_to_plotter
        from city.builder import build_tower_meshes

        for actor_name in list(self.plotter.actors):
            if actor_name.startswith(TOWER_ACTOR_PREFIXES):
                self.plotter.remove_actor(actor_name, render=False)

        add_city_to_plotter(self.plotter, build_tower_meshes(self.data.towers))
        self.plotter.render()

    def _active_visual_mode(self) -> str:
        if self.coverage_radio.isChecked():
            return VISUAL_MODE_COVERAGE
        if self.rays_radio.isChecked():
            return VISUAL_MODE_RAYS
        return VISUAL_MODE_WAVES

    def _on_visual_mode_toggled(self, checked: bool) -> None:
        if not checked or not self._scene_ready:
            return
        self._sync_radio_settings_from_ui()
        self._refresh_visual_mode()

    def _refresh_visual_mode(self, force_compute: bool = False) -> None:
        mode = self._active_visual_mode()
        self._remove_radio_actors()
        if mode != VISUAL_MODE_WAVES:
            self._wave_timer.stop()
            self._remove_wave_actors()

        if mode == VISUAL_MODE_WAVES:
            if not self._wave_timer.isActive():
                self._wave_timer.start(WAVE_UPDATE_INTERVAL_MS)
            self._refresh_waves()
            return

        if mode == VISUAL_MODE_RAYS:
            self._refresh_rays(force_compute=force_compute)
            return

        self._refresh_coverage(force_compute=force_compute)

    def _advance_waves(self) -> None:
        if not self._scene_ready or self._active_visual_mode() != VISUAL_MODE_WAVES:
            return

        for tower in self.data.towers:
            tower_key = self._perimeter_tower_key(tower)
            if tower.enabled and tower_key is not None:
                self.data.tower_wave_phases_m[tower_key] = (
                    self.data.tower_wave_phases_m.get(tower_key, 0.0)
                    + WAVE_PROGRESS_STEP_M
                )
        self._refresh_waves()

    def _refresh_waves(self) -> None:
        from city import add_city_to_plotter
        from city.builder import build_wave_meshes

        self._remove_wave_actors()

        add_city_to_plotter(self.plotter, build_wave_meshes(self.data))
        self.plotter.render()

    def _remove_wave_actors(self) -> None:
        for actor_name in list(self.plotter.actors):
            if actor_name.startswith(WAVE_ACTOR_PREFIXES):
                self.plotter.remove_actor(actor_name, render=False)

    def _remove_radio_actors(self) -> None:
        for actor_name in (RADIO_RAYS_ACTOR, COVERAGE_SLICE_ACTOR):
            if actor_name in self.plotter.actors:
                self.plotter.remove_actor(actor_name, render=False)

    def _on_ferry_enabled_changed(self, _: int) -> None:
        if not self._scene_ready:
            return

        if self.ferry_checkbox.isChecked():
            self.data.ferry_enabled = True
            self._ferry_timer.start(FERRY_UPDATE_INTERVAL_MS)
            self._refresh_ferry()
        else:
            self.data.ferry_enabled = False
            self._ferry_timer.stop()
            self._remove_ferry_actors()
            self.plotter.render()
        self._invalidate_radio_cache()
        self._refresh_visual_mode(force_compute=True)

    def _advance_ferry(self) -> None:
        if not self._scene_ready or not self.ferry_checkbox.isChecked():
            return

        self.data.ferry_progress = (self.data.ferry_progress + FERRY_PROGRESS_STEP) % 1.0
        self._refresh_ferry()
        if self._active_visual_mode() == VISUAL_MODE_COVERAGE:
            self._refresh_coverage()

    def _refresh_ferry(self) -> None:
        from city import add_city_to_plotter
        from city.builder import build_ferry_meshes

        for actor_name in list(self.plotter.actors):
            if actor_name.startswith(FERRY_ACTOR_PREFIXES):
                self.plotter.remove_actor(actor_name, render=False)

        add_city_to_plotter(self.plotter, build_ferry_meshes(self.data))
        self.plotter.render()

    def _remove_ferry_actors(self) -> None:
        for actor_name in list(self.plotter.actors):
            if actor_name.startswith(FERRY_ACTOR_PREFIXES):
                self.plotter.remove_actor(actor_name, render=False)

    def _advance_uav(self) -> None:
        if not self._scene_ready:
            return

        step_s = UAV_UPDATE_INTERVAL_MS / 1000.0
        was_active = self.data.uav_active
        self.data.uav_flight_time_s += step_s
        self.data.uav_active = self.data.uav_flight_time_s < UAV_ACTIVE_SECONDS
        self.data.uav_progress = (
            self.data.uav_flight_time_s / UAV_ACTIVE_SECONDS
            if self.data.uav_active
            else 1.0
        )
        if not self.data.uav_active:
            self._uav_timer.stop()

        if self.data.uav_active or was_active:
            self._refresh_uav()
        if (
            self._active_visual_mode() == VISUAL_MODE_COVERAGE
            and (self.data.uav_active or was_active)
        ):
            self._refresh_coverage()

    def _refresh_uav(self) -> None:
        from city import add_city_to_plotter
        from city.builder import build_uav_meshes

        for actor_name in list(self.plotter.actors):
            if actor_name.startswith(UAV_ACTOR_PREFIXES):
                self.plotter.remove_actor(actor_name, render=False)

        add_city_to_plotter(self.plotter, build_uav_meshes(self.data))
        self.plotter.render()

    def _on_launch_uav_clicked(self) -> None:
        if not self._scene_ready or not self.data.uav_enabled:
            return

        self.data.uav_active = True
        self.data.uav_progress = 0.0
        self.data.uav_flight_time_s = 0.0
        self._refresh_uav()
        if self._active_visual_mode() == VISUAL_MODE_COVERAGE:
            self._refresh_coverage()
        if not self._uav_timer.isActive():
            self._uav_timer.start(UAV_UPDATE_INTERVAL_MS)

    def _sync_radio_settings_from_ui(self) -> None:
        self.data.ray_count = int(self.ray_count_spin.value())
        self.data.ray_max_bounces = int(self.bounce_spin.value())
        self.data.coverage_slice_z_m = float(self.slice_height_spin.value())

    def _invalidate_radio_cache(self) -> None:
        from city.radio import invalidate_coverage

        invalidate_coverage(self.data)

    def _refresh_rays(self, force_compute: bool = False) -> None:
        from city.scene import add_radio_rays

        if force_compute:
            self._invalidate_radio_cache()
        if COVERAGE_SLICE_ACTOR in self.plotter.actors:
            self.plotter.remove_actor(COVERAGE_SLICE_ACTOR, render=False)
        add_radio_rays(self.plotter, self.data)
        self.plotter.render()

    def _refresh_coverage(self, force_compute: bool = False) -> None:
        from city.radio import (
            activate_cached_coverage,
            coverage_is_cached,
            coverage_signature,
            load_persistent_coverage,
        )

        if force_compute:
            self._invalidate_radio_cache()

        signature = coverage_signature(self.data)
        if coverage_is_cached(self.data, signature):
            activate_cached_coverage(self.data, signature)
            self._draw_cached_coverage()
            return
        if load_persistent_coverage(self.data, signature):
            self._draw_cached_coverage()
            return

        if isinstance(self.data.coverage_grid, tuple):
            self._draw_coverage_result(self.data.coverage_grid)
        self._start_coverage_compute()

    def _draw_cached_coverage(self) -> None:
        from city.scene import add_coverage_slice

        if RADIO_RAYS_ACTOR in self.plotter.actors:
            self.plotter.remove_actor(RADIO_RAYS_ACTOR, render=False)
        add_coverage_slice(self.plotter, self.data)
        self.plotter.render()

    def _draw_coverage_result(self, coverage_result: object) -> None:
        from city.scene import add_coverage_result_slice

        if RADIO_RAYS_ACTOR in self.plotter.actors:
            self.plotter.remove_actor(RADIO_RAYS_ACTOR, render=False)
        add_coverage_result_slice(
            self.plotter,
            coverage_result,
            self.data.coverage_slice_z_m,
        )
        self.plotter.render()

    def _start_coverage_compute(self) -> None:
        if self._coverage_job_running:
            self._coverage_pending = True
            return

        self._coverage_job_running = True
        self._coverage_pending = False
        self._coverage_request_id += 1
        task = CoverageComputeTask(
            self._coverage_request_id,
            self._radio_data_snapshot(),
        )
        task.signals.finished.connect(self._on_coverage_computed)
        task.signals.failed.connect(self._on_coverage_failed)
        self._coverage_thread_pool.start(task)

    def _on_coverage_computed(
        self,
        request_id: int,
        signature: object,
        coverage_result: object,
    ) -> None:
        from city.radio import coverage_signature, store_coverage_result

        if request_id != self._coverage_request_id:
            self._coverage_job_running = False
            if self._coverage_pending and self._active_visual_mode() == VISUAL_MODE_COVERAGE:
                self._refresh_coverage()
            return

        self._coverage_job_running = False
        if not isinstance(signature, tuple):
            return

        store_coverage_result(self.data, signature, coverage_result)
        is_current = signature == coverage_signature(self.data)
        if self._active_visual_mode() == VISUAL_MODE_COVERAGE:
            if is_current:
                self._draw_cached_coverage()
            else:
                self._draw_coverage_result(coverage_result)

        if self._coverage_pending and self._active_visual_mode() == VISUAL_MODE_COVERAGE:
            self._refresh_coverage()

    def _on_coverage_failed(self, request_id: int, error_text: str) -> None:
        if request_id != self._coverage_request_id:
            return

        self._coverage_job_running = False
        self._coverage_pending = False
        print("Coverage recompute failed:\n", error_text, file=sys.stderr)

    def _on_recompute_clicked(self) -> None:
        if not self._scene_ready:
            return
        self._sync_radio_settings_from_ui()
        self._invalidate_radio_cache()
        mode = self._active_visual_mode()
        if mode == VISUAL_MODE_WAVES:
            self.coverage_radio.setChecked(True)
            return
        self._refresh_visual_mode(force_compute=True)

    def _on_slice_height_changed(self, _: float) -> None:
        if not self._scene_ready:
            return
        self._sync_radio_settings_from_ui()
        if self._active_visual_mode() == VISUAL_MODE_COVERAGE:
            self._refresh_coverage()

    def _on_radio_quality_changed(self, _: object) -> None:
        if not self._scene_ready:
            return

        self._sync_radio_settings_from_ui()
        self._invalidate_radio_cache()
        if self._active_visual_mode() in {VISUAL_MODE_RAYS, VISUAL_MODE_COVERAGE}:
            self._refresh_visual_mode(force_compute=True)

    def _radio_data_snapshot(self) -> object:
        from city.osm_parser import Building, OSMData, Tower

        return OSMData(
            projection=self.data.projection,
            bounds_xy=self.data.bounds_xy,
            view_bounds_xy=self.data.view_bounds_xy,
            buildings=[
                Building(
                    footprint=list(building.footprint),
                    height_m=building.height_m,
                    kind=building.kind,
                )
                for building in self.data.buildings
            ],
            towers=[
                Tower(
                    footprint=list(tower.footprint),
                    height_m=tower.height_m,
                    name=tower.name,
                    kind=tower.kind,
                    tower_type=tower.tower_type,
                    construction=tower.construction,
                    operator=tower.operator,
                    enabled=tower.enabled,
                )
                for tower in self.data.towers
            ],
            contour_xy=list(self.data.contour_xy),
            boundary_xy=list(self.data.boundary_xy),
            ferry_path_x=self.data.ferry_path_x,
            ferry_path_y_bounds=self.data.ferry_path_y_bounds,
            ferry_clip_y_bounds=self.data.ferry_clip_y_bounds,
            ferry_enabled=self.data.ferry_enabled,
            ferry_progress=self.data.ferry_progress,
            uav_enabled=self.data.uav_enabled,
            uav_active=self.data.uav_active,
            uav_progress=self.data.uav_progress,
            uav_flight_time_s=self.data.uav_flight_time_s,
            wave_phase_m=self.data.wave_phase_m,
            tower_wave_phases_m=dict(self.data.tower_wave_phases_m),
            ray_count=self.data.ray_count,
            ray_max_bounces=self.data.ray_max_bounces,
            voxel_size_m=self.data.voxel_size_m,
            coverage_slice_z_m=self.data.coverage_slice_z_m,
        )

    def _is_perimeter_tower_enabled(self, tower_index: int) -> bool:
        tower_name = f"perimeter_tower_{tower_index}"
        for tower in self.data.towers:
            if tower.name == tower_name:
                return tower.enabled
        return False

    @staticmethod
    def _perimeter_tower_key(tower: object) -> str | None:
        tower_name = getattr(tower, "name", None) or ""
        if not tower_name.startswith("perimeter_tower_"):
            return None
        tower_key = tower_name.removeprefix("perimeter_tower_")
        return tower_key or None

def main() -> None:
    if IMPORT_ERROR is not None:
        missing = IMPORT_ERROR.name or "unknown package"
        print(
            "Missing dependency:",
            missing,
            "\nInstall required packages:\n"
            "    python -m pip install -r requirements.txt",
        )
        sys.exit(1)

    if not OSM_PATH.exists():
        print(f"OSM file not found: {OSM_PATH}")
        sys.exit(1)

    pv.global_theme.window_size = [1200, 760]
    app = QApplication(sys.argv)
    window = MainWindow(OSM_PATH)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger
import asyncio
import numpy as np
from .models import Missile, Target, find_perfect_trajectory, NEW_YORK_LATITUDE

_LAUNCH_VECTOR_CACHE = {}
_CALCULATION_RESULTS = {}
_WIND_ARROW_SCALE = 400.0
_WIND_ARROW_BASE = np.array([-400.0, -400.0, 0.0], dtype=float)


def _make_cache_key(missile_template, target_config, wind_vec):
    m = missile_template
    key = (
        round(wind_vec[0], 3), round(wind_vec[1], 3), round(wind_vec[2], 3),
        round(target_config['x'], 3), round(target_config['y'], 3), round(target_config['z'], 3),
        round(target_config['vx'], 3), round(target_config['vy'], 3), round(target_config['vz'], 3),
        round(m.mass_empty, 3), round(m.fuel_mass, 3), round(m.thrust_force, 3),
        round(m.latitude, 1)
    )
    return key


def _build_wind_arrow(wind_vec):
    vec = np.array(wind_vec, dtype=float)
    mag = np.linalg.norm(vec)
    if mag < 1e-6:
        head = _WIND_ARROW_BASE.copy()
    else:
        direction = vec / mag
        head = _WIND_ARROW_BASE + direction * _WIND_ARROW_SCALE
    base = _WIND_ARROW_BASE
    return {
        'x': [float(base[0]), float(head[0])],
        'y': [float(base[1]), float(head[1])],
        'z': [float(base[2]), float(head[2])]
    }


def _parse_target_config(data):
    try:
        x = float(data.get('target_x', 4000))
        y = float(data.get('target_y', 6000))
        z = float(data.get('target_z', 4000))
    except (TypeError, ValueError):
        raise ValueError("неверные координаты цели")

    if x < 500 or y < 500 or z < 500:
        raise ValueError("координаты цели должны быть >= 500")

    return {
        'x': x, 'y': y, 'z': z,
        'vx': -50, 'vy': -300, 'vz': -50
    }


app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws/calculate")
async def websocket_calculate(websocket: WebSocket):
    await websocket.accept()

    try:
        data = await websocket.receive_json()

        if data.get('action') != 'calculate':
            await websocket.send_json({"error": "неверное действие"})
            await websocket.close()
            return

        try:
            start_ws = float(data.get('wind_speed'))
            start_wd = float(data.get('wind_dir'))
        except (TypeError, ValueError):
            await websocket.send_json({"error": "неверная скорость ветра или направление"})
            await websocket.close()
            return

        await websocket.send_json({"status": "calculating"})

        wx = start_ws * np.cos(np.radians(start_wd))
        wy = start_ws * np.sin(np.radians(start_wd))
        initial_wind = np.array([wx, wy, 0.0], dtype=float)
        wind_arrow = _build_wind_arrow(initial_wind)

        try:
            target_config = _parse_target_config(data)
        except ValueError:
            await websocket.send_json({"error": "неверные координаты цели"})
            await websocket.close()
            return

        missile_template = Missile(
            x=0, y=0, z=0,
            mass=60.0,
            fuel_mass=48.0,
            burn_time=12.0,
            thrust=8000.0,
            drag_coeff=0.2,
            area=0.05,
            latitude=NEW_YORK_LATITUDE
        )

        cache_key = _make_cache_key(missile_template, target_config, initial_wind.tolist())
        perfect_launch_vector = None

        if cache_key in _LAUNCH_VECTOR_CACHE:
            perfect_launch_vector = _LAUNCH_VECTOR_CACHE[cache_key]
            logger.info("используем кэшированный вектор запуска")
        else:
            params = dict(sim_time_max=22.0, az_steps=30, el_steps=15,
                          coarse_dt=0.03, refine_dt=0.015, final_dt=0.008)

            logger.info("расчет новой траектории с оптимизированными параметрами")
            perfect_launch_vector = await asyncio.to_thread(
                find_perfect_trajectory, missile_template, target_config, initial_wind, **params
            )
            try:
                _LAUNCH_VECTOR_CACHE[cache_key] = perfect_launch_vector
                logger.info("кэшируем новый вектор запуска")
            except Exception as e:
                logger.error(f"не удалось кэшировать результат: {e}")

        calculation_id = str(hash(cache_key))
        _CALCULATION_RESULTS[calculation_id] = {
            'launch_vector': perfect_launch_vector.tolist(),
            'target_config': target_config,
            'missile_template': {
                'x': 0, 'y': 0, 'z': 0,
                'mass': 60.0, 'fuel_mass': 48.0, 'burn_time': 12.0,
                'thrust': 8000.0, 'drag_coeff': 0.2, 'area': 0.05,
                'latitude': NEW_YORK_LATITUDE
            },
            'wind_arrow': wind_arrow
        }

        await websocket.send_json({
            "status": "calculated",
            "calculation_id": calculation_id,
            "trajectory_data": {
                "launch_vector": perfect_launch_vector.tolist(),
                "cache_used": cache_key in _LAUNCH_VECTOR_CACHE,
                "wind_arrow": wind_arrow
            },
            "wind_arrow": wind_arrow
        })

        await websocket.close()

    except WebSocketDisconnect:
        logger.info("клиент отключился от расчета")
    except Exception as e:
        logger.exception("ошибка в обработчике websocket расчета")
        try:
            await websocket.send_json({"error": str(e)})
        except:
            pass


@app.websocket("/ws/simulate")
async def websocket_simulate(websocket: WebSocket):
    await websocket.accept()

    try:
        data = await websocket.receive_json()

        if data.get('action') != 'simulate':
            await websocket.send_json({"error": "неверное действие"})
            await websocket.close()
            return

        trajectory_data = data.get('trajectory_data')
        if not trajectory_data or 'launch_vector' not in trajectory_data:
            await websocket.send_json({"error": "не предоставлены данные траектории"})
            await websocket.close()
            return

        try:
            start_ws = float(data.get('wind_speed'))
            start_wd = float(data.get('wind_dir'))
            launch_vector = np.array(trajectory_data['launch_vector'], dtype=float)
        except (TypeError, ValueError) as e:
            await websocket.send_json({"error": f"неверные параметры: {str(e)}"})
            await websocket.close()
            return

        wx = start_ws * np.cos(np.radians(start_wd))
        wy = start_ws * np.sin(np.radians(start_wd))
        initial_wind = np.array([wx, wy, 0.0], dtype=float)

        try:
            target_config = _parse_target_config(data)
        except ValueError:
            await websocket.send_json({"error": "неверные координаты цели"})
            await websocket.close()
            return

        missile = Missile(
            x=0, y=0, z=0,
            mass=60.0,
            fuel_mass=48.0,
            burn_time=12.0,
            thrust=8000.0,
            drag_coeff=0.2,
            area=0.05,
            latitude=NEW_YORK_LATITUDE
        )
        target = Target(**target_config)

        current_wind = initial_wind.copy()
        wind_arrow = _build_wind_arrow(current_wind)

        dt = 0.01
        max_time = 30.0
        current_time = 0.0
        collision_threshold = 5.0
        prev_dist = float('inf')
        send_interval = 0.01
        last_send_time = -send_interval
        min_dist = float('inf')
        min_m_pos = None
        min_t_pos = None
        min_time = None
        min_m_vel = None
        got_hit = False
        divergence_steps = 0
        divergence_limit = max(50, int(1.5 / dt))
        termination_reason = "simulation_finished_no_hit"

        while current_time < max_time:
            try:
                incoming = await asyncio.wait_for(websocket.receive_json(), timeout=0.005)
                if 'wind_speed' in incoming:
                    ws = float(incoming['wind_speed'])
                    wd = float(incoming['wind_dir'])
                    current_wind[0] = ws * np.cos(np.radians(wd))
                    current_wind[1] = ws * np.sin(np.radians(wd))
                    wind_arrow = _build_wind_arrow(current_wind)
            except asyncio.TimeoutError:
                pass
            except asyncio.CancelledError:
                break
            except WebSocketDisconnect:
                logger.info("клиент отключился во время получения")
                break
            except Exception as e:
                logger.exception("непредвиденная ошибка при получении websocket сообщения")
                break

            m_pos = missile.update(dt, current_wind, launch_direction=launch_vector)
            t_pos = target.update(dt)
            dist = np.linalg.norm(np.array(m_pos) - np.array(t_pos))

            if dist < min_dist:
                min_dist = dist
                min_m_pos = m_pos
                min_t_pos = t_pos
                min_time = current_time
                try:
                    min_m_vel = np.array(missile.vel, dtype=float)
                except Exception:
                    min_m_vel = None

            if dist <= collision_threshold:
                missile.pos = np.array(t_pos, dtype=float)
                try:
                    missile.vel = np.array([0.0, 0.0, 0.0], dtype=float)
                except Exception:
                    pass

                calculations_data = {
                    "missile_params": {
                        "mass_empty": missile.mass_empty,
                        "fuel_mass": missile.fuel_mass,
                        "burn_time": missile.burn_time,
                        "thrust": missile.thrust_force,
                        "drag_coeff": missile.cd,
                        "area": missile.area,
                        "latitude": missile.latitude
                    },
                    "target_params": {
                        "initial_pos": target_config,
                        "velocity": [target_config['vx'], target_config['vy'], target_config['vz']]
                    },
                    "wind_params": {
                        "initial": initial_wind.tolist(),
                        "final": current_wind.tolist(),
                        "speed": float(np.linalg.norm(current_wind)),
                        "direction_deg": float(np.degrees(np.arctan2(current_wind[1], current_wind[0]))) % 360
                    },
                    "simulation_params": {
                        "dt": dt,
                        "max_time": max_time,
                        "collision_threshold": collision_threshold,
                        "launch_vector": launch_vector.tolist()
                    },
                    "constants": {
                        "G": 9.81,
                        "RHO": 1.225,
                        "OMEGA_EARTH": 7.2921e-5
                    }
                }
                
                response = {
                    "time": f"{current_time:.2f}",
                    "missile": missile.pos.tolist(),
                    "missile_velocity": missile.vel.tolist(),
                    "missile_speed": round(float(np.linalg.norm(missile.vel)), 2),
                    "target": t_pos,
                    "distance": round(dist, 2),
                    "wind": current_wind.tolist(),
                    "hit": True,
                    "wind_arrow": wind_arrow,
                    "calculations": calculations_data
                }
                await websocket.send_json(response)
                got_hit = True
                break

            if dist > prev_dist and min_dist <= (collision_threshold * 1.2):
                collision_point = min_t_pos if min_t_pos is not None else t_pos
                missile.pos = np.array(collision_point, dtype=float)
                try:
                    missile.vel = np.array([0.0, 0.0, 0.0], dtype=float)
                except Exception:
                    pass

                calculations_data = {
                    "missile_params": {
                        "mass_empty": missile.mass_empty,
                        "fuel_mass": missile.fuel_mass,
                        "burn_time": missile.burn_time,
                        "thrust": missile.thrust_force,
                        "drag_coeff": missile.cd,
                        "area": missile.area,
                        "latitude": missile.latitude
                    },
                    "target_params": {
                        "initial_pos": target_config,
                        "velocity": [target_config['vx'], target_config['vy'], target_config['vz']]
                    },
                    "wind_params": {
                        "initial": initial_wind.tolist(),
                        "final": current_wind.tolist(),
                        "speed": float(np.linalg.norm(current_wind)),
                        "direction_deg": float(np.degrees(np.arctan2(current_wind[1], current_wind[0]))) % 360
                    },
                    "simulation_params": {
                        "dt": dt,
                        "max_time": max_time,
                        "collision_threshold": collision_threshold,
                        "launch_vector": launch_vector.tolist()
                    },
                    "constants": {
                        "G": 9.81,
                        "RHO": 1.225,
                        "OMEGA_EARTH": 7.2921e-5
                    }
                }
                
                response = {
                    "time": f"{current_time:.2f}",
                    "missile": missile.pos.tolist(),
                    "missile_velocity": missile.vel.tolist(),
                    "missile_speed": round(float(np.linalg.norm(missile.vel)), 2),
                    "target": collision_point,
                    "distance": round(min_dist, 2),
                    "wind": current_wind.tolist(),
                    "hit": True,
                    "note": "passed-through-detected",
                    "wind_arrow": wind_arrow,
                    "calculations": calculations_data
                }
                await websocket.send_json(response)
                got_hit = True
                break

            if (current_time - last_send_time) >= send_interval:
                response = {
                    "time": f"{current_time:.2f}",
                    "missile": m_pos,
                    "missile_velocity": missile.vel.tolist(),
                    "missile_speed": round(float(np.linalg.norm(missile.vel)), 2),
                    "target": t_pos,
                    "distance": round(dist, 2),
                    "wind": current_wind.tolist(),
                    "hit": False,
                    "wind_arrow": wind_arrow
                }
                await websocket.send_json(response)
                last_send_time = current_time

            if prev_dist != float('inf') and dist > prev_dist:
                divergence_steps += 1
            else:
                divergence_steps = 0

            if (divergence_steps >= divergence_limit and min_dist <= collision_threshold * 3) or \
                    (missile.pos[2] < -50.0 and current_time > missile.burn_time):
                termination_reason = "terminated_divergence"
                break

            prev_dist = dist

            current_time += dt
            await asyncio.sleep(dt)

        if not got_hit:
            try:
                calculations_data = {
                    "missile_params": {
                        "mass_empty": missile.mass_empty,
                        "fuel_mass": missile.fuel_mass,
                        "burn_time": missile.burn_time,
                        "thrust": missile.thrust_force,
                        "drag_coeff": missile.cd,
                        "area": missile.area,
                        "latitude": missile.latitude
                    },
                    "target_params": {
                        "initial_pos": target_config,
                        "velocity": [target_config['vx'], target_config['vy'], target_config['vz']]
                    },
                    "wind_params": {
                        "initial": initial_wind.tolist(),
                        "final": current_wind.tolist(),
                        "speed": float(np.linalg.norm(current_wind)),
                        "direction_deg": float(np.degrees(np.arctan2(current_wind[1], current_wind[0]))) % 360
                    },
                    "simulation_params": {
                        "dt": dt,
                        "max_time": max_time,
                        "collision_threshold": collision_threshold,
                        "launch_vector": launch_vector.tolist()
                    },
                    "constants": {
                        "G": 9.81,
                        "RHO": 1.225,
                        "OMEGA_EARTH": 7.2921e-5
                    }
                }
                
                final_summary = {
                    "time": f"{current_time:.2f}",
                    "missile": missile.pos.tolist(),
                    "missile_velocity": missile.vel.tolist(),
                    "missile_speed": round(float(np.linalg.norm(missile.vel)), 2),
                    "target": t_pos,
                    "distance": round(dist, 2),
                    "min_distance": (round(min_dist, 2) if min_dist != float('inf') else None),
                    "closest_missile": (min_m_pos if min_m_pos is not None else None),
                    "closest_target": (min_t_pos if min_t_pos is not None else None),
                    "closest_time": (f"{min_time:.2f}" if min_time is not None else None),
                    "closest_missile_speed": (
                        round(float(np.linalg.norm(min_m_vel)), 2) if min_m_vel is not None else None),
                    "wind": current_wind.tolist(),
                    "hit": False,
                    "note": termination_reason,
                    "wind_arrow": wind_arrow,
                    "calculations": calculations_data
                }
                await websocket.send_json(final_summary)
            except Exception:
                logger.exception("не удалось отправить итоговую сводку клиенту")

        await websocket.close()

    except WebSocketDisconnect:
        logger.info("клиент отключился от симуляции")
    except Exception as e:
        logger.exception("ошибка в обработчике websocket симуляции")

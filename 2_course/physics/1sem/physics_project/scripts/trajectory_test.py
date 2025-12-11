import time
import numpy as np
from app.models import Missile, Target, find_perfect_trajectory


def run_test():
    start_ws = 0.0
    start_wd = 0.0

    wx = start_ws * np.cos(np.radians(start_wd))
    wy = start_ws * np.sin(np.radians(start_wd))
    initial_wind = np.array([wx, wy, 0.0], dtype=float)

    target_config = {
        'x': 4000, 'y': 6000, 'z': 4000,
        'vx': -50, 'vy': -300, 'vz': -50
    }

    missile_template = Missile(
        x=0, y=0, z=0,
        mass=60.0,
        fuel_mass=48.0,
        burn_time=12.0,
        thrust=8000.0,
        drag_coeff=0.2,
        area=0.05
    )

    print('начать поиск траектории...')
    t0 = time.time()
    best_dir = find_perfect_trajectory(missile_template, target_config, initial_wind)
    dt_search = time.time() - t0
    print(f'find_perfect_trajectory закончен в {dt_search:.2f}s')

    sim_dt = 0.005
    sim_time = 0.0
    max_time = 30.0

    missile = missile_template.copy()
    target = Target(**target_config)

    min_dist = float('inf')
    min_state = None

    while sim_time < max_time:
        m_pos = np.array(missile.update(sim_dt, initial_wind, launch_direction=best_dir))
        t_pos = np.array(target.update(sim_dt))
        d = np.linalg.norm(m_pos - t_pos)
        if d < min_dist:
            min_dist = d
            min_state = (sim_time, m_pos.copy(), t_pos.copy())
        sim_time += sim_dt

    print(f'min_dist = {min_dist:.3f} m')
    if min_state:
        stime, mpos, tpos = min_state
        print(f'в t={stime:.3f}s ракета={mpos} цель={tpos} diff={tpos-mpos}')


if __name__ == '__main__':
    run_test()

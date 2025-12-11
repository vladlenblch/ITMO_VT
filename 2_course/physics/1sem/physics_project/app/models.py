import numpy as np
from loguru import logger

G = 9.81
RHO = 1.225
OMEGA_EARTH = 7.2921e-5
NEW_YORK_LATITUDE = 40.7


class Missile:
    def __init__(self, x, y, z, mass, fuel_mass, burn_time, thrust, drag_coeff, area, latitude=NEW_YORK_LATITUDE):
        self.pos = np.array([x, y, z], dtype=float)
        self.vel = np.array([0.0, 0.0, 0.0], dtype=float)
        self.latitude = latitude
        self.init_args = (x, y, z, mass, fuel_mass, burn_time, thrust, drag_coeff, area, latitude)

        self.mass_empty = mass
        self.fuel_mass = fuel_mass
        self.fuel_remaining = fuel_mass
        self.current_mass = mass + fuel_mass
        self.burn_time = burn_time
        self.thrust_force = thrust
        self.cd = drag_coeff
        self.area = area
        self.time_elapsed = 0.0

    def copy(self):
        return Missile(*self.init_args)

    def _calculate_coriolis_force(self, velocity):
        omega_earth = 7.2921e-5

        lat_rad = np.radians(self.latitude)

        omega_vector = np.array([
            0,
            omega_earth * np.cos(lat_rad),
            omega_earth * np.sin(lat_rad)
        ])

        coriolis_force = -2 * self.current_mass * np.cross(omega_vector, velocity)

        return coriolis_force

    def update(self, dt, wind_vector, launch_direction):
        if self.time_elapsed < self.burn_time and self.fuel_remaining > 0.0:
            dm = self.fuel_mass / self.burn_time
            consumed = dm * dt
            if consumed > self.fuel_remaining:
                consumed = self.fuel_remaining
            self.fuel_remaining -= consumed
            self.current_mass -= consumed

        if self.current_mass < self.mass_empty:
            self.current_mass = self.mass_empty


        F_thrust = np.array([0.0, 0.0, 0.0])
        if self.time_elapsed < self.burn_time and launch_direction is not None and self.fuel_remaining > 0.0:
            F_thrust = launch_direction * self.thrust_force

        F_gravity = np.array([0.0, 0.0, -self.current_mass * G])

        v_rel = self.vel - np.array(wind_vector, dtype=float)
        v_rel_mag = np.linalg.norm(v_rel)

        F_drag = np.array([0.0, 0.0, 0.0])
        if v_rel_mag > 0:
            force_mag = 0.5 * RHO * self.cd * self.area * (v_rel_mag ** 2)
            F_drag = -force_mag * (v_rel / v_rel_mag)

        F_coriolis = self._calculate_coriolis_force(self.vel)

        F_total = F_thrust + F_gravity + F_drag + F_coriolis

        def derivatives(pos, vel, fuel_rem, time_el, wind_vec):
            current_mass = self.mass_empty + max(fuel_rem, 0.0)

            F_t = np.array([0.0, 0.0, 0.0])
            if time_el < self.burn_time and fuel_rem > 0 and launch_direction is not None:
                F_t = launch_direction * self.thrust_force

            F_g = np.array([0.0, 0.0, -current_mass * G])

            v_rel_local = vel - np.array(wind_vec, dtype=float)
            v_rel_mag_local = np.linalg.norm(v_rel_local)
            F_d = np.array([0.0, 0.0, 0.0])
            if v_rel_mag_local > 0:
                force_mag_local = 0.5 * RHO * self.cd * self.area * (v_rel_mag_local ** 2)
                F_d = -force_mag_local * (v_rel_local / v_rel_mag_local)

            F_c = self._calculate_coriolis_force(vel)

            F_tot = F_t + F_g + F_d + F_c
            acc_local = F_tot / max(current_mass, 1e-6)

            fuel_rate = 0.0
            if time_el < self.burn_time and fuel_rem > 0:
                fuel_rate = -(self.fuel_mass / self.burn_time)

            return vel, acc_local, fuel_rate, 1.0

        p0 = self.pos.copy()
        v0 = self.vel.copy()
        f0 = self.fuel_remaining
        t0 = self.time_elapsed

        k1_v, k1_a, k1_f, k1_t = derivatives(p0, v0, f0, t0, wind_vector)
        p1 = p0 + (dt / 2.0) * k1_v
        v1 = v0 + (dt / 2.0) * k1_a
        f1 = f0 + (dt / 2.0) * k1_f
        t1 = t0 + (dt / 2.0) * k1_t

        k2_v, k2_a, k2_f, k2_t = derivatives(p1, v1, f1, t1, wind_vector)
        p2 = p0 + (dt / 2.0) * k2_v
        v2 = v0 + (dt / 2.0) * k2_a
        f2 = f0 + (dt / 2.0) * k2_f
        t2 = t0 + (dt / 2.0) * k2_t

        k3_v, k3_a, k3_f, k3_t = derivatives(p2, v2, f2, t2, wind_vector)
        p3 = p0 + dt * k3_v
        v3 = v0 + dt * k3_a
        f3 = f0 + dt * k3_f
        t3 = t0 + dt * k3_t

        k4_v, k4_a, k4_f, k4_t = derivatives(p3, v3, f3, t3, wind_vector)

        dp = (dt / 6.0) * (k1_v + 2.0 * k2_v + 2.0 * k3_v + k4_v)
        dv = (dt / 6.0) * (k1_a + 2.0 * k2_a + 2.0 * k3_a + k4_a)
        df = (dt / 6.0) * (k1_f + 2.0 * k2_f + 2.0 * k3_f + k4_f)
        dt_time = dt

        self.pos = self.pos + dp
        self.vel = self.vel + dv
        self.fuel_remaining = max(self.fuel_remaining + df, 0.0)
        self.current_mass = self.mass_empty + self.fuel_remaining
        self.time_elapsed += dt_time

        if self.current_mass < self.mass_empty:
            self.current_mass = self.mass_empty

        return self.pos.tolist()


class Target:
    def __init__(self, x, y, z, vx, vy, vz):
        self.pos = np.array([x, y, z], dtype=float)
        self.vel = np.array([vx, vy, vz], dtype=float)

    def update(self, dt):
        self.pos += self.vel * dt
        return self.pos.tolist()


def find_perfect_trajectory(missile_template, target_config, initial_wind,
                            sim_time_max=40.0,
                            az_steps=72, el_steps=36,
                            coarse_dt=0.01,
                            refine_dt=0.005,
                            final_dt=0.0025):
    logger.info(f"расчеты начаты. ветер: {initial_wind} | время симуляции: {sim_time_max} az_steps={az_steps} el_steps={el_steps} coarse_dt={coarse_dt} refine_dt={refine_dt} final_dt={final_dt}")
    t_pos_0 = np.array([target_config['x'], target_config['y'], target_config['z']])
    t_vel = np.array([target_config['vx'], target_config['vy'], target_config['vz']])
    def simulate_closest_distance(direction_vec, sim_dt=coarse_dt, sim_time_max_local=sim_time_max, 
                                   early_termination_threshold=5000.0):
        sim_missile = missile_template.copy()
        sim_t_pos = t_pos_0.copy()
        sim_time = 0.0
        closest = 1e9
        no_improvement_steps = 0
        max_no_improvement = 50
        
        while sim_time < sim_time_max_local:
            m_p = np.array(sim_missile.update(sim_dt, initial_wind, direction_vec))
            t_p = sim_t_pos + t_vel * sim_time
            d = np.linalg.norm(m_p - t_p)
            
            if d < closest:
                closest = d
                no_improvement_steps = 0
            else:
                no_improvement_steps += 1
            
            if closest > early_termination_threshold and no_improvement_steps > max_no_improvement:
                if sim_time > 5.0:
                    break
            
            sim_time += sim_dt
        return closest

    def dir_from_angles(az_deg, el_deg):
        az = np.radians(az_deg)
        el = np.radians(el_deg)
        x = np.cos(el) * np.cos(az)
        y = np.cos(el) * np.sin(az)
        z = np.sin(el)
        v = np.array([x, y, z], dtype=float)
        n = np.linalg.norm(v)
        return v / n if n != 0 else np.array([1.0, 0.0, 0.0])

    best_dir = None
    best_dist = 1e9

    az_range = (0, 360)
    el_range = (-20, 85)

    for az in np.linspace(az_range[0], az_range[1], az_steps, endpoint=False):
        for el in np.linspace(el_range[0], el_range[1], el_steps):
            vec = dir_from_angles(az, el)
            d = simulate_closest_distance(vec, sim_dt=coarse_dt, sim_time_max_local=sim_time_max,
                                         early_termination_threshold=best_dist * 3.0 if best_dist < 1e8 else 1e9)
            if d < best_dist:
                best_dist = d
                best_dir = vec

    if best_dir is None:
        return np.array([1.0, 0.0, 0.0])

    best_az = np.degrees(np.arctan2(best_dir[1], best_dir[0])) % 360
    best_el = np.degrees(np.arcsin(best_dir[2]))

    refine_steps = [8, 5]
    refine_span = [10.0, 2.0]
    for steps, span in zip(refine_steps, refine_span):
        az_vals = np.linspace(best_az - span, best_az + span, steps)
        el_vals = np.linspace(best_el - span, best_el + span, steps)
        for az in az_vals:
            for el in el_vals:
                vec = dir_from_angles(az, el)
                d = simulate_closest_distance(vec, sim_dt=refine_dt, sim_time_max_local=sim_time_max,
                                               early_termination_threshold=best_dist * 2.0)
                if d < best_dist:
                    best_dist = d
                    best_dir = vec
                    best_az = az
                    best_el = el

    step_sizes = [0.5, 0.2, 0.1]
    for step in step_sizes:
        improved = True
        iterations = 0
        max_iterations = 10
        while improved and iterations < max_iterations:
            improved = False
            iterations += 1
            for d_az, d_el in [(step, 0), (-step, 0), (0, step), (0, -step)]:
                cand_az = best_az + d_az
                cand_el = best_el + d_el
                vec = dir_from_angles(cand_az, cand_el)
                d = simulate_closest_distance(vec, sim_dt=final_dt, sim_time_max_local=sim_time_max,
                                               early_termination_threshold=best_dist * 1.5)
                if d + 1e-6 < best_dist:
                    best_dist = d
                    best_dir = vec
                    best_az = cand_az
                    best_el = cand_el
                    improved = True

    def nelder_mead_2d(obj_fn, x0, step0=0.5, tol=1e-3, max_iter=200, target=3.0):
        alpha = 1.0
        gamma = 2.0
        rho = 0.5
        sigma = 0.5

        simplex = [np.array(x0, dtype=float),
                   np.array([x0[0] + step0, x0[1]], dtype=float),
                   np.array([x0[0], x0[1] + step0], dtype=float)]
        fvals = [obj_fn(p) for p in simplex]
        it = 0
        while it < max_iter:
            idx = np.argsort(fvals)
            simplex = [simplex[i] for i in idx]
            fvals = [fvals[i] for i in idx]
            best = simplex[0]
            worst = simplex[-1]
            second = simplex[1]

            if np.std(fvals) < tol or fvals[0] <= target:
                break

            centroid = (simplex[0] + simplex[1]) / 2.0

            xr = centroid + alpha * (centroid - worst)
            fr = obj_fn(xr)
            if fvals[0] <= fr < fvals[1]:
                simplex[-1] = xr
                fvals[-1] = fr
            elif fr < fvals[0]:
                xe = centroid + gamma * (xr - centroid)
                fe = obj_fn(xe)
                if fe < fr:
                    simplex[-1] = xe
                    fvals[-1] = fe
                else:
                    simplex[-1] = xr
                    fvals[-1] = fr
            else:
                xc = centroid + rho * (worst - centroid)
                fc = obj_fn(xc)
                if fc < fvals[-1]:
                    simplex[-1] = xc
                    fvals[-1] = fc
                else:
                    for i in range(1, len(simplex)):
                        simplex[i] = simplex[0] + sigma * (simplex[i] - simplex[0])
                        fvals[i] = obj_fn(simplex[i])
            it += 1

        return simplex[0], fvals[0], it

    def nm_obj(x_deg):
        az, el = float(x_deg[0]), float(x_deg[1])
        vec = dir_from_angles(az, el)
        return simulate_closest_distance(vec, sim_dt=final_dt, sim_time_max_local=sim_time_max,
                                         early_termination_threshold=best_dist * 1.5)

    try:
        start = np.array([best_az, best_el], dtype=float)
        nm_start, nm_val, nm_iters = nelder_mead_2d(nm_obj, start, step0=0.5, tol=1e-2, max_iter=150, target=5.0)
        if nm_val + 1e-9 < best_dist:
            best_dist = nm_val
            best_dir = dir_from_angles(float(nm_start[0]), float(nm_start[1]))
            best_az = float(nm_start[0])
            best_el = float(nm_start[1])
        logger.info(f"nelder-mead закончен: val={nm_val:.3f} iters={nm_iters} best_dist={best_dist:.3f}")
    except Exception:
        logger.exception("nelder-mead уточнение не удалось; сохраняем предыдущий лучший")

    logger.info(f"лучшее решение найдено: Miss {best_dist:.2f}m")
    return best_dir
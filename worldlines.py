import numpy as np
from scipy.integrate import solve_ivp
from pathlib import Path

# =========================
# EDIT THESE PARAMETERS
# =========================
outdir = Path("data_pg")

# --- SET A: "planet diagrams" ---
rS = 10.0
N = 5
innermost = 2.8 * rS
maxwidth  = 9.0 * rS
rmin = 2.0 * rS
tmax = 100.0
npts = 1500

cone_times = np.linspace(10.0, 90.0, 6)
cone_dt    = 2.0
cone_file  = outdir / "cone_points.csv"
tag        = ""          # -> generates traj_1.csv ...

# --- SET B: black hole ---
rS_bh = 25.0
N_bh = 5
innermost_bh = 1.15 * rS_bh
maxwidth_bh  = 3.5 * rS_bh
rmin_bh = 0.4 * rS_bh
tmax_bh = 200.0
npts_bh = 1500

cone_times_bh = np.linspace(10.0, 90.0, 6)
cone_dt_bh    = 2.0
cone_file_bh  = outdir / "cone_points_bh.csv"
tag_bh        = "bh_"     # -> generates traj_bh_1.csv ...

# Solver settings (shared)
rtol, atol = 1e-9, 1e-12
eps = 1e-10
max_step = 0.1
# =========================


def generate_set(outdir, tag, cone_file,
                 rS, N, innermost, maxwidth, rmin, tmax, npts,
                 cone_times, cone_dt):
    """Write traj_{tag}{i}.csv and cone_file for one parameter set."""

    outdir.mkdir(parents=True, exist_ok=True)

    # Starting radii and time samples
    r0_list = np.linspace(innermost, maxwidth, N)
    t_eval  = np.linspace(0.0, tmax, npts)

    # ODE RHS
    def dr_dtF(t, y, r0):
        r = float(y[0])
        a = rS / r
        b = rS / r0
        s1 = np.sqrt(a)
        s2 = np.sqrt(max(0.0, a - b))
        c  = np.sqrt(max(0.0, 1.0 - b))
        num = -((a - b) * s1) - (c * s2)
        den = 1.0 + a - b
        return np.array([num / den])

    # Stop when r reaches rmin
    def stop_at_rmin(t, y):
        return float(y[0]) - rmin
    stop_at_rmin.terminal = True
    stop_at_rmin.direction = -1

    # Prepare cone output (overwrite each run)
    with cone_file.open("w", encoding="utf-8") as f:
        f.write("r,t,dt,inside\n")

    for i, r0 in enumerate(r0_list, start=1):

        # Solve trajectory
        def rhs(t, y): return dr_dtF(t, y, float(r0))

        sol = solve_ivp(
            fun=rhs,
            t_span=(0.0, tmax),
            y0=np.array([float(r0) * (1.0 - eps)], float),
            t_eval=t_eval,
            events=stop_at_rmin,
            rtol=rtol, atol=atol,
            max_step=max_step,
        )

        t, r = sol.t, sol.y[0]

        # Append cone points for this trajectory
        t_last = float(t[-1])
        with cone_file.open("a", encoding="utf-8") as f:
            for t0 in cone_times:
                if t0 <= t_last:
                    r_at_t0 = float(np.interp(t0, t, r))
                    inside = -1 if (r_at_t0 < rS) else 1
                    f.write(f"{r_at_t0:.12e},{t0:.12e},{cone_dt:.12e},{inside:d}\n")

        # Write trajectory CSV
        csv_path = outdir / f"traj_{tag}{i}.csv"
        with csv_path.open("w", encoding="utf-8") as f:
            f.write("t,r\n")
            for ti, ri in zip(t, r):
                f.write(f"{ti:.12e},{ri:.12e}\n")

        print(f"Wrote {csv_path}")

    print(f"Wrote {cone_file}\n")


# Run both sets back-to-back
generate_set(outdir, tag,    cone_file,
             rS, N, innermost, maxwidth, rmin, tmax, npts,
             cone_times, cone_dt)

generate_set(outdir, tag_bh, cone_file_bh,
             rS_bh, N_bh, innermost_bh, maxwidth_bh, rmin_bh, tmax_bh, npts_bh,
             cone_times_bh, cone_dt_bh)

print("Done.")

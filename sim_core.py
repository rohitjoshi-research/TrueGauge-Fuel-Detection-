"""
TrueGauge fuel-side simulation prototype (spark-ignition, port injection, closed-loop lambda control).

ALL parameters are assumed textbook values or design assumptions. Nothing here is measured vehicle data.
The simulator exists to (i) check the pipeline, (ii) expose which adulterants are observable from fuel trims at all,
and (iii) plan the empirical study. It is never a source of accuracy claims.
"""
import numpy as np

# --- approximate property table (nominal textbook values; to be replaced by measured values) -------------
RHO = dict(gasoline=0.745, ethanol=0.789, methanol=0.792, acetone=0.784, kerosene=0.800, water=1.000)   # kg/L
AFR = dict(gasoline=14.7, ethanol=9.0, methanol=6.47, acetone=9.5, kerosene=14.7, water=0.0)            # stoich. air/fuel, mass


def mixture(vol_fracs):
    """vol_fracs: dict of volume fractions summing to 1 -> (density kg/L, stoichiometric air per kg mixture)."""
    tot = sum(vol_fracs.values())
    assert abs(tot - 1.0) < 1e-9, tot
    rho = sum(f * RHO[k] for k, f in vol_fracs.items())
    w = {k: f * RHO[k] / rho for k, f in vol_fracs.items()}            # mass fractions
    afr = sum(w[k] * AFR[k] for k in w)                                  # air needed adds linearly by mass
    return rho, afr


def steady_trim(adulterant, phi, nominal="gasoline"):
    """Idealised steady-state total fuel trim (fraction) needed to hold lambda = 1 when the ECU assumes clean
    gasoline: (1 + trim) = (AFR_nom / AFR_mix) * (rho_nom / rho_mix).  Injectors deliver VOLUME, so density matters."""
    rho_n, afr_n = mixture({nominal: 1.0})
    rho_m, afr_m = mixture({nominal: 1.0 - phi, adulterant: phi})
    return (afr_n / afr_m) * (rho_n / rho_m) - 1.0


def density_temp_factor(dT, beta=0.001):
    """Relative change of fuel density for a temperature change dT (deg C); ~0.1 %/deg C for hydrocarbons."""
    return -beta * dT


# --- drive cycles ----------------------------------------------------------------------------------------
def drive_cycle(kind, n, rng):
    """Intake air mass flow (g/s) per 1-s step."""
    m = np.zeros(n)
    if kind == "highway":
        x = 14.0
        for i in range(n):
            x = 0.97 * x + 0.03 * 14.0 + rng.normal(0, 0.45)
            m[i] = max(x, 6.0)
        return m
    # urban stop-go: idle segments and acceleration/cruise bursts
    i = 0
    while i < n:
        idle = int(rng.integers(8, 30)); seg = np.full(idle, rng.uniform(2.2, 3.2))
        burst = int(rng.integers(10, 40)); lvl = rng.uniform(6.0, 24.0)
        ramp = np.linspace(seg[-1], lvl, burst) + rng.normal(0, 0.4, burst)
        for part in (seg, np.clip(ramp, 2.0, None)):
            k = min(len(part), n - i); m[i:i + k] = part[:k]; i += k
            if i >= n: break
    return m


# --- ECU + plant -----------------------------------------------------------------------------------------
def simulate(vol_fracs=None, cycle="urban", T=2700, seed=0, ltft0=0.0, maf_gain=0.0, inj_gain=0.0,
             leak_gps=0.0, warmup=90, Ks=0.4, KL=1.0 / 900.0, lam_noise=0.008, lam_tau=1.0, clip=0.25):
    """
    Returns dict of arrays (1 Hz).  Fuel is the mixture in `vol_fracs` (default clean gasoline).
    Faults: maf_gain (relative MAF gain error), inj_gain (relative injector flow error), leak_gps (unmetered air).
    ECU: injected volume = m_air_meas / (AFR_nom * rho_nom) * (1 + LTFT + STFT); STFT is a fast integrator on the
    lambda error, LTFT a slow integrator on STFT (time constant 1/KL ~ 15 min). Open loop for `warmup` seconds.
    """
    rng = np.random.default_rng(seed)
    vol_fracs = vol_fracs or {"gasoline": 1.0}
    rho_mix, afr_mix = mixture(vol_fracs)
    rho_nom, afr_nom = mixture({"gasoline": 1.0})
    m_true = drive_cycle(cycle, T, rng)
    stft = np.zeros(T); ltft = np.zeros(T); lam = np.zeros(T); lam_meas = np.zeros(T)
    S, L, lm = 0.0, ltft0, 1.0
    for t in range(T):
        m_meas = (1.0 + maf_gain) * m_true[t]                      # what the ECU believes
        V = m_meas / (afr_nom * rho_nom) * (1.0 + L + S)           # commanded volume (L per s)
        fuel_mass = rho_mix * V * (1.0 + inj_gain)
        lam_t = (m_true[t] + leak_gps) / (fuel_mass * afr_mix)    # leak air is real but unmetered
        lm += (lam_t - lm) / lam_tau + rng.normal(0, lam_noise)    # lagged, noisy lambda sensor
        if t >= warmup:                                            # closed loop
            S = float(np.clip(S + Ks * (lm - 1.0), -clip, clip))   # lean (lm>1) -> add fuel
            L = float(np.clip(L + KL * S, -clip, clip))
        else:
            S = 0.0
        stft[t], ltft[t], lam[t], lam_meas[t] = S, L, lam_t, lm
    return dict(t=np.arange(T), m_air=m_true, stft=stft, ltft=ltft, total=stft + ltft, lam=lam, lam_meas=lam_meas,
                rho=rho_mix, afr=afr_mix)


def settled_total(ltft0=0.0, **kw):
    """Total trim averaged over the last 10 min of a 45-min run."""
    r = simulate(ltft0=ltft0, **kw)
    return float(np.mean(r["total"][-600:]))


def trim_vs_airflow(r, tmin=1500, bins=(2, 4, 6, 8, 10, 13, 16, 20, 26)):
    t = r["t"] >= tmin
    m, y = r["m_air"][t], r["total"][t]
    idx = np.digitize(m, bins)
    xs, ys, es = [], [], []
    for b in range(1, len(bins)):
        sel = idx == b
        if sel.sum() >= 15:
            xs.append(m[sel].mean()); ys.append(y[sel].mean()); es.append(y[sel].std() / np.sqrt(sel.sum()))
    return np.array(xs), np.array(ys), np.array(es)

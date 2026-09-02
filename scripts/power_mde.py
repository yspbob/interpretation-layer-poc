#!/usr/bin/env python3
"""Minimum detectable effect for the primary estimand (preregistration/analysis_plan.md).

Model: ticket i has a latent violation propensity p_i ~ Beta(a, b) with mean p0 (arm A base
rate) and dispersion phi; each run has O_i opportunities ~ 1 + Poisson(lambda - 1); violations
~ Binomial(O, p). Arm C multiplies the propensity by (1 - effect). Per ticket the k runs are
pooled (sum V / sum O). The test is the sign-flip permutation test on paired differences at
alpha 0.05 (two-sided) with the success rule "CI below zero" approximated by the one-sided
rejection in the layer-favouring direction. MDE = smallest effect with power >= 0.80.

Inputs come from phase4/admissibility.json once it exists; until then run with explicit
--p0 and --lam to see the sensitivity. Deterministic (seed 20260903).

Usage: power_mde.py --p0 0.15 --lam 4 [--k 3] [--n 25] [--phi 0.3] [--sims 2000]
"""
import argparse, math, random

def simulate(n, k, p0, lam, phi, effect, sims, rnd):
    # Beta parameters from mean p0 and dispersion phi (phi in (0,1): variance = p0(1-p0)phi)
    kappa = (1 - phi) / phi
    a, b = p0 * kappa, (1 - p0) * kappa
    rejections = 0
    for _ in range(sims):
        diffs = []
        for _i in range(n):
            p = rnd.betavariate(a, b)
            pa, pc = p, p * (1 - effect)
            va = oa = vc = oc = 0
            for _r in range(k):
                o1 = 1 + _poisson(lam - 1, rnd); o2 = 1 + _poisson(lam - 1, rnd)
                va += sum(rnd.random() < pa for _ in range(o1)); oa += o1
                vc += sum(rnd.random() < pc for _ in range(o2)); oc += o2
            diffs.append(vc / oc - va / oa)
        obs = sum(diffs) / len(diffs)
        # sign-flip permutation, one-sided (layer-favouring = negative)
        cnt = 0; perms = 400
        for _p in range(perms):
            s = sum(d if rnd.random() < 0.5 else -d for d in diffs) / len(diffs)
            if s <= obs:
                cnt += 1
        if (cnt + 1) / (perms + 1) < 0.025:
            rejections += 1
    return rejections / sims

def _poisson(mu, rnd):
    if mu <= 0:
        return 0
    L = math.exp(-mu); k = 0; p = 1.0
    while True:
        p *= rnd.random()
        if p < L:
            return k
        k += 1

def mde(n, k, p0, lam, phi, sims, seed=20260903):
    rnd = random.Random(seed)
    grid = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    out = []
    for e in grid:
        pw = simulate(n, k, p0, lam, phi, e, sims, rnd)
        out.append((e, pw))
        if pw >= 0.8:
            break
    return out

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--p0", type=float, required=True, help="arm A mean violation rate per opportunity")
    ap.add_argument("--lam", type=float, required=True, help="mean opportunities per run (>=1)")
    ap.add_argument("--k", type=int, default=3); ap.add_argument("--n", type=int, default=25)
    ap.add_argument("--phi", type=float, default=0.3); ap.add_argument("--sims", type=int, default=500)
    a = ap.parse_args()
    print(f"N={a.n} k={a.k} p0={a.p0} lam={a.lam} phi={a.phi}")
    for e, pw in mde(a.n, a.k, a.p0, a.lam, a.phi, a.sims):
        print(f"  relative reduction {e:.1f} (absolute {a.p0*e:.3f}): power {pw:.2f}")

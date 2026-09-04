import math
from typing import List, Tuple, Dict

# ------------------------------------------------------------
# Constants / model parameters (from the described framework)
# ------------------------------------------------------------
LENSING_AMP = 0.05
BERRY_COEFF = 0.46
L_CENTER = 200.0
SIGMA = 50.0
U_SCALE = 1.0          # denominator in the Berry phase term


def multipole_subset(l: int) -> List[Tuple[int, int]]:
    """
    Return the cyclic subset S_l = {(l, m) | m = -l ... +l}
    """
    return [(l, m) for m in range(-l, l + 1)]


def cyclic_progression(max_l: int) -> List[List[Tuple[int, int]]]:
    """
    Generate the nested cyclic sequence:
    {S_0}, {S_0,S_1}, {S_0,S_1,S_2}, ...
    """
    progression = []
    current = []
    for l in range(max_l + 1):
        current = current + multipole_subset(l)
        progression.append(list(current))
    return progression


def berry_phase(u: float, l: int) -> float:
    """
    Geometric (Berry) phase contribution:
    φ(t) ≈ 0.46 * (u / 1) * (2l + 1) / 2500
    """
    return BERRY_COEFF * (u / U_SCALE) * (2 * l + 1) / 2500.0


def lensing_factor(z: float) -> float:
    """
    μ_lens(z) = 1 + 0.05 * z / (1 + z)
    """
    return 1.0 + LENSING_AMP * z / (1.0 + z)


def gaussian_weight(l: float) -> float:
    """
    exp( -(l - 200)^2 / (2 * 50^2) )
    """
    return math.exp(-((l - L_CENTER) ** 2) / (2.0 * SIGMA ** 2))


def evolved_Cl(Cl_base: float, z: float, u: float, l: int) -> float:
    """
    Full evolved power spectrum:
    C_l(z, u) = C_l * [μ_lens]^2 * |e^{i φ}|^2 * Gaussian

    Note: |e^{i φ}|^2 ≡ 1 for real φ, but we keep the term explicit
    for future complex extensions.
    """
    mu = lensing_factor(z)
    phase = berry_phase(u, l)
    # |exp(i * phase)|^2 is always 1.0 for real phase
    phase_mod = abs(complex(math.cos(phase), math.sin(phase))) ** 2
    gauss = gaussian_weight(float(l))
    return Cl_base * (mu ** 2) * phase_mod * gauss


def hubble_parameter(z: float, H0: float = 70.0,
                     Omega_m: float = 0.3, Omega_L: float = 0.7) -> float:
    """
    Simple flat ΛCDM Hubble parameter (DESI-inspired).
    H(z) = H0 * sqrt(Ω_m (1+z)^3 + Ω_Λ)
    """
    return H0 * math.sqrt(Omega_m * (1.0 + z)**3 + Omega_L)


# ------------------------------------------------------------
# Demonstration / example usage
# ------------------------------------------------------------
if __name__ == "__main__":
    # Example base power spectrum values (toy numbers)
    base_Cl = {
        0: 1000.0,
        1: 300.0,
        2: 50.0,
        200: 2500.0,
        500: 800.0,
        1000: 200.0
    }

    print("=== Multipole Subsets ===")
    for l in range(0, 4):
        print(f"S_{l} = {multipole_subset(l)}")

    print("\n=== Cyclic Progression (up to l=3) ===")
    prog = cyclic_progression(3)
    for i, subset in enumerate(prog):
        print(f"Stage {i}: {len(subset)} components")

    print("\n=== Evolved C_l(z, u) examples ===")
    redshifts = [0.0, 1.0, 1100.0]
    u_values = [0.0, 0.5, 1.0]

    for z in redshifts:
        for u in u_values:
            print(f"\nz = {z:.1f}, u = {u:.1f}")
            for l, Cl0 in base_Cl.items():
                Cl_evolved = evolved_Cl(Cl0, z, u, l)
                print(f"  l={l:4d}  C_l_base={Cl0:8.1f}  →  C_l(z,u)={Cl_evolved:10.3f}")

    print("\n=== Hubble parameter check ===")
    for z in [0.0, 0.5, 1.0, 2.0]:
        print(f"H({z:.1f}) = {hubble_parameter(z):.2f} km/s/Mpc")

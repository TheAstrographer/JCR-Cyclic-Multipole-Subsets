import math
import numpy as np

class JCRIntegratedClockSubsetEngine:
    def __init__(self):
        # --- JCR COSMOLOGICAL CLOCK DISCRETE INFRASTRUCTURE ---
        self.epsilon = 1e-9
        self.N_today = 1_000_000_000
        self.H_wind = 70.0               # Bosonic baseline (km/s/Mpc)
        self.sh_geom_base = 3.170        # Local geometric torque amplitude
        self.delta_phi_torque = 1.72113420759
        self.sin_torque = math.sin(self.delta_phi_torque)
        
        self.tau_damp = 5.8
        self.chi_screen_scale = 4500.0  # Mpc
        self.Omega_m = 0.3
        self.Omega_L = 0.7

        # --- CYCLIC SUBSET AXIOM MATRICES ---
        self.w_winding = 3.25            # Phase-locked winding operator parameter
        
# ============================================================
        # COMPLETE 15-ERA CHRONOLOGICAL PARTITION (Fully Accrued)
        # ============================================================
        self.epochs = [
            {"name": "Planck Epoch",                "u_start": 0.000, "u_end": 0.005, "max_l": 0},
            {"name": "Grand Unification",           "u_start": 0.005, "u_end": 0.010, "max_l": 0},
            {"name": "Inflationary Epoch",          "u_start": 0.010, "u_end": 0.030, "max_l": 0},
            {"name": "Electroweak Epoch",           "u_start": 0.030, "u_end": 0.040, "max_l": 1},
            {"name": "Quark Epoch",                 "u_start": 0.040, "u_end": 0.050, "max_l": 1},
            {"name": "Hadron Epoch",                "u_start": 0.050, "u_end": 0.060, "max_l": 1},
            {"name": "Lepton Epoch",                "u_start": 0.060, "u_end": 0.070, "max_l": 1},
            {"name": "Nucleosynthesis",             "u_start": 0.070, "u_end": 0.080, "max_l": 1},
            {"name": "Photon Epoch",                "u_start": 0.080, "u_end": 0.180, "max_l": 1},
            {"name": "Matter-Radiation Equality",   "u_start": 0.180, "u_end": 0.220, "max_l": 2},
            {"name": "Recombination/Decoupling",    "u_start": 0.220, "u_end": 0.280, "max_l": 2},
            {"name": "Cosmic Dark Ages",            "u_start": 0.280, "u_end": 0.400, "max_l": 2},
            {"name": "Cosmic Dawn & Reionization",  "u_start": 0.400, "u_end": 0.520, "max_l": 2},
            {"name": "Galaxy Formation & Structure","u_start": 0.520, "u_end": 0.750, "max_l": 3},
            {"name": "Dark Energy Domination",      "u_start": 0.750, "u_end": 1.000, "max_l": 4},
        ]

# --- CLOCK KINEMATICS ---
    def scale_factor(self, N: float) -> float:
        return math.exp(self.epsilon * N)

    def redshift(self, a: float) -> float:
        return 1.0 / a - 1.0

    def comoving_distance_approx(self, N: float) -> float:
        return 4500.0 * (N / self.N_today)

    def H_base(self, z: float) -> float:
        return self.H_wind * math.sqrt(self.Omega_m * (1 + z)**3 + self.Omega_L)

    def H_total(self, z: float, chi: float) -> float:
        f_mod = 1.0 + 5.0 * math.exp(-z / 2.0)
        f_damp = math.exp(-z / self.tau_damp)
        suppression = f_mod * f_damp * math.exp(-chi / self.chi_screen_scale)
        
        a = 1.0 / (1.0 + z)
        delta_H_torque = (self.sh_geom_base * a * self.sin_torque) * suppression * 0.528
        return self.H_base(z) + delta_H_torque

    # --- SUBSET SPECTRUM CALCULATIONS ---
    def formulate_multipole_subset(self, l: int) -> list:
        return [(l, m) for m in range(-l, l + 1)]
# --- SUBSET SPECTRUM CALCULATIONS ---
    def formulate_multipole_subset(self, l: int) -> list:
        return [(l, m) for m in range(-l, l + 1)]

    def get_clock_state_matrix(self, N_step: float) -> dict:
        """Maps a discrete lattice tick step N onto the active cosmological subset framework."""
        a = self.scale_factor(N_step)
        z = self.redshift(a)
        chi = self.comoving_distance_approx(N_step)
        H_t = self.H_total(z, chi)
        
        u_clamped = max(0.0, min(1.0, N_step / self.N_today))
        
        # Locate active chronological epoch
        current_epoch = self.epochs[-1]
        for epoch in self.epochs:
            if epoch["u_start"] <= u_clamped <= epoch["u_end"]:
                current_epoch = epoch
                break
                
        # Populate active harmonic subsets
        active_subsets = []
        total_elements = 0
        for l in range(0, current_epoch["max_l"] + 1):
            subset_elements = self.formulate_multipole_subset(l)
            active_subsets.append({f"S_{l}": subset_elements})
            total_elements += len(subset_elements)
            
phase_lock_factor = math.sin(2.0 * math.pi * u_clamped * self.w_winding)

        return {
            "N": N_step,
            "u": u_clamped,
            "a": a,
            "z": z,
            "H_total": H_t,
            "epoch_name": current_epoch["name"],
            "max_l": current_epoch["max_l"],
            "total_elements": total_elements,
            "phase_lock_resonance": phase_lock_factor,
            "subsets": active_subsets
        }

# ==============================================================================
# EXECUTION & VERIFICATION
# ==============================================================================
engine = JCRIntegratedClockSubsetEngine()

print("=" * 130)
print("   REBUILT JCR INTEGRATED CLOCK & CYCLIC MULTIPOLE SUBSET ENGINE — COMPLETE 15-ERA TABLE")
print("=" * 130)
print(f"{'Lattice Step N':>14}  {'u':>5}  {'Redshift z':>10}  {'H_total':>8}  {'Active Epoch':<32}  {'ℓmax':>4}  {'States':>6}  {'Phase'}")
print("-" * 130)

# Representative milestone ticks covering all major eras
milestone_ticks = [
    0,
    5_000_000,      # ~Planck / GUT
    20_000_000,     # Inflation
    45_000_000,     # Electroweak / Quark
    100_000_000,    # Photon Epoch
    200_000_000,    # Equality / Recombination
    350_000_000,    # Dark Ages
    450_000_000,    # Cosmic Dawn
    600_000_000,    # Galaxy Formation
    800_000_000,    # Dark Energy onset
    950_000_000,
    engine.N_today  # Present day
]

for n in milestone_ticks:
    m = engine.get_clock_state_matrix(n)
    print(f"{m['N']:14,d}  {m['u']:5.3f}  {m['z']:10.4f}  {m['H_total']:8.2f}  {m['epoch_name']:<32}  {m['max_l']:4d}  {m['total_elements']:6d}  {m['phase_lock_resonance']:+.4f}")

print("-" * 130)

# Present-day verification
present = engine.get_clock_state_matrix(engine.N_today)
print(f"\n[Present-Day Terminal Boundary] N = 10^9   u = 1.000")
print(f"  Epoch               : {present['epoch_name']}")
print(f"  Max multipole ℓ     : {present['max_l']}")
print(f"  Total visibility states : {present['total_elements']}  (full cascade → 25)")
print(f"  H_total             : {present['H_total']:.2f} km s⁻¹ Mpc⁻¹")
print(f"  Phase-lock resonance: {present['phase_lock_resonance']:+.5f}")
print(f"\n  Active Harmonic Architecture:")
for subset_entry in present["subsets"]:
    for name, elements in subset_entry.items():
        print(f"    {name:<4} ({len(elements)} states): {elements}")
print("=" * 130)

# Show the full epoch table for confirmation
print("\nCOMPLETE 15-ERA TABLE LOADED:")
print(f"{'Era Name':<35} {'u_start':>8} {'u_end':>8} {'ℓ_max':>6} {'States':>7}")
print("-" * 70)
for ep in engine.epochs:
    states = (ep["max_l"] + 1)**2
    print(f"{ep['name']:<35} {ep['u_start']:8.3f} {ep['u_end']:8.3f} {ep['max_l']:6d} {states:7d}")
print("=" * 70)

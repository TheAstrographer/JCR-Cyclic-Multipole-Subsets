import math
import numpy as np

class JCRCyclicSubsetEngine:
    def __init__(self):
        """
        Pure Python Engine executing the Cyclic Multipole Subset Evolution Axiom.
        Maps discrete harmonic spaces S_l to continuous cosmic time intervals u.
        """
        self.w_winding = 3.25  # Invariant phase-locked winding operator parameter
        
        # Explicitly define the chronological boundaries of the cosmological epochs
        self.epochs = [
            {"name": "Inflation",      "u_start": 0.00, "u_end": 0.05, "max_l": 0},
            {"name": "Radiation Dom.", "u_start": 0.05, "u_end": 0.35, "max_l": 1},
            {"name": "Matter Dom.",    "u_start": 0.35, "u_end": 0.75, "max_l": 2},
            {"name": "Dark Energy",    "u_start": 0.75, "u_end": 1.00, "max_l": 4}
        ]

    def formulate_multipole_subset(self, l: int) -> list:
        """
        Defines the discrete elements of subset S_l = {(l, m) | m = -l to l}.
        Returns exactly 2l + 1 elements matching your structural definitions.
        """
        subset_elements = []
        for m in range(-l, l + 1):
            subset_elements.append((l, m))
        return subset_elements

    def get_active_harmonic_matrix(self, u: float) -> dict:
        """
        Maps scaled time u = (t - t_min)/(t_max - t_min) straight to the active 
        chronological epoch and builds the cyclic multipole subset collection.
        """
        # Clamp u strictly between 0 and 1 to prevent out-of-boundary memory leaks
        u_clamped = max(0.0, min(1.0, u))
        
        current_epoch = self.epochs[-1]  # Default fallback matrix entry
        for epoch in self.epochs:
            if epoch["u_start"] <= u_clamped <= epoch["u_end"]:
                current_epoch = epoch
                break
                
        # Build the dynamic multi-layered subset list: {S_0, S_1, ..., S_max_l}
        active_subsets = []
        total_elements = 0
        
        for l in range(0, current_epoch["max_l"] + 1):
            subset_s = self.formulate_multipole_subset(l)
            active_subsets.append({f"S_{l}": subset_s})
            total_elements += len(subset_s)
            
        # Calculate the live phase-locked cyclic resonance transformation tracking factor
        # Connects your microscopic tick evolution directly to the macroscopic epoch phase
        phase_lock_factor = math.sin(2.0 * math.pi * u_clamped * self.w_winding)

        return {
            "scaled_time_u": u_clamped,
            "epoch_name": current_epoch["name"],
            "max_degree_l": current_epoch["max_l"],
            "subsets": active_subsets,
            "total_active_elements": total_elements,
            "phase_lock_resonance": phase_lock_factor
        }

# ==============================================================================
# PIPELINE EXECUTION SUMMARY AND DIAGNOSTIC LOOP
# ==============================================================================
if __name__ == "__main__":
    print("=" * 110)
    print("         EXECUTING JOSHUA CHRISTOPHER RYAN'S CYCLIC MULTIPOLE SUBSET PIPELINE")
    print("=" * 110)
    
    engine = JCRCyclicSubsetEngine()
    
    # Define milestone test ticks across the scaled cosmic timeline u
    test_time_ticks = [0.02, 0.15, 0.55, 0.88, 1.00]
    
    print(f"{'Scaled Time (u)':<17} {'Cosmological Epoch':<20} {'Max Degree (l)':<16} {'Total States (∑ 2l+1)':<22} {'Phase Resonance'}")
    print("-" * 110)
    
    for u_tick in test_time_ticks:
        matrix = engine.get_active_harmonic_matrix(u_tick)
        print(f"{matrix['scaled_time_u']:<17.2f} {matrix['epoch_name']:<20} {matrix['max_degree_l']:<16} {matrix['total_active_elements']:<22} {matrix['phase_lock_resonance']:+.5f}")
        
    print("-" * 110)
    
    # Detailed output snapshot illustrating present day (u = 1.0) structural alignments
    present_day = engine.get_active_harmonic_matrix(1.0)
    print(f"\n[Verification] Present-Day (u = 1.0) Active Subset Blueprint Layout:")
    for subset_entry in present_day["subsets"]:
        for name, elements in subset_entry.items():
            print(f"  • Harmonic Set {name:<5} -> Contains {len(elements)} items: {elements}")
    print("=" * 110)

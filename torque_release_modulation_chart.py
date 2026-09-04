import matplotlib.pyplot as plt
import numpy as np
import math

# Parameters from the engine
epsilon = 1e-9
N_today = 1_000_000_000
H_wind = 70.0
sh_geom_base = 3.170
delta_phi_torque = 1.72113420759
sin_torque = math.sin(delta_phi_torque)
tau_damp = 5.8
chi_screen_scale = 4500.0
Omega_m = 0.3
Omega_L = 0.7

# Generate u from 0 to 1
u_vals = np.linspace(0, 1, 600)
N_vals = u_vals * N_today

a_vals = np.exp(epsilon * N_vals)
z_vals = 1.0 / a_vals - 1.0
chi_vals = 4500.0 * u_vals   # comoving_distance_approx

# Modulation factors
f_mod = 1.0 + 5.0 * np.exp(-z_vals / 2.0)
f_damp = np.exp(-z_vals / tau_damp)
f_screen = np.exp(-chi_vals / chi_screen_scale)
suppression = f_mod * f_damp * f_screen

# Torque contribution (following the code formula)
delta_H_torque = (sh_geom_base * a_vals * sin_torque) * suppression * 0.528

# H_base and H_total
H_base = H_wind * np.sqrt(Omega_m * (1 + z_vals)**3 + Omega_L)
H_total = H_base + delta_H_torque

# Create multi-panel chart
fig, axes = plt.subplots(4, 1, figsize=(12, 13), sharex=True)
fig.suptitle('Torque Release Modulation by Continuous Damping & Screening Functions\n'
             r'Effective Expansion Rate Rises Smoothly Despite Discrete Multipole Cascade',
             fontsize=14, fontweight='bold', y=0.98)

# Color scheme
c1, c2, c3, c4 = '#e74c3c', '#3498db', '#2ecc71', '#9b59b6'

# Panel 1: Individual modulation factors
axes[0].plot(u_vals, f_mod, color=c1, lw=2.2, label=r'Modulation $1 + 5e^{-z/2}$')
axes[0].plot(u_vals, f_damp, color=c2, lw=2.2, label=r'Redshift damping $e^{-z/\tau_{\rm damp}}$')
axes[0].plot(u_vals, f_screen, color=c3, lw=2.2, label=r'Geometric screening $e^{-\chi/\chi_{\rm screen}}$')
axes[0].plot(u_vals, suppression, color=c4, lw=2.8, linestyle='--', label='Combined suppression')
axes[0].set_ylabel('Factor value', fontsize=11)
axes[0].set_ylim(0, 7)
axes[0].legend(loc='upper right', fontsize=9, framealpha=0.9)
axes[0].grid(True, alpha=0.3)
axes[0].set_title('Continuous Modulation Factors', fontsize=12)
axes[0].axhline(1.0, color='gray', ls=':', alpha=0.6)

# Panel 2: Torque contribution ΔH
axes[1].plot(u_vals, delta_H_torque, color='#e67e22', lw=2.5)
axes[1].fill_between(u_vals, 0, delta_H_torque, color='#e67e22', alpha=0.25)
axes[1].set_ylabel(r'$\Delta H_{\rm torque}$ (km s$^{-1}$ Mpc$^{-1}$)', fontsize=11)
axes[1].grid(True, alpha=0.3)
axes[1].set_title('Local Torque Contribution (smoothly released)', fontsize=12)
axes[1].axhline(3.17, color='red', ls='--', alpha=0.7, label=r'Full torque amplitude $\approx 3.17$')
axes[1].legend(loc='upper right', fontsize=9)

# Panel 3: H_base vs H_total
axes[2].plot(u_vals, H_base, color='#7f8c8d', lw=2.0, label=r'$H_{\rm base}$ (fiducial)')
axes[2].plot(u_vals, H_total, color='#c0392b', lw=2.5, label=r'$H_{\rm total} = H_{\rm base} + \Delta H_{\rm torque}$')
axes[2].fill_between(u_vals, H_base, H_total, color='#c0392b', alpha=0.2)
axes[2].set_ylabel(r'$H$ (km s$^{-1}$ Mpc$^{-1}$)', fontsize=11)
axes[2].grid(True, alpha=0.3)
axes[2].set_title('Effective Expansion Rate (smooth rise)', fontsize=12)
axes[2].legend(loc='upper right', fontsize=9)
axes[2].axhline(73.17, color='green', ls='--', alpha=0.7, label=r'Target $73.17$')
axes[2].legend(loc='upper right', fontsize=9)

# Panel 4: Redshift and scale factor for context
ax4a = axes[3]
ax4b = ax4a.twinx()
line1 = ax4a.plot(u_vals, z_vals, color='#2980b9', lw=2.0, label='Redshift $z$')
line2 = ax4b.plot(u_vals, a_vals, color='#27ae60', lw=2.0, label='Scale factor $a$')
ax4a.set_ylabel(r'Redshift $z$', color='#2980b9', fontsize=11)
ax4b.set_ylabel(r'Scale factor $a$', color='#27ae60', fontsize=11)
ax4a.set_xlabel(r'Scaled Cosmic Time $u = N / N_{\rm today}$', fontsize=12)
ax4a.grid(True, alpha=0.3)
ax4a.set_title('Underlying Clock Variables', fontsize=12)

# Combined legend
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax4a.legend(lines, labels, loc='center right', fontsize=9)

# Epoch shading on all panels
epoch_bounds = [0.00, 0.05, 0.35, 0.75, 1.00]
epoch_colors = ['#ffcccc', '#ccffcc', '#ccccff', '#ffffcc']
epoch_names = ['Inflation', 'Radiation', 'Matter', 'Dark Energy']

for ax in axes:
    for i in range(4):
        ax.axvspan(epoch_bounds[i], epoch_bounds[i+1], alpha=0.15, color=epoch_colors[i])
    for b in epoch_bounds[1:-1]:
        ax.axvline(b, color='black', ls=':', alpha=0.4, lw=1)

# Add epoch labels on top panel
for i, name in enumerate(epoch_names):
    mid = (epoch_bounds[i] + epoch_bounds[i+1]) / 2
    axes[0].text(mid, 6.5, name, ha='center', va='bottom', fontsize=8, 
                 color='#333333', style='italic')

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('torque_release_modulation_chart.png', dpi=150, bbox_inches='tight', facecolor='white')
print("Chart saved as torque_release_modulation_chart.png")
plt.close()

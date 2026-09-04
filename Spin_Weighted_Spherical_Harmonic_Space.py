import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Circle
import matplotlib.patches as mpatches

fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111)
ax.set_xlim(-5.5, 5.5)
ax.set_ylim(-1, 6)
ax.set_aspect('equal')
ax.axis('off')

# Title
fig.suptitle('Spin-Weighted Spherical-Harmonic Space up to $\\ell=4$\n'
             r'Total Dimension: $\sum_{\ell=0}^{4}(2\ell+1)=25$ Independent Projectable Visibility States',
             fontsize=16, fontweight='bold', y=0.98)

# Colors for each ℓ
colors = {
    0: '#e74c3c',  # red
    1: '#3498db',  # blue
    2: '#2ecc71',  # green
    3: '#9b59b6',  # purple
    4: '#f39c12'   # orange
}

# Draw rows for each ℓ
y_positions = {0: 5.0, 1: 3.9, 2: 2.8, 3: 1.7, 4: 0.6}

for ell in range(5):
    y = y_positions[ell]
    n_states = 2*ell + 1
    
    # Label for ℓ
    ax.text(-5.2, y, f'$\\ell={ell}$', fontsize=14, fontweight='bold',
            va='center', ha='right', color=colors[ell])
    
    # State count
    ax.text(5.2, y, f'{n_states} states', fontsize=11, va='center', ha='left',
            color=colors[ell], style='italic')
    
    # Draw the m states
    m_values = list(range(-ell, ell+1))
    spacing = 1.0 if ell < 3 else 0.9
    start_x = - (n_states - 1) * spacing / 2
    
    for i, m in enumerate(m_values):
        x = start_x + i * spacing
        
        # Circle for each state
        circle = Circle((x, y), 0.32, facecolor=colors[ell], edgecolor='black',
                        linewidth=1.5, alpha=0.85, zorder=3)
        ax.add_patch(circle)
        
        # Label (ℓ, m)
        ax.text(x, y, f'$({ell},{m})$', fontsize=8, ha='center', va='center',
                color='white', fontweight='bold', zorder=4)
    
# Horizontal baseline
    ax.plot([-4.5, 4.5], [y-0.45, y-0.45], color='gray', linewidth=0.5, alpha=0.4)

# Total box at bottom
total_box = FancyBboxPatch((-3.5, -0.7), 7, 0.55, boxstyle="round,pad=0.05",
                           facecolor='#2c3e50', edgecolor='black', linewidth=2, alpha=0.9)
ax.add_patch(total_box)
ax.text(0, -0.42, r'Total: 25 Independent Projectable Visibility States  ($\ell_{\max}=4$)',
        fontsize=13, ha='center', va='center', color='white', fontweight='bold')

# Legend / note
ax.text(0, 5.7, r'Spin weight $s=0$ (scalar) spherical harmonics $Y_{\ell m}$  |  Each circle = one projectable channel $S_{\ell,m}$',
        fontsize=10, ha='center', style='italic', color='#555555')

# Epoch annotation
ax.text(0, -1.1, 'Activated fully in the Dark Energy epoch ($u \\geq 0.75$) → releases full local torque component',
        fontsize=11, ha='center', color='#c0392b', fontweight='bold')

plt.tight_layout(rect=[0, 0.02, 1, 0.94])
plt.savefig('spin_weighted_spherical_harmonic_space_l4.png', dpi=160, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("Chart saved successfully.")
plt.close()

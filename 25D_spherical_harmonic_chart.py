#!/usr/bin/env python3
"""
Cyclic Multipole Subset Chart
Full Twenty-Five-Dimensional Visibility Space of the Dark-Energy Era
Spherical-Harmonic Standing-Wave Nodes on the Unit Sphere
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.special import sph_harm_y
import matplotlib.colors as mcolors

def plot_sh(l, m, ax, title, exaggerate=0.22):
    """Plot a real spherical harmonic standing-wave pattern on the unit sphere."""
    phi = np.linspace(0, 2 * np.pi, 100)
    theta = np.linspace(0, np.pi, 50)
    phi, theta = np.meshgrid(phi, theta)

    Y = sph_harm_y(l, m, theta, phi)
    amp = Y.real

    vmax = np.max(np.abs(amp)) + 1e-12
    r = 1.0 + exaggerate * (amp / vmax)

    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)

    norm = mcolors.TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)

    ax.plot_surface(
        x, y, z,
        facecolors=plt.cm.RdBu_r(norm(amp)),
        rstride=1, cstride=1,
        linewidth=0, antialiased=True, alpha=0.93
    )

    ax.set_title(title, fontsize=9, pad=4)
    ax.set_axis_off()
    ax.set_box_aspect([1, 1, 1])

    lim = 1.35
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_zlim(-lim, lim)


# ------------------------------------------------------------------
# Main figure
# ------------------------------------------------------------------
fig = plt.figure(figsize=(15, 11))

# Representative modes that span the full 25-dimensional space (ℓ = 0 … 4)
modes = [
    (0, 0, "S0  ℓ=0 m=0\nMonopole\n1 state"),
    (1, 0, "S1  ℓ=1 m=0\nDipole\n3 states total"),
    (1, 1, "S1  ℓ=1 m=±1\nDipole components"),
    (2, 0, "S2  ℓ=2 m=0\nQuadrupole\n5 states total"),
    (2, 2, "S2  ℓ=2 m=±2\nHigh-symmetry"),
    (3, 0, "S3  ℓ=3 m=0\nOctupole\n7 states total"),
    (3, 2, "S3  ℓ=3 m=2\nOctupole"),
    (4, 0, "S4  ℓ=4 m=0\nHexadecapole\n9 states total"),
    (4, 4, "S4  ℓ=4 m=±4\nHighest symmetry\nvertices"),
]

# 3×3 grid
for i, (l, m, title) in enumerate(modes):
    ax = fig.add_subplot(3, 3, i + 1, projection='3d')
    plot_sh(l, m, ax, title)

# Title
plt.suptitle(
    "Cyclic Multipole Subset Chart\n"
    "Full Twenty-Five-Dimensional Visibility Space of the Dark-Energy Era\n"
    "Spherical-Harmonic Standing-Wave Nodes on the Unit Sphere\n"
    "ℓ = 0 → 4  |  Σ(2ℓ+1) = 25 Independent Projectable States  |  "
    "Full Torque Release → H₀ = 73.17 km s⁻¹ Mpc⁻¹",
    fontsize=13, y=0.98
)

# Footer
fig.text(
    0.5, 0.02,
    "Red/Blue = opposite phase lobes   |   White = nodal lines (zero amplitude)\n"
    "High-symmetry vertices = preferred stable projection / resonance nodes "
    "in the Dark-Energy epoch (u ≥ 0.75)",
    ha='center', fontsize=9, style='italic'
)

plt.tight_layout(rect=[0, 0.04, 1, 0.93])

# Save
plt.savefig(
    'cyclic_multipole_25D_spherical_resonance.png',
    dpi=160,
    bbox_inches='tight',
    facecolor='white'
)
print("Saved: cyclic_multipole_25D_spherical_resonance.png")
plt.close()
print("Done.")

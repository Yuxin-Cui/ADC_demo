import numpy as np
import matplotlib.pyplot as plt

# 1. Define the Parameters
E_max = 100        # Maximum inhibition (%)
E_min = 0          # Baseline inhibition (%)
log_IC50 = 1.0     # The log10 of the IC50 (IC50 = 10 units)
hill_slope = 1.5   # Steepness of the curve

# 2. Generate Data
# We use a log scale for the x-axis to create the sigmoidal shape
log_conc = np.linspace(-1, 3, 1000) 
conc = 10**log_conc

# The Hill Equation (Four-parameter logistic curve)
def hill_equation(x, top, bottom, log_ic50, hill):
    return bottom + (top - bottom) / (1 + 10**((log_ic50 - x) * hill))

y = hill_equation(log_conc, E_max, E_min, log_IC50, hill_slope)

# 3. Create the Plot
plt.figure(figsize=(7, 5))

# --- AUC (Area Under the Curve) ---
# We fill the area first so it sits behind the lines
plt.fill_between(log_conc, y, color='skyblue', alpha=0.3, label='AUC (Area Under Curve)')

# --- Main Dose-Response Curve ---
plt.plot(log_conc, y, label='Dose-Response Curve', color='navy', linewidth=3)

# --- E_max (Maximum Efficacy) ---
plt.axhline(y=E_max, color='red', linestyle='--', alpha=0.7, linewidth=2)
plt.text(2.6, E_max + 2, r'$E_{max}$', color='red', fontsize=14, fontweight='bold')

# --- 50% Killing Line and IC50 ---
# Based on your previous preference, we add the 50% threshold line
plt.axhline(y=50, color='green', linestyle=':', linewidth=2, label='50% Killing Line')
plt.plot([log_IC50, log_IC50], [0, 50], color='green', linestyle='--', linewidth=1.5)
plt.plot(log_IC50, 50, 'go', markersize=8) # Point at the IC50
plt.text(log_IC50 - 0.35, 55, r'$IC_{50}$', color='green', fontsize=14, fontweight='bold')

# --- Hill Slope Visualization ---
# Calculating a tangent arrow at the midpoint to show steepness
mid_idx = np.argmin(np.abs(log_conc - log_IC50))
x_mid = log_conc[mid_idx]
y_mid = y[mid_idx]
dx = 0.4
slope_val = (hill_slope * np.log(10) * (E_max - E_min) / 4)
dy = slope_val * dx
plt.arrow(x_mid - dx/2, y_mid - dy/2, dx, dy, color='darkmagenta', 
          width=0.03, head_width=0.12, length_includes_head=True)
plt.text(x_mid + 0.25, y_mid - 15, 'Hill Slope\n(Steepness)', 
         color='darkmagenta', fontsize=12, fontweight='bold')

# 4. Labels and Aesthetics
plt.title('Dose-Response Parameters', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Log Concentration $[D]$', fontsize=14)
plt.ylabel('Inhibition (%)', fontsize=14)
plt.ylim(0, 115)
plt.xlim(-1, 3)
plt.grid(True, which='both', linestyle='--', alpha=0.4)
plt.legend(loc='lower right', fontsize=12)

# 5. Export at High Resolution (300 DPI)
plt.tight_layout()
plt.savefig('dose_response_plot.png', dpi=300)
plt.show()

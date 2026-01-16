import matplotlib.pyplot as plt
import numpy as np

# 1. SETUP DATA
doses = [0, 1, 2, 4, 8, 16]

# Sensitive Group (Low baseline)
base_sens = 1000
raw_sens = np.array([1000, 700, 400, 150, 50, 10])

# Resistant Group (High baseline)
base_res = 5000
raw_res = np.array([5000, 4900, 4750, 4500, 4250, 4000])

# 2. CALCULATE NORMALIZED METRICS
# Relative Viability (Fraction of 1)
viability_sens = raw_sens / base_sens
viability_res = raw_res / base_res

# Percent Killing (100 - Viability%)
killing_sens = (1 - viability_sens) * 100
killing_res = (1 - viability_res) * 100

# 3. CREATE FIGURE WITH 3 SUBPLOTS
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 6))

color_sens = '#D62728' # Red
color_res  = '#1F77B4' # Blue

# --- PLOT 1: RAW COUNTS ---
ax1.plot(doses, raw_sens, label='Sensitive', color=color_sens, marker='o', linewidth=2.5)
ax1.plot(doses, raw_res, label='Resistant', color=color_res, marker='s', linestyle='--', linewidth=2.5)
ax1.set_title('1. RAW COUNTS\n(Misleading Scale)', fontweight='bold')
ax1.set_ylabel('Absolute Cell Count')

# --- PLOT 2: RELATIVE VIABILITY ---
ax2.plot(doses, viability_sens * 100, label='Sensitive', color=color_sens, marker='o', linewidth=2.5)
ax2.plot(doses, viability_res * 100, label='Resistant', color=color_res, marker='s', linestyle='--', linewidth=2.5)
ax2.axhline(50, color='black', linestyle=':', linewidth=1.5) # 50% Threshold
ax2.set_title('2. RELATIVE VIABILITY\n(Survival %)', fontweight='bold')
ax2.set_ylabel('% Viability (Relative to Dose 0)')
ax2.set_ylim(-5, 105)

# --- PLOT 3: PERCENT KILLING ---
ax3.plot(doses, killing_sens, label='Sensitive', color=color_sens, marker='o', linewidth=2.5)
ax3.plot(doses, killing_res, label='Resistant', color=color_res, marker='s', linestyle='--', linewidth=2.5)
ax3.axhline(50, color='black', linestyle=':', linewidth=1.5) # 50% Threshold
ax3.set_title('3. PERCENT KILLING\n(Drug Efficacy)', fontweight='bold')
ax3.set_ylabel('% Killed Relative to Baseline')
ax3.set_ylim(-5, 105)

# 4. STYLING
for ax in [ax1, ax2, ax3]:
    ax.grid(False)
    ax.set_xlabel('Dose')
    for spine in ['top', 'right', 'bottom', 'left']:
        ax.spines[spine].set_linewidth(1.5)
    ax.legend(frameon=True, edgecolor='black')

plt.tight_layout()
plt.show()
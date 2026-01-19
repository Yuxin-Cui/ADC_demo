import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import SmoothBivariateSpline

# -----------------------------
# 1. Simulate plate with edge effect
# -----------------------------
np.random.seed(42)

n_rows, n_cols = 8, 12  # 96-well plate

rows, cols = np.meshgrid(
    np.arange(1, n_rows + 1),
    np.arange(1, n_cols + 1),
    indexing="ij"
)

true_signal = 100

edge_effect = (
    15 * (np.abs(rows - (n_rows + 1) / 2) +
          np.abs(cols - (n_cols + 1) / 2))
)

signal = true_signal + edge_effect + np.random.normal(0, 3, rows.shape)

df = pd.DataFrame({
    "row": rows.ravel(),
    "col": cols.ravel(),
    "signal": signal.ravel()
})

# -----------------------------
# 2. Fit 2D surface (robust spline)
# -----------------------------
spline = SmoothBivariateSpline(
    df["row"],
    df["col"],
    df["signal"],
    kx=3,
    ky=3,
    s=100  # smoothing factor to avoid nxest warning
)

df["spatial_bias"] = spline.ev(df["row"], df["col"])

# -----------------------------
# 3. Correct edge effect
# -----------------------------
df["signal_corrected"] = (
    df["signal"]
    - df["spatial_bias"]
    + np.median(df["signal"])
)

# -----------------------------
# 4. Plot before and after
# -----------------------------
fig, axes = plt.subplots(1, 2, figsize=(10, 4))

axes[0].imshow(
    df.pivot(index="row", columns="col", values="signal"),
    cmap="viridis"
)
axes[0].set_title("Before Correction")
axes[0].invert_yaxis()

axes[1].imshow(
    df.pivot(index="row", columns="col", values="signal_corrected"),
    cmap="viridis"
)
axes[1].set_title("After 2D Surface Correction")
axes[1].invert_yaxis()

plt.tight_layout()
plt.show()

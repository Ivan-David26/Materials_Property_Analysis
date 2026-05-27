# %% [markdown]
# # Notebook 2: Temperature-Dependent Material Properties
#
# **Project:** Materials Property Visualization and Analysis Using Python  
# **Author:** Materials Engineering Portfolio Project
#
# ---
#
# ## Engineering Context
#
# In real-world applications, materials rarely operate at room temperature.
# Elevated temperatures significantly degrade most mechanical properties:
#
# - **Yield strength** drops as thermal energy assists dislocation motion (creep onset)
# - **Elastic modulus** decreases as atomic bond stiffness weakens
# - **Thermal conductivity** may increase or decrease depending on the mechanism
#   (phonon vs. electron dominated)
#
# This notebook analyzes how five key engineering alloys perform across a wide temperature
# range, with engineering commentary on their suitability for elevated-temperature service.
#
# ### Materials Analyzed
# | Material | Primary Use Case | Max Service Temp |
# |----------|-----------------|-----------------|
# | AISI 4140 Steel | Structural, oil & gas | ~480°C |
# | Aluminum 6061-T6 | Automotive, aerospace | ~150°C |
# | Titanium Ti-6Al-4V | Aerospace structures | ~315°C |
# | Inconel 718 | Jet engines, turbines | ~650°C |
# | AISI 304 Stainless | Chemical plant, food | ~870°C |
# | Nylon 66 | Gears, housings | ~100°C |

# %% [markdown]
# ## 1. Setup

# %%
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.insert(0, os.path.join("..", "src"))
from data_loader import load_temperature_data
from visualizations import plot_temperature_strength

# %%
df_temp = load_temperature_data(
    filepath=os.path.join("..", "data", "raw", "temperature_dependent_properties.csv")
)
print(f"Loaded {len(df_temp)} data points for {df_temp['Material'].nunique()} materials")
df_temp.head(12)

# %% [markdown]
# ## 2. Yield Strength vs. Temperature

# %%
fig = plot_temperature_strength(df_temp)
plt.show()

# %% [markdown]
# ### Engineering Interpretation
#
# **Aluminum 6061-T6** shows rapid strength degradation above 150°C.
# The T6 temper (age-hardening) depends on fine precipitates (Mg₂Si) that coarsen
# and dissolve at elevated temperatures, eliminating their strengthening effect.
# This is why aluminum engines require water cooling.
#
# **Titanium Ti-6Al-4V** maintains useful strength up to about 315°C in airframe
# applications (though the alloy is capable to ~600°C for non-sustained loading).
# Its excellent specific strength at moderate temperatures makes it ideal for aircraft
# bulkheads and engine nacelles.
#
# **AISI 4140 Steel** is a workhorse structural steel with reasonable high-temperature
# capability (~480°C for sustained service). At higher temperatures, it enters the
# creep regime and tempering embrittlement becomes a concern.
#
# **Inconel 718** is the star of high-temperature performance — a precipitation-hardened
# nickel superalloy that retains over 60% of its room-temperature yield strength at 650°C.
# This makes it indispensable for turbine discs and high-pressure compressor blades.
#
# **Nylon 66** degrades rapidly above 80°C and becomes unusable above ~130°C.
# Elevated-temperature polymer applications typically require PEEK or polyimides.

# %% [markdown]
# ## 3. Normalized Strength Retention

# %%
# Calculate strength retention relative to room temperature (20°C) value
materials = df_temp["Material"].unique()
fig, ax = plt.subplots(figsize=(11, 6))

palette = sns.color_palette("tab10", n_colors=len(materials))

for i, mat in enumerate(materials):
    subset = df_temp[df_temp["Material"] == mat].sort_values("Temperature_C")
    # Reference value at 20°C (or closest available)
    ref = subset.loc[(subset["Temperature_C"] - 20).abs().idxmin(), "Yield_Strength_MPa"]
    if ref > 0:
        retention = subset["Yield_Strength_MPa"] / ref * 100
        ax.plot(subset["Temperature_C"], retention, marker="o", markersize=5,
                color=palette[i], label=mat, linewidth=1.8)

ax.axhline(y=50, color="red", linestyle="--", linewidth=1, alpha=0.6, label="50% retention")
ax.axhline(y=75, color="orange", linestyle=":", linewidth=1, alpha=0.6, label="75% retention")
ax.set_xlabel("Temperature (°C)", fontsize=12)
ax.set_ylabel("Yield Strength Retention (% of room-temp value)", fontsize=11)
ax.set_title("Normalized Yield Strength Retention vs. Temperature", fontsize=13)
ax.legend(fontsize=9, loc="lower left")
ax.set_ylim(0, 115)
ax.grid(True, alpha=0.4, linestyle="--")
plt.tight_layout()
plt.show()

# %% [markdown]
# The normalized plot removes the absolute strength differences and lets us compare
# **how quickly** each material degrades with temperature.
#
# - **Inconel 718** retains ~80% of strength at 650°C — exceptional.
# - **Titanium Ti-6Al-4V** retains ~57% at 600°C.
# - **Nylon 66** retains only ~8% at 130°C — very temperature-sensitive.
# - **Aluminum 6061-T6** crosses the 50% retention line around 200°C.

# %% [markdown]
# ## 4. Thermal Conductivity vs. Temperature

# %%
fig, ax = plt.subplots(figsize=(10, 6))
palette = sns.color_palette("tab10", n_colors=len(materials))

for i, mat in enumerate(materials):
    subset = df_temp[df_temp["Material"] == mat].sort_values("Temperature_C")
    ax.plot(
        subset["Temperature_C"],
        subset["Thermal_Conductivity_W_mK"],
        marker="s", markersize=4,
        color=palette[i], label=mat, linewidth=1.8,
    )

ax.set_xlabel("Temperature (°C)", fontsize=12)
ax.set_ylabel("Thermal Conductivity (W/m·K)", fontsize=12)
ax.set_title("Thermal Conductivity vs. Temperature\nfor Selected Engineering Materials", fontsize=13)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.4, linestyle="--")
plt.tight_layout()
plt.show()

# %% [markdown]
# **Engineering note on thermal conductivity trends:**
#
# - **Steels and aluminum alloys**: Conductivity decreases slightly with temperature
#   (electron scattering increases as lattice vibrations intensify).
# - **Inconel 718**: Conductivity *increases* with temperature — characteristic of alloys
#   where phonon conduction dominates over electron conduction.
# - **Nylon 66**: Nearly constant — polymers conduct heat mainly through molecular vibration
#   (chain motion), which is relatively insensitive to temperature in the solid state.
# - **Titanium alloys**: Historically poor conductors — the complex HCP crystal structure
#   and alloy additions scatter both electrons and phonons.

# %% [markdown]
# ## 5. Practical Service Temperature Recommendations

# %%
# Calculate the temperature at which yield strength drops to 75% of room-temperature value
print("Estimated temperature at which yield strength drops to 75% of room-temperature value:")
print("-" * 60)

for mat in materials:
    subset = df_temp[df_temp["Material"] == mat].sort_values("Temperature_C")
    ref = subset.loc[(subset["Temperature_C"] - 20).abs().idxmin(), "Yield_Strength_MPa"]
    threshold = 0.75 * ref

    # Find where strength first drops below threshold
    below = subset[subset["Yield_Strength_MPa"] < threshold]
    if not below.empty:
        temp_75 = below["Temperature_C"].iloc[0]
        print(f"  {mat:<35} → {temp_75:>5}°C")
    else:
        print(f"  {mat:<35} → > {subset['Temperature_C'].max()}°C (within data range)")

# %% [markdown]
# ## 6. Summary
#
# Key engineering conclusions from the temperature analysis:
#
# 1. **Material selection must always specify the operating temperature range.**
#    A material that is ideal at room temperature may be completely inadequate at 200°C.
#
# 2. **Aluminum alloys** are generally limited to ~150°C for structural applications
#    where strength is the design criterion.
#
# 3. **Nickel superalloys** like Inconel 718 are the go-to choice for gas turbine
#    hot sections (combustor, high-pressure turbine) where temperatures exceed 500°C.
#
# 4. **Titanium alloys** fill the critical 150–315°C window in aerospace where aluminum
#    is too weak but superalloys are too heavy.
#
# 5. **Polymers** are temperature-sensitive; always check the HDT (Heat Deflection
#    Temperature) and glass transition temperature (Tg) before specifying.

# %%
print("Notebook 02 complete. Proceed to 03_automotive_lightweighting.ipynb")

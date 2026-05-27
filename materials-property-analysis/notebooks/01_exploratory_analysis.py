# %% [markdown]
# # Notebook 1: Exploratory Data Analysis of Engineering Materials
#
# **Project:** Materials Property Visualization and Analysis Using Python  
# **Author:** Materials Engineering Portfolio Project  
# **Date:** 2024
#
# ---
#
# ## Overview
#
# This notebook performs an initial exploratory data analysis (EDA) on a dataset of
# 52 engineering materials spanning seven material classes:
#
# - Steels
# - Aluminum Alloys
# - Other Metals (Ti, Mg, Cu)
# - Polymers
# - Ceramics
# - Fiber-Reinforced Composites
# - Superalloys
#
# We'll examine the distribution of key mechanical and thermal properties, identify
# interesting patterns, and prepare the data for deeper analysis in subsequent notebooks.
#
# ---
#
# ### Key Properties We'll Examine
#
# | Property | Symbol | Unit | Significance |
# |----------|--------|------|-------------|
# | Tensile Strength | σ_UTS | MPa | Maximum load-bearing capacity |
# | Yield Strength | σ_y | MPa | Onset of permanent deformation |
# | Elastic Modulus | E | GPa | Stiffness (resistance to elastic deformation) |
# | Hardness | HV | — | Resistance to indentation / surface wear |
# | Density | ρ | g/cm³ | Mass per unit volume |
# | Thermal Conductivity | k | W/(m·K) | Heat transfer capability |
# | Elongation | δ | % | Ductility — strain at fracture |

# %% [markdown]
# ## 1. Setup and Imports

# %%
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Add src/ to path so we can import our modules
sys.path.insert(0, os.path.join("..", "src"))

from data_loader import load_main_dataset, get_category_summary
from visualizations import (
    plot_category_distribution,
    plot_ashby_strength_density,
    plot_hardness_vs_tensile,
    plot_thermal_conductivity,
    plot_correlation_heatmap,
    plot_boxplots_by_category,
)

print("Libraries loaded successfully.")

# %% [markdown]
# ## 2. Load and Inspect the Dataset

# %%
df = load_main_dataset(filepath=os.path.join("..", "data", "raw", "materials_properties.csv"))
print(f"Dataset shape: {df.shape[0]} materials × {df.shape[1]} properties\n")
df.head(10)

# %%
# Check data types and missing values
print("Data types:\n", df.dtypes, "\n")
print("Missing values:\n", df.isnull().sum())

# %% [markdown]
# ### Observation
# Only `Melting_Point_C` has missing values — this is expected because composites
# do not have a true melting point (they thermally degrade instead).

# %% [markdown]
# ## 3. Basic Statistical Summary

# %%
# Overall descriptive statistics for numeric columns
numeric_cols = [
    "Tensile_Strength_MPa", "Yield_Strength_MPa", "Elastic_Modulus_GPa",
    "Hardness_HV", "Density_g_cm3", "Thermal_Conductivity_W_mK",
    "Elongation_percent", "Specific_Strength_MPa_g_cm3"
]

stats = df[numeric_cols].describe().round(2)
stats

# %% [markdown]
# **Key observations from the summary statistics:**
#
# - **Tensile strength** spans an enormous range: 25 MPa (PTFE/Teflon) to 2450 MPa (Maraging Steel 350).
#   This 98× range reflects the fundamental differences between material classes.
# - **Thermal conductivity** is similarly wide: <1 W/m·K for polymers and composites
#   vs. 388 W/m·K for copper — a span of three orders of magnitude.
# - **Density** ranges from 0.91 g/cm³ (polypropylene) to 8.94 g/cm³ (copper),
#   immediately explaining why lightweight materials matter for transport applications.
# - **Elongation** is bimodal: ceramics and some composites show 0% (brittle),
#   while annealed metals can exceed 300%.

# %%
# Category-level summary
summary = get_category_summary(df)
print("Category-level mean values:")
summary.xs("mean", axis=1, level=1).round(1)

# %% [markdown]
# ## 4. Dataset Composition

# %%
fig = plot_category_distribution(df)
plt.show()

# %% [markdown]
# The dataset contains a good cross-section of engineering materials.
# Steels dominate (as they do in most structural applications), followed by
# aluminum alloys and polymers. Composites are a smaller but increasingly
# important class in modern engineering.

# %% [markdown]
# ## 5. Property Distributions

# %% [markdown]
# ### 5.1 Tensile Strength Distribution

# %%
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Histogram
df["Tensile_Strength_MPa"].hist(bins=20, ax=axes[0], color="#2980B9", edgecolor="white")
axes[0].set_xlabel("Tensile Strength (MPa)")
axes[0].set_ylabel("Count")
axes[0].set_title("Distribution of Tensile Strength")
axes[0].axvline(df["Tensile_Strength_MPa"].mean(), color="red",
                linestyle="--", label=f"Mean: {df['Tensile_Strength_MPa'].mean():.0f} MPa")
axes[0].legend()

# Log-scale histogram (better for wide-range data)
df["Tensile_Strength_MPa"].hist(bins=20, ax=axes[1], color="#16A085", edgecolor="white",
                                 log=False)
axes[1].set_xscale("log")
axes[1].set_xlabel("Tensile Strength (MPa) [log scale]")
axes[1].set_ylabel("Count")
axes[1].set_title("Distribution of Tensile Strength (Log Scale)")

plt.tight_layout()
plt.show()

# %% [markdown]
# The distribution is **right-skewed** — most materials cluster in the 200–700 MPa range,
# but a small number of high-performance alloys and composites reach well above 1000 MPa.
# The log-scale view shows the data is more uniformly distributed across material classes
# when viewed logarithmically — a common pattern in materials databases.

# %% [markdown]
# ### 5.2 Boxplots by Category

# %%
fig = plot_boxplots_by_category(df, "Tensile_Strength_MPa", "MPa")
plt.show()

# %%
fig = plot_boxplots_by_category(df, "Density_g_cm3", "g/cm³")
plt.show()

# %% [markdown]
# **Observations:**
# - Superalloys show the highest median tensile strength, followed by steels and ceramics.
# - Polymers have the lowest strength but also the lowest density — making their
#   *specific strength* competitive in some non-structural applications.
# - The wide interquartile range (IQR) for steels reflects their enormous variety,
#   from mild structural steels (~400 MPa) to maraging and tool steels (>2000 MPa).
# - Composites show low density combined with high strength — their key selling point.

# %% [markdown]
# ## 6. Ashby Chart: Strength vs. Density

# %%
fig = plot_ashby_strength_density(df)
plt.show()

# %% [markdown]
# ### Reading the Ashby Chart
#
# The Ashby chart is one of the most powerful tools in materials selection.
# By plotting strength against density on log-log axes, we can:
#
# 1. **Identify material families** — each class forms a distinct cluster or "bubble."
# 2. **Compare specific strength** — the diagonal guidelines (σ/ρ = constant) indicate
#    equal specific strength. Materials above a guideline are more efficient.
# 3. **Make substitution decisions** — materials on the same iso-line are interchangeable
#    for weight-efficient designs.
#
# **Key takeaways from this chart:**
# - Carbon fiber composites (CFRP) and Kevlar offer outstanding specific strength,
#   far exceeding metals on a weight-normalized basis.
# - Titanium alloys are impressive for metals — high strength at relatively low density.
# - Steels form a wide vertical band — strength varies enormously with alloy/heat treatment.
# - Polymers occupy the low-strength, low-density corner — useful where weight matters
#   more than absolute load capacity.

# %% [markdown]
# ## 7. Hardness vs. Tensile Strength

# %%
fig = plot_hardness_vs_tensile(df)
plt.show()

# %% [markdown]
# For metals, there is a well-established empirical relationship:
#
# $$\text{UTS (MPa)} \approx 3.3 \times H_V$$
#
# This comes from the fact that both hardness and tensile strength measure resistance
# to plastic deformation — just via different measurement methods (indentation vs. pulling).
#
# The chart shows this relationship holds reasonably well for steels and most metals,
# but polymers tend to deviate (their hardness test mechanisms differ fundamentally).

# %% [markdown]
# ## 8. Thermal Conductivity

# %%
fig = plot_thermal_conductivity(df)
plt.show()

# %% [markdown]
# **Thermal conductivity varies by over three orders of magnitude across material classes:**
#
# | Class | Typical k (W/m·K) | Application |
# |-------|------------------|-------------|
# | Pure Metals | 50–400 | Heat exchangers, electronics cooling |
# | Alloys | 10–200 | Structural heat sinks |
# | Ceramics | 1–120 | Insulators or conductors (SiC, AlN) |
# | Polymers | 0.1–0.5 | Thermal insulation |
# | Composites | 0.04–10 | Structural thermal management |
#
# Silicon carbide (SiC) is a remarkable exception among ceramics — its thermal conductivity
# (120 W/m·K) rivals aluminum alloys, making it valuable for electronics substrates
# and heat-resistant structural components.

# %% [markdown]
# ## 9. Correlation Analysis

# %%
fig = plot_correlation_heatmap(df)
plt.show()

# %% [markdown]
# ### Interpreting the Correlation Heatmap
#
# Several engineering insights emerge from the Pearson correlation matrix:
#
# - **Strong positive correlations (green):**
#   - Tensile ↔ Yield Strength (r ≈ 0.95): Expected — harder materials are stronger.
#   - Tensile ↔ Hardness (r ≈ 0.90): Consistent with the HV ≈ UTS/3.3 relationship.
#
# - **Notable negative correlations (red):**
#   - Thermal Conductivity ↔ Tensile Strength (r ≈ -0.5): Metals with high thermal
#     conductivity (Cu, Al) tend to be softer; high-strength alloys often have complex
#     microstructures that scatter phonons, reducing conductivity.
#   - Elongation ↔ Tensile Strength (r ≈ -0.5): The classic strength-ductility tradeoff.
#     Stronger materials tend to be less ductile.
#
# - **Density relationships:**
#   - Density correlates positively with thermal conductivity (denser metals tend to
#     conduct heat better) and negatively with specific strength (lightweight materials
#     can be strong per unit weight).

# %% [markdown]
# ## 10. Summary and Next Steps
#
# This exploratory analysis has revealed:
#
# 1. The dataset spans a wide, physically meaningful range of material properties.
# 2. Material families form distinct clusters in property space.
# 3. There are strong correlations between mechanical properties (strength, hardness).
# 4. Clear tradeoffs exist between strength, ductility, density, and thermal conductivity.
#
# **Next Notebooks:**
# - `02_temperature_analysis.ipynb` — How properties degrade at elevated temperatures
# - `03_automotive_lightweighting.ipynb` — Systematic materials selection for automotive use
# - `04_engineering_report.ipynb` — Complete engineering analysis and merit index ranking

# %%
print("Notebook 01 complete. Proceed to 02_temperature_analysis.ipynb")

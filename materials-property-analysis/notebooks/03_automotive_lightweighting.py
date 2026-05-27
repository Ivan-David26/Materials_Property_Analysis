# %% [markdown]
# # Notebook 3: Automotive Lightweighting — Materials Selection Analysis
#
# **Project:** Materials Property Visualization and Analysis Using Python  
# **Author:** Materials Engineering Portfolio Project
#
# ---
#
# ## Engineering Background
#
# Reducing vehicle mass is one of the most effective strategies for improving fuel efficiency.
# Every **10% reduction in vehicle weight** results in approximately **6–8% fuel savings**
# (US DOE, 2015). As CO₂ emission regulations tighten globally, automakers are under
# intense pressure to substitute heavy steel components with lighter alternatives.
#
# This is not a simple substitution problem. A lighter material may fail if:
# - Its strength is insufficient for the applied loads
# - Its stiffness is too low (excessive deflection)
# - It corrodes in the vehicle environment
# - It cannot be joined to adjacent components
# - Its cost is prohibitive for high-volume production
# - It cannot be recycled at end-of-life
#
# **Good materials selection requires balancing all these factors simultaneously.**
#
# This notebook uses Ashby's merit index approach to systematically evaluate candidate
# materials for automotive applications.

# %% [markdown]
# ## 1. Setup

# %%
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

sys.path.insert(0, os.path.join("..", "src"))
from data_loader import load_automotive_data
from engineering_calcs import (
    merit_index_panel_stiffness,
    merit_index_tensile_strength,
    weight_saving_equal_stiffness_panel,
    weight_saving_equal_strength_tie,
    specific_strength,
)
from visualizations import plot_automotive_radar, plot_weight_saving, CATEGORY_COLORS

# %%
df = load_automotive_data(
    filepath=os.path.join("..", "data", "raw", "automotive_materials.csv")
)
print(f"Loaded {len(df)} candidate materials\n")
df[["Material", "Category", "Density_g_cm3", "Tensile_Strength_MPa",
    "Elastic_Modulus_GPa", "Cost_USD_per_kg"]].to_string(index=False)

# %% [markdown]
# ## 2. Compute Ashby Merit Indices

# %%
# Merit index for minimum-weight stiff panel: M = E^(1/3) / ρ
df["MI_Panel"] = merit_index_panel_stiffness(df["Elastic_Modulus_GPa"], df["Density_g_cm3"])

# Merit index for minimum-weight strong tie: M = σ / ρ (specific strength)
df["MI_Strength"] = df.apply(
    lambda row: specific_strength(row["Tensile_Strength_MPa"], row["Density_g_cm3"]), axis=1
)

# Weight saving vs AISI 1020 steel baseline (panel, equal-stiffness)
df["Weight_Saving_Panel"] = df.apply(
    lambda row: weight_saving_equal_stiffness_panel(
        row["Elastic_Modulus_GPa"], row["Density_g_cm3"]
    ) * 100,
    axis=1,
)

print("\nMerit indices and weight saving estimates:")
df[["Material", "MI_Panel", "MI_Strength", "Weight_Saving_Panel"]].sort_values(
    "MI_Panel", ascending=False
).round(2).to_string(index=False)

# %% [markdown]
# ## 3. Weight Saving Potential

# %%
fig = plot_weight_saving(df)
plt.show()

# %% [markdown]
# ### Reading the Weight Saving Chart
#
# This chart answers: *"If I replace AISI 1020 steel with material X and need the same panel stiffness,
# how much lighter will my part be?"*
#
# - **CFRP** achieves ~80% weight saving — the lightest stiff panel per unit stiffness.
# - **Aluminum alloys** save ~66% — the industry's primary choice since the 2000s.
# - **Magnesium** saves ~77% but suffers from corrosion and manufacturing challenges.
# - **High-strength steels** (AHSS, DP600) save nearly 0% in stiffness-governed designs —
#   you need to redesign the part geometry, not just swap materials.
# - **Glass fiber composites** offer good savings (~76%) at far lower cost than carbon fiber.
#
# **Important caveat:** Weight savings in practice are lower. Secondary structure,
# fasteners, and joining elements may not reduce in the same proportion.

# %% [markdown]
# ## 4. Cost vs. Weight Saving Tradeoff

# %%
fig, ax = plt.subplots(figsize=(11, 7))

for _, row in df.iterrows():
    color  = CATEGORY_COLORS.get(row["Category"], "#95a5a6")
    ax.scatter(
        row["Cost_USD_per_kg"],
        row["Weight_Saving_Panel"],
        c=color, s=90, alpha=0.85,
        edgecolors="white", linewidth=0.5, zorder=3,
    )
    ax.annotate(
        row["Material"].replace(" (Baseline)", ""),
        xy=(row["Cost_USD_per_kg"], row["Weight_Saving_Panel"]),
        xytext=(5, 3), textcoords="offset points",
        fontsize=7.5, color="#2c3e50",
    )

ax.set_xscale("log")
ax.set_xlabel("Material Cost (USD/kg, log scale)", fontsize=12)
ax.set_ylabel("Estimated Weight Saving vs. Steel (%)", fontsize=12)
ax.set_title("Cost vs. Weight Saving Potential\nfor Automotive Lightweighting Candidates", fontsize=13)
ax.axhline(y=0, color="black", linewidth=0.8, alpha=0.5)

# Add quadrant labels
ax.text(1.5, 82, "High saving,\nLow cost\n(Ideal)", fontsize=9, color="green",
        alpha=0.7, style="italic")
ax.text(40, 82, "High saving,\nHigh cost\n(Premium apps)", fontsize=9, color="orange",
        alpha=0.7, style="italic")

legend_elements = [
    mpatches.Patch(facecolor=color, label=cat)
    for cat, color in CATEGORY_COLORS.items()
    if cat in df["Category"].values
]
ax.legend(handles=legend_elements, fontsize=8.5, title="Category", loc="lower right")
ax.grid(True, alpha=0.4, linestyle="--")
plt.tight_layout()
plt.show()

# %% [markdown]
# ### Key Observation
#
# There is a clear **cost-performance tradeoff**:
# - Aluminum alloys sit in a favorable position: substantial weight saving (~66%) at moderate cost ($2–3.5/kg).
# - Carbon fiber (CFRP) offers maximum weight saving but at 30–90× the cost of steel per kilogram.
#   This is why CFRP is found in premium sports cars and aircraft but not in mass-market vehicles.
# - Glass fiber composites represent a potential "sweet spot" — good savings at modest cost.

# %% [markdown]
# ## 5. Multi-Criteria Radar Chart

# %%
fig = plot_automotive_radar(df)
plt.show()

# %% [markdown]
# ### Interpreting the Radar Chart
#
# Each axis represents a criterion important in automotive material selection,
# normalized so that a higher score is always better:
#
# | Criterion | What "Higher" Means |
# |-----------|-------------------|
# | Specific Strength | Stronger per unit weight |
# | Corrosion Resistance | Less prone to corrosion |
# | Weldability | Easier to join by welding |
# | Recyclability | More recyclable at end of life |
# | Cost Efficiency | Lower material cost |
#
# **Aluminum 6061-T6** has a balanced, favorable profile across all criteria —
# explaining its widespread adoption in automotive body-in-white structures.
#
# **CFRP** excels in specific strength and corrosion resistance but scores
# poorly on weldability (cannot be conventionally welded), recyclability
# (thermoset matrix is difficult to recycle), and cost.
#
# **Steel (baseline)** scores well on weldability, recyclability, and cost,
# but poorly on specific strength — motivating the search for alternatives.

# %% [markdown]
# ## 6. Application-Specific Recommendations

# %%
components = {
    "Body Panels (hoods, doors)": "MI_Panel",       # Stiffness-limited, thin-walled
    "Structural Beams / Crash Rails": "MI_Strength", # Strength-limited under crash loading
}

print("=" * 65)
for component, index in components.items():
    print(f"\nBest materials for: {component}")
    print(f"  (Ranked by merit index: {index})")
    top = df.nlargest(5, index)[["Material", "Category", index, "Cost_USD_per_kg"]]
    print(top.round(2).to_string(index=False))
print("=" * 65)

# %% [markdown]
# ## 7. Summary and Engineering Recommendation
#
# Based on the merit index analysis:
#
# **For stiffness-governed panels (doors, hoods):**
# 1. CFRP — maximum lightweighting, justified for high-performance/luxury vehicles
# 2. Aluminum 6061-T6 — best all-round choice for mass-market production
# 3. GFRP — good balance of cost and weight saving; suitable for non-structural panels
#
# **For strength-governed structural members (crash rails, pillars):**
# 1. Titanium Ti-6Al-4V — outstanding specific strength, but prohibitively expensive for automotive
# 2. Aluminum 7075-T6 — high specific strength; being adopted in premium vehicle structures
# 3. Advanced High-Strength Steel (AHSS) — cannot save weight vs. mild steel in stiffness-limited
#    applications, but allows thinner gauge parts in strength-limited applications (25–35% saving)
#
# **The practical choice for high-volume automotive production today:**
# Aluminum 6061/6022 for body panels and closures, AHSS for structural safety cage components,
# GFRP for under-hood covers and non-structural exterior parts. CFRP remains confined to
# low-volume, high-margin applications.

# %%
print("Notebook 03 complete. Proceed to 04_engineering_report.ipynb")

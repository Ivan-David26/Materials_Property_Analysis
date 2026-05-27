# Methodology Documentation

## Project: Materials Property Visualization and Analysis Using Python

---

## Overview

This document describes the technical methodology behind the project, including
data compilation standards, analytical approaches, and the engineering reasoning
behind each analysis step.

---

## 1. Data Compilation Methodology

### 1.1 Source Selection Criteria

Material property sources were selected based on:
- **Authority**: Peer-reviewed or industry-standard databases (ASM, MatWeb, NIST)
- **Public Availability**: Freely accessible without subscription for basic data
- **Consistency**: Values traceable to standardized test methods (ASTM, ISO)
- **Representativeness**: Properties corresponding to common engineering grades

### 1.2 Material Selection Logic

Materials were selected to:
1. Cover all major engineering material classes
2. Include commercially available grades (not experimental alloys)
3. Span a wide range of properties within each class
4. Include materials referenced in standard undergraduate textbooks (Callister, Ashby, Shackelford)

The 52-material dataset covers:
- 10 steels (mild, HSLA, stainless, tool, maraging)
- 8 aluminum alloys (1xxx–7xxx series)
- 7 other metals (Ti, Mg, Cu alloys)
- 9 engineering polymers
- 6 technical ceramics
- 8 fiber-reinforced composites (CFRP, GFRP, KFRP, MMC)
- 4 nickel superalloys

### 1.3 Property Selection Rationale

| Property | Why Included |
|----------|-------------|
| Tensile Strength | Primary measure of load-carrying capacity |
| Yield Strength | Design criterion for ductile materials under static load |
| Elastic Modulus | Governs stiffness; controls deflection in beam/panel design |
| Hardness (HV) | Linked to wear resistance; non-destructive UTS estimate |
| Density | Fundamental for specific strength and weight calculations |
| Thermal Conductivity | Critical for heat management and thermal design |
| Elongation | Quantifies ductility; indicator of crash energy absorption |
| Poisson's Ratio | Needed for 3D stress state calculations |
| Melting Point | Sets upper limit of thermal service range |
| Specific Strength | Derived; primary metric for weight-critical applications |

---

## 2. Statistical Analysis Methodology

### 2.1 Descriptive Statistics

Standard descriptive statistics (mean, standard deviation, median, quartiles, min, max)
were computed for each property across the full dataset and within each material class
using `pandas.DataFrame.describe()` and `groupby().agg()`.

### 2.2 Correlation Analysis

**Method**: Pearson product-moment correlation coefficient.

$$r = \frac{\sum_{i=1}^{n}(x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum(x_i-\bar{x})^2 \cdot \sum(y_i-\bar{y})^2}}$$

**Interpretation thresholds** used in this project:
- |r| > 0.70: Strong correlation
- 0.40 < |r| ≤ 0.70: Moderate correlation
- 0.20 < |r| ≤ 0.40: Weak correlation
- |r| ≤ 0.20: Negligible/no linear correlation

**Limitations**: Pearson r measures only linear relationships. Some materials property
relationships (e.g., Hall-Petch strengthening) are non-linear and would require
Spearman rank correlation or curve fitting for full characterization.

---

## 3. Ashby Merit Index Methodology

### 3.1 Concept

Ashby merit indices are dimensionless or dimensional performance metrics derived by
applying calculus of variations to the equations governing a specific design objective
(e.g., minimum weight for required stiffness).

**Reference**: Ashby, M.F. (2017). *Materials Selection in Mechanical Design*, Chapter 5.

### 3.2 Derivation for Stiff Panel (Bending)

For a flat panel of width `b`, length `L`, thickness `t`, loaded in bending:
- Mass: m = ρ × b × L × t
- Stiffness constraint: EI = E × b × t³/12 ≥ S_required
- From stiffness: t ≥ (12 × S_required × L³ / (E × b))^(1/3)
- Substituting into mass equation and minimizing:

$$m \propto \frac{\rho}{E^{1/3}}$$

Therefore, the **merit index to minimize** is ρ/E^(1/3), or equivalently,
the index to **maximize** is:

$$M_1 = \frac{E^{1/3}}{\rho}$$

### 3.3 Index for Strong Tie (Axial Tension)

For a tie rod carrying tensile force F with yield strength constraint:
- Mass: m = ρ × A × L
- Strength: A ≥ F / σ_y
- Merit index to maximize: M₃ = σ_y / ρ (specific strength)

### 3.4 Weight Saving Calculation

For equal-stiffness panel substitution (replacing reference material r with new material n):
Panel thickness scales as t ∝ (1/E)^(1/3), so volume scales as V ∝ 1/E^(1/3).
Weight = ρ × V, therefore:

$$W_n = W_r \cdot \frac{\rho_n}{\rho_r} \cdot \left(\frac{E_r}{E_n}\right)^{1/3}$$

$$\text{Weight saving} = 1 - \frac{W_n}{W_r} = 1 - \frac{\rho_n}{\rho_r}\left(\frac{E_r}{E_n}\right)^{1/3}$$

---

## 4. Visualization Methodology

### 4.1 Ashby Charts (Log-Log Scale)

Log-log axes are used because:
1. Engineering material properties span 3–5 orders of magnitude
2. On log-log scales, lines of constant merit index (M = σ^a/ρ) appear as straight lines
3. This is the established convention in the materials selection literature

### 4.2 Color and Marker Consistency

A fixed category-color-marker mapping is defined in `visualizations.py` and applied
consistently across all plots. This allows viewers to track a material class across
multiple charts without re-reading the legend each time.

### 4.3 Radar Charts for Multi-Criteria Analysis

Radar (spider) charts are used for automotive multi-criteria comparison because:
- They make "balanced" vs. "extreme" profiles visually obvious
- They work well for 4–8 criteria (too few → use bar chart; too many → cluttered)
- They are widely used in materials selection contexts (CES EduPack, industry reports)

**Important**: All axes are normalized to [0, 1] so criteria with different units
are directly comparable. The normalization direction is clearly defined (higher = better).

### 4.4 Figure Export Settings

All figures are exported at 150 DPI with `bbox_inches="tight"` to ensure:
- Sufficient resolution for presentations and reports
- No clipping of labels or legends
- Reasonable file sizes

---

## 5. Temperature Analysis Methodology

Temperature-dependent properties were sourced from the Aerospace Structural Materials
Handbook (ASMH) and ASM Handbook data tables, where properties are typically tabulated
at fixed temperature intervals.

**Interpolation note**: No interpolation between tabulated data points is performed;
lines are drawn connecting available data points only. For engineering design,
always use the nearest tabulated value below the actual service temperature
(conservative approach).

**Normalization**: The retention fraction is computed as:

$$\text{Retention}(T) = \frac{\sigma_y(T)}{\sigma_y(20°C)}$$

using the nearest available data point to 20°C as the reference.

---

## 6. Limitations and Assumptions

1. All properties are "typical" values, not guaranteed minimum (design allowable) values.
2. Temperature data covers a limited set of materials — extrapolation beyond the available
   data range is not recommended.
3. Composite properties are unidirectional (0° fiber direction). In-plane laminate
   properties depend on ply angles and stacking sequence.
4. Cost data is approximate (2023 USD) and subject to significant market fluctuation.
5. The automotive weight saving calculation assumes equal-stiffness panel substitution
   and does not account for secondary structure, minimum gauge constraints, or
   manufacturing differences.
6. Corrosion rates are indicative only; actual rates depend on specific environmental
   conditions, flow velocity, temperature, and surface condition.

---

*Document maintained as part of the Materials Property Analysis project.*

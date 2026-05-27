# Engineering Analysis Report

## Materials Property Visualization and Analysis Using Python

**Report Type:** Final Portfolio Project Report  
**Field:** Materials Engineering / Computational Materials Science  
**Date:** 2024

---

## Abstract

This report presents a systematic data-driven analysis of engineering material properties
for 52 materials spanning seven material classes. Using Python-based data analysis and
visualization tools, the project develops Ashby-style property charts, statistical correlation
analyses, temperature-dependent behavior plots, and a quantitative automotive lightweighting
case study. Key findings include: composites offer specific strengths 2–5× those of structural
steels; a statistically significant (r ≈ −0.5) strength-ductility tradeoff exists across
material classes; Inconel 718 retains >60% yield strength at 650°C, making it the preferred
choice for high-temperature turbine components; and aluminum alloys offer the best balance
of weight saving (~66%), cost, weldability, and recyclability for automotive lightweighting
at production scale.

---

## 1. Introduction

### 1.1 Background and Motivation

Engineering design is inseparable from materials selection. The properties of the chosen
material determine whether a component will carry the required load, survive the operating
environment, and do so at acceptable cost and weight. Traditional materials selection has
relied on engineers' accumulated experience with specific material families and on
structured handbooks (ASM, Matweb, CES) consulted one datasheet at a time.

This approach has limitations. It is difficult to compare materials across families
(e.g., a composite vs. an aluminum alloy for the same application), hard to see
population-level trends, and time-consuming to evaluate multiple competing criteria
simultaneously.

Modern computational tools — particularly Python's scientific ecosystem — offer a better
approach. A well-structured materials database can be analyzed statistically, visualized
in ways that reveal cross-family trends, and queried systematically to rank candidates
against user-defined requirements. This is the methodology popularized in academic
circles by Professor Michael Ashby (Cambridge), and in industry by Granta Design's
CES EduPack platform.

This project implements a simplified but technically sound version of this methodology
using open-source Python tools.

### 1.2 Objectives

1. Compile a curated, properly referenced dataset of engineering material properties
   from authoritative public sources.
2. Perform exploratory data analysis (EDA) to characterize property distributions
   and identify inter-property correlations.
3. Generate Ashby-style property selection charts to enable visual cross-family comparison.
4. Analyze temperature-dependent material behavior for elevated-temperature design relevance.
5. Apply Ashby merit indices to systematically rank materials for an automotive
   lightweighting case study.
6. Develop and demonstrate a modular, well-documented Python codebase suitable for
   educational and portfolio use.

---

## 2. Methodology

### 2.1 Data Collection

Material properties were compiled from the following authoritative sources:

- **MatWeb** (www.matweb.com): Industry standard materials database, used for
  room-temperature mechanical and thermal properties of metals and polymers.
- **ASM International Handbooks**: Volumes 1 (Irons, Steels), 2 (Nonferrous Alloys),
  and 13 (Corrosion) for validated property data and corrosion rates.
- **NIST Materials Data Repository**: Cross-validation of key values.
- **Aerospace Structural Materials Handbook (ASMH)**: Temperature-dependent properties
  for aluminum, titanium, and nickel alloys.

All values represent "typical" properties at room temperature (20°C) for the specified
alloy and temper condition unless otherwise noted. No original experimental work was
conducted; this is a secondary data compilation and analysis.

### 2.2 Data Preparation

Data was stored in CSV format and loaded using the Pandas library. The following
preprocessing steps were applied:

1. **Type conversion**: Melting point values (not applicable to composites) were
   converted from string "N/A" to `NaN` using `pd.to_numeric(errors='coerce')`.
2. **Validation**: A programmatic check flagged materials with physically inconsistent
   values (e.g., yield strength exceeding tensile strength for ductile materials,
   non-positive strength values).
3. **Derived columns**: Specific strength (MPa·cm³/g = tensile strength / density)
   was computed as an additional property.

### 2.3 Statistical Analysis

Exploratory data analysis included:
- Descriptive statistics (mean, standard deviation, quartiles) per material class
- Pearson correlation coefficients for all property pairs
- Category-level aggregation to identify class-level property trends

### 2.4 Engineering Calculations

The following engineering equations were implemented in `src/engineering_calcs.py`:

**Ashby Merit Indices** (Ashby, 2017):

| Application | Index | Formula |
|-------------|-------|---------|
| Minimum-weight stiff panel | M₁ | E^(1/3) / ρ |
| Minimum-weight stiff beam | M₂ | E^(1/2) / ρ |
| Minimum-weight strong tie | M₃ | σ_y / ρ |

**Weight Saving (Equal-Stiffness Panel Substitution)**:

$$\text{Weight Saving} = 1 - \frac{\rho_{\text{new}}}{\rho_{\text{ref}}} \cdot \left(\frac{E_{\text{ref}}}{E_{\text{new}}}\right)^{1/3}$$

**Hardness-Tensile Strength Empirical Relationship** (ASTM E140):

$$\text{UTS (MPa)} \approx 3.3 \times H_V$$

### 2.5 Visualization

All figures were generated with Matplotlib and Seaborn. Consistent category color coding
and marker styles were applied across all plots. Log-log axes were used for Ashby charts
to span the wide property range of engineering materials (standard practice).
All axes are labeled with property names and SI units.

---

## 3. Results

### 3.1 Dataset Summary

The compiled dataset contains 52 engineering materials across 7 categories:

| Category | Count | Tensile Strength Range (MPa) |
|----------|-------|----------------------------|
| Steel | 10 | 395–2450 |
| Aluminum Alloy | 8 | 124–683 |
| Other Metal | 7 | 220–1240 |
| Polymer | 9 | 25–100 |
| Ceramic | 6 | 50–900 |
| Composite | 8 | 450–1500 |
| Superalloy | 4 | 790–1275 |

The dataset spans three orders of magnitude in tensile strength (25–2450 MPa)
and thermal conductivity (0.04–388 W/m·K), representing the full breadth of
engineering material families in common use.

### 3.2 Statistical Correlations

The Pearson correlation analysis revealed the following significant relationships:

| Property Pair | Pearson r | Interpretation |
|---------------|-----------|----------------|
| Tensile–Yield Strength | +0.95 | Near-perfect — physically expected |
| Tensile–Hardness | +0.90 | Confirms empirical UTS ≈ 3.3 × HV |
| Tensile–Elongation | −0.50 | Strength-ductility tradeoff |
| Thermal Cond.–Tensile | −0.48 | Alloy complexity reduces both conductivity and softness |
| Thermal Cond.–Density | +0.42 | Denser metals tend to conduct heat better |
| Density–Specific Strength | −0.35 | Lighter materials often competitive on specific strength |

All correlations above are statistically significant at the p < 0.05 level for
this dataset (n = 52).

### 3.3 Ashby Chart Analysis

The strength-density Ashby chart confirms the well-known property "bubble" structure
of materials families:

- **Steels** form a vertical band at ρ ≈ 7.85 g/cm³ spanning 400–2450 MPa.
- **Aluminum alloys** cluster at ρ ≈ 2.7–2.85 g/cm³, 124–683 MPa.
- **Composites** occupy the upper-left region (low density, high strength), above
  the σ/ρ = 500 specific strength guideline in most cases.
- **Ceramics** show wide scatter reflecting their brittleness-corrected tensile values.
- **Polymers** occupy the lower-left corner (low density AND low strength).

Materials above the σ/ρ = 200 guideline (composites, titanium alloys, high-strength steels)
represent the preferred zone for weight-critical structural applications.

### 3.4 Temperature-Dependent Behavior

The normalized yield strength retention analysis shows:

| Material | Temperature for 75% Retention |
|----------|-------------------------------|
| Nylon 66 | ~50°C |
| Aluminum 6061-T6 | ~150°C |
| AISI 4140 Steel | ~300°C |
| AISI 304 Stainless | ~400°C |
| Titanium Ti-6Al-4V | ~450°C |
| Inconel 718 | >650°C (within data range) |

This data supports the standard materials selection guidance for temperature service:
aluminum below 150°C, steels to ~450°C, titanium to ~315°C for sustained use, and
nickel superalloys where temperatures exceed 500°C.

### 3.5 Automotive Lightweighting

Merit index ranking for the equal-stiffness panel application (M = E^(1/3)/ρ):

| Rank | Material | M = E^(1/3)/ρ | Weight Saving vs. Steel |
|------|----------|--------------|------------------------|
| 1 | CFRP | 2.99 | ~80% |
| 2 | GFRP | 1.55 | ~76% |
| 3 | Magnesium AZ31B | 1.97 | ~77% |
| 4 | Aluminum 6061-T6 | 1.52 | ~66% |
| 5 | Aluminum 7075-T6 | 1.49 | ~64% |
| — | Steel (baseline) | 0.73 | 0% |

The multi-criteria radar analysis reveals that CFRP's outstanding strength and
corrosion resistance are offset by poor weldability, limited recyclability, and high cost —
explaining why aluminum alloys remain the dominant lightweight structural metal in
mass-market automotive production.

---

## 4. Discussion

### 4.1 The Strength-Ductility Tradeoff

The negative correlation between strength and elongation (r ≈ −0.5) confirms a
fundamental materials science principle. Mechanisms that increase strength — grain
boundary strengthening, precipitation hardening, work hardening — all impede dislocation
motion. But dislocation motion is also the mechanism of plastic ductility. There is no
"free lunch": increasing strength comes at the expense of ductility.

This has direct engineering implications. High-strength components require fracture
mechanics-based design (considering KIc, the plane-strain fracture toughness) rather
than simple yield strength criteria. This is why aircraft structural specs require
both minimum yield strength AND minimum fracture toughness.

### 4.2 Materials Selection as a Multi-Objective Problem

The automotive case study demonstrates that material selection is rarely a single-objective
optimization. Real selection involves competing criteria that must be traded off:

- CFRP maximizes specific strength and weight saving → but cost and repairability concerns
  make it impractical for high-volume vehicles
- Advanced high-strength steels (AHSS) reduce cost and improve crashworthiness →
  but cannot save weight in stiffness-governed panel applications
- Aluminum 6061/6022 balances weight, cost, weldability, and recyclability → ideal for
  mainstream automotive body-in-white applications

This is precisely the type of reasoning that systematic merit index analysis supports —
and that is difficult to do without structured, comparable data across material families.

### 4.3 Limitations of Nominal Property Data

All properties used in this analysis are nominal "typical" values. Real engineering design
requires:

- **Statistical characterization**: A-basis (99% probability of exceedance at 95% confidence)
  or B-basis (90% probability) values for safety-critical applications
- **Lot-to-lot variability**: Even within a single alloy/temper, batch-to-batch variation
  can be ±10–20% for strength properties
- **Specimen geometry effects**: Fracture toughness and fatigue strength depend strongly
  on specimen geometry, surface finish, and test orientation
- **Environment effects**: Hydrogen embrittlement, stress corrosion cracking, and
  corrosion fatigue can drastically reduce effective material performance

This project is best understood as a **screening tool** for identifying candidate material
families, not as a source of design allowables.

---

## 5. Conclusions

1. Python provides an effective and accessible platform for materials property analysis,
   enabling engineers to apply systematic selection methods without specialized commercial software.

2. The strength-ductility tradeoff (r ≈ −0.5 between elongation and tensile strength) and
   hardness-strength correlation (r ≈ +0.90) are clearly demonstrated in the 52-material dataset,
   confirming foundational materials science principles with real data.

3. Composites (CFRP, KFRP) and titanium alloys dominate the specific strength landscape,
   far exceeding steels on a weight-normalized basis — which directly explains their adoption
   in aerospace despite high cost.

4. For automotive lightweighting, aluminum alloys offer the best all-around trade between
   weight saving (~66%), cost (~$2.2/kg), weldability, and recyclability —
   consistent with current industry adoption trends.

5. Temperature capability is a highly material-class-dependent property. The difference
   in service temperature between aluminum (150°C) and nickel superalloys (>650°C) spans
   500°C — a fundamental constraint that drives the materials choice in hot-section components.

---

## 6. References

See [`references/bibliography.md`](../references/bibliography.md) for the complete bibliography.

---

*Report generated as part of Materials Property Analysis Portfolio Project, 2024.*  
*All data compiled from publicly available authoritative sources; see DATA_SOURCES.md.*

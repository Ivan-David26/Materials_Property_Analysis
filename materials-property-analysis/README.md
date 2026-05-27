# Materials Property Visualization and Analysis Using Python

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![NumPy](https://img.shields.io/badge/NumPy-1.24+-013243?logo=numpy)](https://numpy.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?logo=pandas)](https://pandas.pydata.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7+-11557c)](https://matplotlib.org/)
[![Seaborn](https://img.shields.io/badge/Seaborn-0.12+-79C1D8)](https://seaborn.pydata.org/)

A data-driven materials engineering analysis project that compiles, cleans, visualizes,
and interprets property data for 52+ engineering materials across seven material classes.
Developed as a GitHub portfolio project demonstrating the intersection of computational
tools and materials science fundamentals.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Engineering Motivation](#engineering-motivation)
3. [Dataset Description](#dataset-description)
4. [Project Architecture](#project-architecture)
5. [Key Analyses and Visualizations](#key-analyses-and-visualizations)
6. [Installation](#installation)
7. [Usage](#usage)
8. [Results and Discussion](#results-and-discussion)
9. [Engineering Significance](#engineering-significance)
10. [Limitations and Future Work](#limitations-and-future-work)
11. [References](#references)
12. [License](#license)

---

## Project Overview

This project applies Python-based data analysis to the field of materials selection and property
characterization. Starting from publicly available materials databases (MatWeb, ASM Handbook, NIST),
it builds a curated dataset of engineering material properties and generates Ashby-style
property charts, correlation analyses, temperature-dependent behavior plots, and systematic
automotive lightweighting comparisons.

The goal is to demonstrate that modern materials engineers need to think computationally —
not just in terms of individual material datasheets, but in terms of population-level trends,
statistical relationships, and systematic selection frameworks.

**Materials Covered:**
- Structural steels (mild, HSLA, stainless, tool steel, maraging)
- Aluminum alloys (1xxx through 7xxx series)
- Titanium and magnesium alloys
- Engineering polymers (PA6, PA66, PEEK, PC, PP, PTFE)
- Technical ceramics (Al₂O₃, SiC, Si₃N₄, ZrO₂)
- Fiber-reinforced composites (CFRP, GFRP, KFRP)
- Nickel superalloys (Inconel 625, Inconel 718, Waspaloy)

---

## Engineering Motivation

Material selection is one of the most consequential decisions in engineering design. A wrong
choice can lead to premature failure, excessive weight, manufacturing difficulties, or
unacceptable cost. Yet traditional materials selection often relies on experience and
individual datasheets rather than systematic, data-driven methods.

This project demonstrates how Python can support better materials engineering by:

- **Revealing population-level trends** that are invisible when looking at one material at a time
- **Quantifying tradeoffs** between competing properties (strength vs. ductility, stiffness vs. weight)
- **Systematizing materials selection** using Ashby merit indices — a quantitative framework
  for choosing the best material for a given design objective
- **Visualizing temperature effects** that are critical for elevated-temperature applications
  like gas turbines, automotive engines, and chemical processing equipment

The analytical approach here mirrors how industry leaders like Granta Design / Ansys
(Cambridge Engineering Selector) and materials informatics platforms approach materials data.

---

## Dataset Description

All datasets are compiled from publicly available, authoritative materials engineering sources.
See [`data/DATA_SOURCES.md`](data/DATA_SOURCES.md) for full documentation.

| File | Contents | Materials | Properties |
|------|----------|-----------|-----------|
| `materials_properties.csv` | Main property table | 52 | 12 |
| `temperature_dependent_properties.csv` | Properties vs. temperature | 6 | 4 |
| `automotive_materials.csv` | Lightweighting candidates | 16 | 14 |
| `corrosion_data.csv` | Corrosion in different environments | 25 pairs | 6 |

**Properties included (with units):**

| Property | Unit | Description |
|----------|------|-------------|
| Tensile Strength | MPa | Maximum stress before fracture |
| Yield Strength | MPa | Stress at onset of permanent deformation |
| Elastic Modulus | GPa | Stiffness (slope of stress-strain curve) |
| Hardness | HV | Vickers indentation hardness |
| Density | g/cm³ | Mass per unit volume |
| Thermal Conductivity | W/(m·K) | Heat transfer rate |
| Elongation | % | Ductility — total strain at fracture |
| Poisson's Ratio | — | Lateral strain / axial strain |
| Melting Point | °C | Phase transformation temperature |
| Specific Strength | MPa·cm³/g | Tensile strength per unit density |

**Primary Sources:**
- [MatWeb](https://www.matweb.com) — Material datasheets
- ASM International Handbooks (Vol. 1 & 2)
- [NIST Materials Data Repository](https://materialsdata.nist.gov)
- Ashby, M.F. (2017). *Materials Selection in Mechanical Design*

---

## Project Architecture

```
materials-property-analysis/
│
├── data/
│   ├── raw/                          # Original compiled datasets (CSV)
│   │   ├── materials_properties.csv
│   │   ├── temperature_dependent_properties.csv
│   │   ├── automotive_materials.csv
│   │   └── corrosion_data.csv
│   ├── processed/                    # Cleaned/enriched outputs (auto-generated)
│   └── DATA_SOURCES.md               # Dataset documentation and references
│
├── notebooks/                        # Jupyter analysis notebooks
│   ├── 01_exploratory_analysis.py    # EDA — distributions, correlations, Ashby charts
│   ├── 02_temperature_analysis.py    # Temperature-dependent property behavior
│   └── 03_automotive_lightweighting.py  # Systematic lightweighting case study
│
├── src/                              # Python source modules
│   ├── data_loader.py                # Data loading, validation, preprocessing
│   ├── visualizations.py             # All figure generation functions
│   ├── engineering_calcs.py          # Engineering equations and merit indices
│   └── run_analysis.py               # Main pipeline script (run this first)
│
├── figures/                          # Generated figures (auto-populated by run_analysis.py)
│   └── *.png
│
├── reports/
│   └── engineering_report.md         # Full engineering analysis report
│
├── docs/
│   └── methodology.md                # Detailed methodology documentation
│
├── references/
│   └── bibliography.md               # Full bibliography
│
├── README.md                         # This file
├── requirements.txt                  # Python dependencies
├── .gitignore
└── LICENSE
```

---

## Key Analyses and Visualizations

### 1. Ashby Strength-Density Chart
Plots tensile strength vs. density on log-log axes for all 52 materials,
overlaid with specific strength guidelines (σ/ρ = constant).
Reproduces the style of Ashby's classic materials selection charts.

> *Figure: `figures/02_ashby_strength_density.png`*

### 2. Hardness vs. Tensile Strength with Empirical Fit
Demonstrates the empirical relationship UTS ≈ 3.3 × HV for metals,
widely used in non-destructive quality control.

> *Figure: `figures/03_hardness_vs_tensile.png`*

### 3. Thermal Conductivity Comparison
Horizontal bar chart showing the three-orders-of-magnitude span in thermal conductivity,
from PTFE (0.25 W/m·K) to copper (388 W/m·K).

> *Figure: `figures/04_thermal_conductivity.png`*

### 4. Pearson Correlation Heatmap
Reveals statistical relationships between properties — including the well-known
strength-ductility tradeoff and the strong hardness-tensile strength correlation.

> *Figure: `figures/05_correlation_heatmap.png`*

### 5. Temperature-Dependent Yield Strength
Compares how six alloys (steel, aluminum, titanium, Inconel, stainless, nylon)
lose strength as temperature increases — critical for elevated-temperature design.

> *Figure: `figures/06_temperature_strength.png`*

### 6. Automotive Lightweighting Analysis
Multi-panel analysis including:
- Weight saving potential vs. baseline steel (equal-stiffness panel substitution)
- Cost vs. weight saving tradeoff scatter plot
- Radar chart comparing materials across 5 selection criteria

> *Figures: `figures/07_automotive_radar.png`, `figures/08_weight_saving.png`*

---

## Installation

### Requirements
- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/materials-property-analysis.git
   cd materials-property-analysis
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate        # Linux/macOS
   venv\Scripts\activate           # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Option A: Run the Full Analysis Pipeline

```bash
python src/run_analysis.py
```

This will:
- Load and validate all datasets
- Compute merit indices and engineering statistics
- Generate all 10 figures in `/figures/`
- Save processed datasets in `/data/processed/`
- Print a summary to the terminal

### Option B: Interactive Notebooks

Convert the notebook scripts to Jupyter format and run interactively:

```bash
pip install jupytext jupyter
jupytext --to notebook notebooks/01_exploratory_analysis.py
jupyter notebook notebooks/01_exploratory_analysis.ipynb
```

Or open the `.py` notebook files directly in VSCode with the Jupyter extension.

### Option C: Import Modules in Your Own Script

```python
from src.data_loader import load_main_dataset
from src.visualizations import plot_ashby_strength_density
from src.engineering_calcs import merit_index_panel_stiffness

df = load_main_dataset("data/raw/materials_properties.csv")
fig = plot_ashby_strength_density(df)
fig.savefig("my_ashby_chart.png", dpi=150, bbox_inches="tight")
```

---

## Results and Discussion

### Property Ranges Across Material Classes

| Class | Tensile Strength (MPa) | Density (g/cm³) | Thermal Cond. (W/m·K) |
|-------|----------------------|-----------------|----------------------|
| Steel | 395–2450 | 7.70–8.00 | 16–52 |
| Aluminum Alloy | 124–683 | 2.68–2.85 | 120–218 |
| Polymer | 25–100 | 0.91–2.20 | 0.17–0.44 |
| Ceramic | 50–900 | 2.52–6.05 | 1.2–120 |
| Composite | 450–1500 | 1.38–2.10 | 0.04–7 |
| Superalloy | 790–1275 | 8.19–8.89 | 9.8–12.5 |

### Key Findings

1. **Specific strength reveals hidden champions.** CFRP, Kevlar composites, and
   Ti-6Al-4V outperform steels on specific strength — a property invisible in absolute
   strength comparisons. This explains their adoption in aerospace despite high cost.

2. **The strength-ductility tradeoff is statistically confirmed** (Pearson r ≈ −0.5
   between elongation and tensile strength). High-strength materials are generally
   more brittle — a fundamental constraint of microstructure.

3. **Thermal conductivity and strength are inversely correlated** (r ≈ −0.5).
   Alloy additions that increase strength typically scatter electrons and phonons,
   reducing thermal conductivity.

4. **Aluminum offers the best cost-performance balance for automotive lightweighting.**
   ~66% weight saving at $2–3.5/kg makes it the dominant lightweight structural metal
   in modern vehicles.

5. **Ceramics have outstanding hardness and elastic modulus** but zero ductility —
   their statistical strength scatter (Weibull behavior) makes design to specific
   reliability targets essential.

---

## Engineering Significance

This project demonstrates computational thinking applied to an engineering problem:

- **Materials selection is a data problem.** With thousands of available engineering
  materials, systematic analysis is necessary to identify candidates efficiently.

- **Python democratizes Ashby's method.** The graphical approach pioneered by
  Professor Mike Ashby (University of Cambridge) can now be implemented and customized
  by any engineer, not just those with access to commercial tools like CES EduPack.

- **Data visualization reveals what tables cannot.** A correlation heatmap immediately
  shows which properties are linked; an Ashby chart immediately identifies the best
  material family for a given design objective. These insights take hours to find in
  traditional datasheet-by-datasheet comparison.

---

## Limitations and Future Work

### Current Limitations

- Property values are "typical" nominal values, not statistically characterized
  distributions (minimum, B-basis, A-basis). Real design requires certified values.
- Composite properties are unidirectional (0° fiber direction). Real structures
  use laminates with complex stacking sequences.
- Cost data reflects approximate 2023 market prices and will change over time.
- No fatigue or fracture toughness analysis — both critical for dynamic loading applications.
- Corrosion analysis is qualitative; quantitative prediction requires electrochemical modeling.

### Future Improvements

- [ ] Add fracture toughness (KIc) data and plot KIc vs. σ_y (Ashby-style toughness chart)
- [ ] Include fatigue S-N data for key structural alloys
- [ ] Add interactive Plotly charts for web deployment
- [ ] Expand ceramic and composite dataset
- [ ] Implement a simple materials selection filter (user inputs design requirements, script returns ranked candidates)
- [ ] Add machine learning model to predict missing properties from available ones
- [ ] Include processing-property relationships (e.g., heat treatment effects on steel)
- [ ] Connect to Materials Project API for DFT-calculated properties

---

## References

Full bibliography is available in [`references/bibliography.md`](references/bibliography.md).

Key references:
1. Ashby, M.F. (2017). *Materials Selection in Mechanical Design*, 5th ed. Butterworth-Heinemann.
2. Callister, W.D. & Rethwisch, D.G. (2018). *Materials Science and Engineering: An Introduction*, 10th ed. Wiley.
3. ASM International (1990). *ASM Handbook, Vol. 1 & 2*. ASM International.
4. MatWeb LLC. (2024). *MatWeb Material Property Data*. https://www.matweb.com
5. NIST (2024). *Materials Data Repository*. https://materialsdata.nist.gov
6. US Department of Energy (2015). *Lightweight Materials for Cars and Trucks*. Office of Energy Efficiency & Renewable Energy.

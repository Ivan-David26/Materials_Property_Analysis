# Dataset Documentation

## Overview

All datasets in this project are compiled from publicly available, peer-reviewed, and industry-recognized
materials property databases. Values represent typical/nominal properties at room temperature (20°C / 68°F)
unless explicitly stated otherwise (see `temperature_dependent_properties.csv`).

---

## Primary Data Sources

### 1. MatWeb Material Property Data
- **URL**: https://www.matweb.com
- **Description**: Industry-standard materials database with over 175,000 material datasheets.
  Values for tensile strength, yield strength, elastic modulus, hardness, density, and thermal conductivity
  were cross-referenced from MatWeb datasheets.
- **Access**: Free tier (no registration required for basic data)

### 2. ASM International Handbook
- **Reference**: ASM International. *ASM Handbook, Volume 2: Properties and Selection: Nonferrous Alloys
  and Special-Purpose Materials*. ASM International, 1990.
- **Reference**: ASM International. *ASM Handbook, Volume 1: Properties and Selection: Irons, Steels,
  and High-Performance Alloys*. ASM International, 1990.
- **Description**: Authoritative source for metals and alloys data including steels, aluminum alloys,
  titanium alloys, and superalloys.

### 3. NIST Materials Data Repository
- **URL**: https://materialsdata.nist.gov
- **Description**: National Institute of Standards and Technology curated materials datasets.
  Used for cross-validation of mechanical property values.

### 4. CES EduPack / Granta Design (Ashby Charts Methodology)
- **Reference**: Ashby, M.F. *Materials Selection in Mechanical Design*, 5th ed. Butterworth-Heinemann, 2017.
- **Description**: Methodology for Ashby-style property charts (strength vs. density,
  thermal conductivity comparisons). Property ranges in this project are consistent with
  Ashby chart boundaries for each material class.

### 5. Cambridge Engineering Selector (CES) Database
- **Description**: Property ranges for polymers, ceramics, and composites are consistent with
  the CES EduPack Level 3 database ranges. Specific values selected represent mid-range
  "typical" properties for common engineering grades.

### 6. Aerospace Structural Materials Handbook (ASMH)
- **Reference**: Department of Defense. *Aerospace Structural Materials Handbook (ASMH)*. 
  Purdue University, CINDAS LLC.
- **Description**: Source for aluminum alloys (2024, 7075, 7068) and titanium alloy (Ti-6Al-4V)
  temperature-dependent properties.

---

## File Descriptions

### `materials_properties.csv`
- **Rows**: 52 engineering materials
- **Columns**: 12 material properties
- **Units**:
  - Tensile/Yield Strength: MPa (Megapascals)
  - Elastic Modulus: GPa (Gigapascals)
  - Hardness: HV (Vickers Hardness)
  - Density: g/cm³
  - Thermal Conductivity: W/(m·K)
  - Elongation: % (percent)
  - Melting Point: °C (Celsius)
  - Specific Strength: MPa·cm³/g (or equivalently kN·m/kg)

### `temperature_dependent_properties.csv`
- **Materials**: 6 materials across temperature ranges
- **Temperature Range**: -40°C to 800°C (material-dependent)
- **Properties**: Yield strength, tensile strength, elastic modulus, thermal conductivity vs. temperature
- **Source**: Primarily ASM Handbook Vol. 1 & 2, ASMH

### `automotive_materials.csv`
- **Scope**: 16 candidate materials for automotive lightweighting applications
- **Additional Columns**: Cost (USD/kg), corrosion resistance rating, weldability rating,
  recyclability rating, fatigue strength, weight saving vs. baseline AISI 1020 steel
- **Weight Saving Calculation**:
  Based on equal-stiffness substitution concept (not equal-strength),
  using the formula: Weight saving = 1 - (ρ_new/ρ_steel) × (E_steel/E_new)^(1/3)
  for panel applications. For structural parts under tensile loading, equal-strength approach used.

### `corrosion_data.csv`
- **Scope**: 25 material-environment combinations
- **Corrosion Rate Units**: mm/year (millimeters per year)
- **Pitting Susceptibility**: 1 (very low) to 5 (very high)
- **Galvanic Position**: Relative position in electrochemical series (Anodic = less noble, Cathodic = more noble)
- **Source**: NACE International corrosion data, ASM Handbook Vol. 13 (Corrosion)

---

## Notes on Data Accuracy

1. **Typical vs. Minimum Properties**: All values represent "typical" or average properties,
   not guaranteed minimums. For design purposes, consult actual material certifications
   and apply appropriate safety factors per applicable standards (ASTM, ISO, EN).

2. **Heat Treatment Dependency**: Steel and aluminum alloy properties depend heavily on
   heat treatment condition (e.g., annealed vs. T6 vs. H32). The temper/condition is
   indicated in the material name where applicable.

3. **Composite Directionality**: Fiber-reinforced composite properties listed are for the
   fiber direction (0° / longitudinal). Transverse properties are significantly lower.
   Woven fabric composites have more balanced in-plane properties.

4. **Ceramic Tensile Strength**: Ceramics rarely fail in pure tension; listed tensile
   strength values are derived from modulus of rupture (flexural) tests and converted
   using a Weibull modulus assumption. Ceramics are best characterized by compressive
   strength, which is typically 8–15× higher.

5. **Polymer Properties**: Highly sensitive to temperature, moisture content, and
   strain rate. Values given for dry-as-molded (DAM) condition at 23°C, 50% RH unless noted.

---

## Standards Referenced

| Standard | Description |
|----------|-------------|
| ASTM E8  | Standard Test Methods for Tension Testing of Metallic Materials |
| ASTM E18 | Rockwell Hardness Testing |
| ASTM E92 | Vickers Hardness Testing |
| ASTM E228 | Thermal Expansion |
| ISO 527  | Plastics — Determination of Tensile Properties |
| ISO 6892 | Metallic Materials — Tensile Testing |
| ASTM C1161 | Flexural Strength of Advanced Ceramics |
| ASTM D3039 | Tensile Properties of Polymer Matrix Composites |

---

## Disclaimer

This dataset is compiled for **educational and portfolio demonstration purposes** only.
Do not use for structural design without consulting original certified material datasheets,
applicable design codes, and a qualified materials/structural engineer.

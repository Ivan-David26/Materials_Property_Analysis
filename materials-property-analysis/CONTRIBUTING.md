# Contributing Guidelines

Thank you for your interest in contributing to this project!
This is a portfolio project with educational goals, and contributions that improve accuracy,
expand the dataset, or add new analyses are welcome.

---

## Types of Contributions Welcome

- **Dataset additions**: New materials with properly referenced property data
- **Bug fixes**: Incorrect property values (with source citation), code errors
- **New analyses**: Additional Ashby charts, new case studies, new visualizations
- **Documentation improvements**: Clearer explanations, better engineering commentary
- **Code quality**: Refactoring for clarity, additional tests

---

## Contribution Process

1. **Fork the repository** on GitHub
2. **Create a new branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes** with clear, commented code
4. **Test your changes**: Run `python src/run_analysis.py` and verify outputs look correct
5. **Update documentation** if you add new files or change behavior
6. **Submit a pull request** with a clear description of what changed and why

---

## Data Contribution Standards

If adding new material data, you must:

1. Cite the source (MatWeb datasheet ID, ASM Handbook volume/page, DOI, etc.)
2. Use the same property columns and units as the existing CSV files
3. Add an entry to `data/DATA_SOURCES.md` documenting your source
4. Use "typical" property values — not minimum/maximum unless clearly labeled

---

## Suggested Commit Message Format

```
feat: add fracture toughness data for high-strength steels
fix: correct thermal conductivity for AISI 316 stainless (MatWeb ID 7847)
docs: update methodology section with Weibull modulus note for ceramics
refactor: extract weight saving calculation to engineering_calcs.py
```

---

## Code Style

- Follow PEP 8 conventions
- Add docstrings to all functions (NumPy docstring style)
- Comment engineering equations with their source reference
- Use descriptive variable names (e.g., `tensile_strength_MPa`, not `ts`)
- Prefer clarity over cleverness

---

## Questions?

Open a GitHub Issue with your question or suggestion.

---

*This project follows open-source community standards. All contributions will be acknowledged.*

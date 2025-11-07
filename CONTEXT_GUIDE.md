# Quick Context Guide - FL Housing Affordability Analyzer

**Purpose:** Navigate to the right documentation to understand this app quickly.

---

## 🎯 To Understand This App (Start Here)

**1. High-Level Overview (5 min read):**
- → `EXECUTIVE_SUMMARY.md` - Problem, solution, findings, business value

**2. Full Documentation (15 min read):**
- → `README.md` - Features, methodology, deployment, usage

**3. Visual Understanding:**
- → `app.py` - See the 4 operational modes (Generate, Simulate, Analyze, Single Household)

---

## 📝 Recent Changes & Why

**Model Calibration Fixes:**
- → `FIXES_APPLIED.md` - Why affordability was 6.1% and how we fixed it

**Gemini Integration:**
- → `IMPROVEMENTS_IMPLEMENTED.md` - AI integration for result interpretation

**Sensitivity Sliders:**
- → `SLIDER_INTEGRATION.md` - User-adjustable assumptions (income growth, insurance, etc.)

---

## 🔧 Model Calibration Reference

**Key Parameters (Fine-Tuned):**

File: `src/monte_carlo_housing.py`

| Parameter | Location | Value | Why |
|-----------|----------|-------|-----|
| Income Growth | Lines 152-154, 296-298 | 4.0% | Florida economy average |
| Insurance Increase | Line 327-329 | 3-12% (triangular) | Realistic range vs previous 5-20% |
| Affordability Threshold | Line 344 | 50% | Industry standard for homeownership |
| $0 Cost Bug Fix | Line 263 | Records lost savings | Fixed data anomaly |

**User-Adjustable Sliders:**
- File: `src/gemini_helper.py`, function `add_sensitivity_sliders()`
- Default values match calibrated model

---

## 🧪 How to Resume Work / Test

**1. Verify Setup:**
```bash
cd FL_housing_analysis
python -m py_compile app.py src/*.py  # Check syntax
```

**2. Test Core Functionality:**
```bash
python test_model_fixes.py          # Validates calibration
python test_slider_integration.py   # Tests user parameters
python test_timeline_viz.py         # Timeline graphs
```

**3. Run App Locally:**
```bash
streamlit run app.py
```

**4. Check Recent Commits:**
```bash
git log --oneline -10
```

---

## 📂 File Structure Guide

**Core Modules:**
- `src/household_generator.py` - Synthetic FL household creation
- `src/monte_carlo_housing.py` - **Main simulation engine** (10,000+ scenarios)
- `src/financial_analysis.py` - Statistical analysis and metrics
- `src/gemini_helper.py` - AI integration + sensitivity sliders

**Key Functions to Understand:**
- `MonteCarloHousingSimulator.simulate_buying()` - Lines 211-383
- `MonteCarloHousingSimulator.simulate_renting()` - Lines 116-209
- `MonteCarloHousingSimulator.simulate_timeline()` - Lines 458-629 (for graphs)

**Test Files:**
- `test_model_fixes.py` - Validates calibration improvements
- `test_slider_integration.py` - Validates user parameter integration
- `test_timeline_viz.py` - Validates year-by-year projections

---

## 🏗️ Architecture Overview

```
User Input (app.py)
    ↓
Sidebar Sliders (gemini_helper.py)
    ↓
Stored in st.session_state
    ↓
MonteCarloHousingSimulator(income_growth=X, insurance_increase=Y, ...)
    ↓
10,000 simulations per household × 4 scenarios
    ↓
Results: affordability %, default risk, equity, costs (with percentiles)
    ↓
Timeline graphs (optimistic/expected/pessimistic)
    ↓
Gemini reports (structured summaries for AI interpretation)
```

---

## 🚨 Known Issues / Limitations

**Documented in:** `TEST_RESULTS.md` lines 183-195

1. **Low affordability for some households** - Not a bug, reflects realistic constraints
2. **Flat zero lines in graphs** - Household can't afford down payment (expected behavior)
3. **Streamlit Cloud deploy** - Uses `.python-version` (3.10) automatically

---

## 🔄 Common Tasks

**Add a new Florida region:**
1. Edit `src/monte_carlo_housing.py` line 107-114 (region_adjustments dict)
2. Edit `src/household_generator.py` (add to FLORIDA_REGIONS)

**Adjust default scenario prices:**
1. Edit `src/monte_carlo_housing.py` lines 59-103 (HousingScenarioParameters)

**Change slider ranges:**
1. Edit `src/gemini_helper.py` lines 156-204 (add_sensitivity_sliders function)

**Add new visualization:**
1. Edit `app.py` in `single_household_analysis_page()` function (starts line 535)

---

## 🎓 Academic Context

**Synthetic Data Justification:**
- → `EXECUTIVE_SUMMARY.md` lines 17-29
- → `README.md` lines 301-320
- → `app.py` lines 107-141 (About section)

**Why it's valid:** Standard practice in Monte Carlo research; eliminates privacy concerns; enables controlled experimentation.

---

## 📊 Dataset Info

**Generated Data:**
- `florida_households.csv` - Synthetic household cohort (if exists in data/)
- `florida_housing_analysis_report.csv` - Simulation results (if exists in outputs/)

**Not tracked in Git** - Regenerate using app (Mode 1: Generate Household Data)

---

## 🔗 Deployment

**Live App:** Streamlit Cloud (auto-deploys from GitHub main branch)
**Repository:** https://github.com/horacefonseca/FL_housing_montecarlo_estimation_app

**Deployment docs:**
- → `README.md` lines 230-266
- → `.python-version` specifies Python 3.10
- → `requirements.txt` has all dependencies

---

**Last Updated:** January 2025
**For Questions:** Check GitHub issues or re-read documentation files listed above

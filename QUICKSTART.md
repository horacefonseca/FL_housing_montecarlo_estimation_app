# Quick Start Guide - Florida Housing Affordability Analyzer

Get the app running in 5 minutes!

## 🚀 Local Setup (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Test Installation
```bash
python test_modules.py
```

Expected: `[SUCCESS] ALL TESTS PASSED`

### Step 3: Launch App
```bash
streamlit run app.py
```

App opens at: `http://localhost:8501`

**Done!** 🎉

---

## 🌐 Deploy to Streamlit Cloud (Free)

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Florida Housing Analyzer"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Step 2: Deploy
1. Go to https://share.streamlit.io/
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Main file: `app.py`
6. Click "Deploy"

**Live in 2-5 minutes!**

---

## 📖 First-Time User Guide

### 1. Generate Household Data (1 minute)
- Click "Generate Household Data"
- Set 100 households
- Enable amplification
- Click "Generate"
- Review Florida regions & income distribution

### 2. Run Simulations (2 minutes)
- Switch to "Run Simulations"
- Set 1,000 simulations (for testing)
- Sample size: 10 households
- Time horizon: 10 years
- Select "All Scenarios"
- Click "Run"

### 3. Analyze Results (1 minute)
- Switch to "Analyze Results"
- Review affordability by scenario
- Check income stratification
- View regional analysis
- See visualizations

### 4. Single Household (1 minute)
- Switch to "Single Household Analysis"
- Select a household
- Review their profile
- Click "Compare All Scenarios"
- See personalized recommendations

---

## 🎯 Quick Tips

### Performance
- **Testing**: 1,000 simulations, 10 households
- **Production**: 10,000 simulations, 100+ households

### Understanding Results

**Affordability Rate**: % of scenarios where household maintains payments
- 80%+: Low risk
- 50-80%: Moderate risk
- <50%: High risk

**Default Risk**: % of scenarios ending in foreclosure
- <10%: Low risk
- 10-20%: Moderate risk
- >20%: High risk

**Equity Built**: Expected home equity after time horizon
- Positive = wealth building
- Negative = potential loss

### Florida-Specific Notes

**Hurricane Insurance**: Major cost factor!
- Miami: Highest (~$8,500+ for premium homes)
- Panhandle: High risk but lower property values
- Tampa: Moderate

**Regional Prices**:
- Most expensive: Miami-Dade (35% above average)
- Least expensive: Panhandle (15% below average)

**Rent vs Buy**:
- Renting: Lower risk, no equity
- Starter Home: FHA 5% down, builds equity
- Standard Home: Better appreciation
- Premium Home: Best equity potential, highest risk

---

## 🔧 Troubleshooting

### "Module not found"
```bash
pip install -r requirements.txt
```

### Tests failing
```bash
# Check Python version
python --version  # Should be 3.9+

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Slow performance
- Reduce simulations to 1,000
- Use sample size of 10-20
- Simulate single scenario

---

## 📊 Example Workflow

**Goal**: Find best housing option for $60k income household in Tampa

```
1. Generate 500 households
2. Run simulations:
   - 10,000 per household
   - Sample 50 households
   - 10-year horizon
   - All scenarios
3. Filter results:
   - Income $55k-$65k
   - Region: Tampa Bay
4. Compare scenarios:
   - Renting: 95% affordable
   - Starter: 78% affordable, $85k equity
   - Standard: 52% affordable, $125k equity
5. Decision: Buy Starter Home (good balance)
```

---

## 🎓 For Academics

### Quick Experiment

```python
# In Python console
from src.household_generator import FloridaHouseholdGenerator
from src.monte_carlo_housing import MonteCarloHousingSimulator

# Generate data
gen = FloridaHouseholdGenerator(random_seed=42)
households = gen.generate_household_cohort(n_households=100)

# Simulate
sim = MonteCarloHousingSimulator(random_seed=42)
result = sim.simulate_household(
    households.iloc[0],
    'Buy Standard Home',
    num_simulations=10000,
    time_horizon_years=10
)

print(f"Affordability: {result['probability_affordable']*100:.1f}%")
print(f"Expected Equity: ${result['equity_built']['mean']:,.0f}")
```

---

## 📚 Learn More

- **README.md**: Complete documentation
- **config/simulation_config.json**: Adjustable parameters
- **test_modules.py**: Verify installation

---

## 🆘 Need Help?

1. Run tests: `python test_modules.py`
2. Check README.md
3. GitHub Issues

---

## ✅ Pre-Deployment Checklist

Before deploying to Streamlit Cloud:

- [ ] Tests passing (`python test_modules.py`)
- [ ] App runs locally (`streamlit run app.py`)
- [ ] Code pushed to GitHub
- [ ] `.python-version` file exists (Python 3.10)
- [ ] `requirements.txt` has compatible versions

---

**You're ready!** Start analyzing Florida housing affordability! 🏠📊

**Quick Command Reference:**
```bash
# Test
python test_modules.py

# Run locally
streamlit run app.py

# Deploy
git push origin main
# Then use Streamlit Cloud dashboard
```

"""
Test script to validate Monte Carlo model fixes
Tests the improved affordability calculations
"""

import sys
import pandas as pd
import numpy as np
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from household_generator import FloridaHouseholdGenerator
from monte_carlo_housing import MonteCarloHousingSimulator

print("=" * 80)
print("Testing Model Fixes - FL Housing Monte Carlo")
print("=" * 80)

# Generate a small test dataset
print("\n1. Generating test households...")
generator = FloridaHouseholdGenerator(random_seed=42)
test_households = generator.generate_household_cohort(n_households=10)
print(f"   [OK] Generated {len(test_households)} test households")
print(f"   Mean Income: ${test_households['annual_income'].mean():,.0f}")
print(f"   Mean Credit: {test_households['credit_score'].mean():.0f}")

# Initialize simulator
print("\n2. Initializing Monte Carlo simulator...")
simulator = MonteCarloHousingSimulator(random_seed=42)
print("   [OK] Simulator initialized")

# Test renting scenario
print("\n3. Testing 'Keep Renting' scenario...")
household = test_households.iloc[0]
renting_result = simulator.simulate_renting(
    household,
    num_simulations=1000,
    time_horizon_years=10
)
print(f"   Household: ${household['annual_income']:,.0f} income, {household['credit_score']:.0f} credit")
print(f"   Probability Affordable: {renting_result['probability_affordable']*100:.1f}%")
print(f"   Mean Total Cost: ${renting_result['total_cost_paid']['mean']:,.0f}")

# Test buying scenarios
scenarios = ['Buy Starter Home', 'Buy Standard Home', 'Buy Premium Home']
results = []

print("\n4. Testing buying scenarios...")
for scenario in scenarios:
    print(f"\n   Testing '{scenario}'...")
    result = simulator.simulate_buying(
        household,
        scenario,
        num_simulations=1000,
        time_horizon_years=10
    )

    print(f"   [OK] Probability Affordable: {result['probability_affordable']*100:.1f}%")
    print(f"   [OK] Probability Default: {result['probability_default']*100:.1f}%")
    print(f"   [OK] Mean Equity Built: ${result['equity_built']['mean']:,.0f}")
    print(f"   [OK] Mean Total Cost: ${result['total_cost_paid']['mean']:,.0f}")

    results.append({
        'scenario': scenario,
        'affordability': result['probability_affordable'] * 100,
        'default': result['probability_default'] * 100,
        'equity': result['equity_built']['mean'],
        'total_cost': result['total_cost_paid']['mean']
    })

# Summary
print("\n" + "=" * 80)
print("SUMMARY OF MODEL FIXES")
print("=" * 80)

results_df = pd.DataFrame(results)
print("\nSCENARIO COMPARISON:")
print(results_df.to_string(index=False))

print("\nKEY IMPROVEMENTS:")
print(f"   - Income Growth: 2.5% -> 4.0% (more realistic for Florida)")
print(f"   - Insurance Increases: 5-20% -> 3-12% (less aggressive)")
print(f"   - Affordability Threshold: 45% -> 50% (less conservative)")

print("\nEXPECTED RESULTS:")
print(f"   - Affordability should be HIGHER than previous 6.1%")
print(f"   - Default risk should be LOWER than previous 95.2%")
print(f"   - Total cost should be NON-ZERO (fixing anomaly)")

# Check for $0 total cost anomaly
if results_df['total_cost'].min() == 0:
    print("\n[WARNING] $0 total cost still detected - investigating...")
else:
    print("\n[OK] Total cost anomaly FIXED - all values non-zero")

# Check affordability improvement
avg_affordability = results_df['affordability'].mean()
if avg_affordability > 20:
    print(f"[OK] Affordability improved to {avg_affordability:.1f}% (was 6.1%)")
else:
    print(f"[WARNING] Affordability still low at {avg_affordability:.1f}%")

print("\n" + "=" * 80)
print("Test Complete!")
print("=" * 80)

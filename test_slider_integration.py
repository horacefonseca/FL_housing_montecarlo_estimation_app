"""
Test script to validate sensitivity slider integration
Tests that user-adjusted parameters affect simulation results
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
print("Testing Sensitivity Slider Integration")
print("=" * 80)

# Generate test household
print("\n1. Generating test household...")
generator = FloridaHouseholdGenerator(random_seed=42)
test_households = generator.generate_household_cohort(n_households=1)
household = test_households.iloc[0]
print(f"   Household: ${household['annual_income']:,.0f} income, {household['credit_score']:.0f} credit")

# Test 1: Default parameters (calibrated values)
print("\n2. Test with DEFAULT parameters...")
print("   - Income Growth: 4.0%")
print("   - Insurance Increase: 8.0%")
print("   - Affordability Threshold: 50.0%")

simulator_default = MonteCarloHousingSimulator(
    random_seed=42,
    income_growth=0.04,
    insurance_increase=0.08,
    affordability_threshold=0.50
)

result_default = simulator_default.simulate_buying(
    household,
    'Buy Starter Home',
    num_simulations=1000,
    time_horizon_years=10
)

print(f"   RESULT: {result_default['probability_affordable']*100:.1f}% affordable")

# Test 2: Conservative parameters (stricter)
print("\n3. Test with CONSERVATIVE parameters...")
print("   - Income Growth: 2.0% (lower)")
print("   - Insurance Increase: 11.0% (higher, within 3-12% range)")
print("   - Affordability Threshold: 43.0% (stricter)")

simulator_conservative = MonteCarloHousingSimulator(
    random_seed=42,
    income_growth=0.02,
    insurance_increase=0.11,
    affordability_threshold=0.43
)

result_conservative = simulator_conservative.simulate_buying(
    household,
    'Buy Starter Home',
    num_simulations=1000,
    time_horizon_years=10
)

print(f"   RESULT: {result_conservative['probability_affordable']*100:.1f}% affordable")

# Test 3: Optimistic parameters (more lenient)
print("\n4. Test with OPTIMISTIC parameters...")
print("   - Income Growth: 6.0% (higher)")
print("   - Insurance Increase: 5.0% (lower)")
print("   - Affordability Threshold: 50.0% (lenient)")

simulator_optimistic = MonteCarloHousingSimulator(
    random_seed=42,
    income_growth=0.06,
    insurance_increase=0.05,
    affordability_threshold=0.50
)

result_optimistic = simulator_optimistic.simulate_buying(
    household,
    'Buy Starter Home',
    num_simulations=1000,
    time_horizon_years=10
)

print(f"   RESULT: {result_optimistic['probability_affordable']*100:.1f}% affordable")

# Summary
print("\n" + "=" * 80)
print("SUMMARY - Parameter Sensitivity Test")
print("=" * 80)

comparison = pd.DataFrame([
    {
        'Scenario': 'Conservative',
        'Income Growth': '2.0%',
        'Insurance Inc': '11.0%',
        'Threshold': '43.0%',
        'Affordability': f"{result_conservative['probability_affordable']*100:.1f}%"
    },
    {
        'Scenario': 'Default',
        'Income Growth': '4.0%',
        'Insurance Inc': '8.0%',
        'Threshold': '50.0%',
        'Affordability': f"{result_default['probability_affordable']*100:.1f}%"
    },
    {
        'Scenario': 'Optimistic',
        'Income Growth': '6.0%',
        'Insurance Inc': '5.0%',
        'Threshold': '50.0%',
        'Affordability': f"{result_optimistic['probability_affordable']*100:.1f}%"
    }
])

print("\n" + comparison.to_string(index=False))

# Validate expected behavior
print("\n" + "=" * 80)
print("VALIDATION")
print("=" * 80)

afford_conservative = result_conservative['probability_affordable'] * 100
afford_default = result_default['probability_affordable'] * 100
afford_optimistic = result_optimistic['probability_affordable'] * 100

# Conservative should be lowest
if afford_conservative < afford_default:
    print("[OK] Conservative parameters produce LOWER affordability")
else:
    print("[WARNING] Conservative parameters did not reduce affordability as expected")

# Optimistic should be highest
if afford_optimistic > afford_default:
    print("[OK] Optimistic parameters produce HIGHER affordability")
else:
    print("[WARNING] Optimistic parameters did not increase affordability as expected")

# Check parameters are being used (not all the same)
if afford_conservative != afford_default and afford_optimistic != afford_default:
    print("[OK] Parameters ARE affecting simulation results")
else:
    print("[WARNING] Parameters may NOT be affecting simulation results")

print("\n" + "=" * 80)
print("Slider Integration Test Complete!")
print("=" * 80)

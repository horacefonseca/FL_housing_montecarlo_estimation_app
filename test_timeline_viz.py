"""
Quick test for timeline visualization feature
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / 'src'))

from household_generator import FloridaHouseholdGenerator
from monte_carlo_housing import MonteCarloHousingSimulator

print("=" * 80)
print("Testing Timeline Visualization Feature")
print("=" * 80)

# Generate test household
print("\n1. Generating test household...")
generator = FloridaHouseholdGenerator(random_seed=42)
households = generator.generate_household_cohort(n_households=1)
household = households.iloc[0]

print(f"   Household: ${household['annual_income']:,.0f} income, {household['credit_score']:.0f} credit")
print(f"   Region: {household['region']}, Savings: ${household['savings']:,.0f}")

# Initialize simulator
print("\n2. Testing simulate_timeline() function...")
simulator = MonteCarloHousingSimulator(random_seed=42)

# Test timeline for Buy Starter Home
scenario = 'Buy Starter Home'
print(f"\n3. Running timeline simulation for '{scenario}'...")

timeline = simulator.simulate_timeline(
    household,
    scenario,
    num_simulations=100,  # Small number for quick test
    time_horizon_years=10
)

print(f"\n4. Timeline Results:")
print(f"   Scenario: {timeline['scenario']}")
print(f"   Years tracked: {len(timeline['years'])}")
print(f"   Years: {timeline['years']}")

print(f"\n5. Equity Over Time (first 5 years):")
for i in range(min(5, len(timeline['years']))):
    year = timeline['years'][i]
    pess = timeline['equity']['pessimistic'][i]
    exp = timeline['equity']['expected'][i]
    opt = timeline['equity']['optimistic'][i]
    print(f"   Year {year}: Pessimistic=${pess:,.0f}, Expected=${exp:,.0f}, Optimistic=${opt:,.0f}")

print(f"\n6. Monthly Costs Over Time (first 5 years):")
for i in range(min(5, len(timeline['years']))):
    year = timeline['years'][i]
    opt_cost = timeline['monthly_costs']['optimistic'][i]
    exp_cost = timeline['monthly_costs']['expected'][i]
    pess_cost = timeline['monthly_costs']['pessimistic'][i]
    print(f"   Year {year}: Best=${opt_cost:,.0f}, Expected=${exp_cost:,.0f}, Worst=${pess_cost:,.0f}")

print(f"\n7. Cumulative Costs (first 5 years):")
for i in range(min(5, len(timeline['years']))):
    year = timeline['years'][i]
    opt_total = timeline['cumulative_costs']['optimistic'][i]
    exp_total = timeline['cumulative_costs']['expected'][i]
    pess_total = timeline['cumulative_costs']['pessimistic'][i]
    print(f"   Year {year}: Best=${opt_total:,.0f}, Expected=${exp_total:,.0f}, Worst=${pess_total:,.0f}")

# Validation
print("\n" + "=" * 80)
print("VALIDATION")
print("=" * 80)

# Check data structure
if 'years' in timeline and 'equity' in timeline and 'monthly_costs' in timeline:
    print("[OK] Timeline data structure is correct")
else:
    print("[ERROR] Missing expected keys in timeline data")

# Check equity progression
final_equity_expected = timeline['equity']['expected'][-1]
if final_equity_expected > 0:
    print(f"[OK] Positive final equity: ${final_equity_expected:,.0f}")
else:
    print(f"[WARNING] Negative or zero final equity: ${final_equity_expected:,.0f}")

# Check costs increase over time
initial_cost = timeline['monthly_costs']['expected'][0]
final_cost = timeline['monthly_costs']['expected'][-1]
if final_cost > initial_cost:
    print(f"[OK] Costs increased over time: ${initial_cost:,.0f} -> ${final_cost:,.0f}")
else:
    print(f"[WARNING] Costs did not increase as expected")

# Check cumulative costs accumulate
cumulative_initial = timeline['cumulative_costs']['expected'][0]
cumulative_final = timeline['cumulative_costs']['expected'][-1]
if cumulative_final > cumulative_initial:
    print(f"[OK] Cumulative costs accumulated: ${cumulative_initial:,.0f} -> ${cumulative_final:,.0f}")
else:
    print(f"[ERROR] Cumulative costs did not accumulate properly")

print("\n" + "=" * 80)
print("Timeline Test Complete!")
print("=" * 80)

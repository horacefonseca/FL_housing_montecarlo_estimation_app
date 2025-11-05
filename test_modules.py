"""
Test script to verify all modules work correctly
Run this before deploying the application
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from household_generator import FloridaHouseholdGenerator
from monte_carlo_housing import MonteCarloHousingSimulator
from financial_analysis import FloridaHousingAnalyzer

def test_household_generator():
    """Test household data generation"""
    print("\n" + "="*80)
    print("TEST 1: Household Data Generator")
    print("="*80)

    try:
        generator = FloridaHouseholdGenerator(random_seed=42)
        households = generator.generate_household_cohort(n_households=100, amplify=True)

        assert len(households) > 100, "Amplification should increase household count"
        assert 'household_id' in households.columns, "Missing household_id column"
        assert 'financial_risk_score' in households.columns, "Missing financial_risk_score column"

        print(f"[OK] Generated {len(households)} households successfully")
        print(f"[OK] Columns: {list(households.columns)}")
        print(f"[OK] Income range: ${households['annual_income'].min():,.0f} - ${households['annual_income'].max():,.0f}")
        print(f"[OK] Risk score range: {households['financial_risk_score'].min():.1f} - {households['financial_risk_score'].max():.1f}")

        return households

    except Exception as e:
        print(f"[FAIL] Household generator test failed: {str(e)}")
        return None


def test_monte_carlo_simulator(households):
    """Test Monte Carlo housing simulation"""
    print("\n" + "="*80)
    print("TEST 2: Monte Carlo Housing Simulator")
    print("="*80)

    if households is None:
        print("[FAIL] Skipping simulator test (no household data)")
        return None

    try:
        simulator = MonteCarloHousingSimulator(random_seed=42)

        # Test single household - renting scenario
        test_household = households.iloc[0]
        print(f"\nTesting single household: {test_household['household_id']}")
        print(f"Income: ${test_household['annual_income']:,.0f}, Region: {test_household['region']}")

        result = simulator.simulate_household(
            test_household,
            'Keep Renting',
            num_simulations=1000,
            time_horizon_years=10
        )

        assert 'probability_affordable' in result, "Missing affordability probability"
        assert 'total_cost_paid' in result, "Missing total cost"
        assert 0 <= result['probability_affordable'] <= 1, "Invalid affordability probability"

        print(f"[OK] Renting simulation successful")
        print(f"  - Affordability probability: {result['probability_affordable']*100:.1f}%")
        print(f"  - Mean total cost: ${result['total_cost_paid']['mean']:,.0f}")

        # Test buying scenario
        result2 = simulator.simulate_household(
            test_household,
            'Buy Starter Home',
            num_simulations=1000,
            time_horizon_years=10
        )

        print(f"[OK] Buying simulation successful")
        print(f"  - Affordability probability: {result2['probability_affordable']*100:.1f}%")
        print(f"  - Mean equity built: ${result2['equity_built']['mean']:,.0f}")

        # Create simple results dataframe for testing
        results_list = [result, result2]
        import pandas as pd
        results_df = pd.DataFrame(results_list)

        print(f"[OK] Simulation results compiled successfully")

        return results_df

    except Exception as e:
        print(f"[FAIL] Simulator test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def test_analyzer(households, results_df):
    """Test financial analysis module"""
    print("\n" + "="*80)
    print("TEST 3: Financial Analyzer")
    print("="*80)

    if results_df is None or households is None:
        print("[FAIL] Skipping analyzer test (no simulation results or household data)")
        return False

    try:
        analyzer = FloridaHousingAnalyzer()

        # Test summary statistics
        summary = analyzer.generate_summary_statistics(results_df)
        assert 'total_households' in summary, "Missing total_households in summary"
        print(f"[OK] Summary statistics generated")
        print(f"  - Total scenarios analyzed: {summary['total_households']}")

        # Test scenario comparison
        comparison = analyzer.compare_scenarios_analysis(results_df)
        assert len(comparison) > 0, "No scenario comparison results"
        print(f"[OK] Scenario comparison successful")
        print(f"  - Compared {len(comparison)} scenarios")

        # Test income stratification
        income_analysis = analyzer.income_stratification_analysis(households, results_df)
        print(f"[OK] Income stratification successful")
        print(f"  - Income brackets analyzed: {len(income_analysis)}")

        return True

    except Exception as e:
        print(f"[FAIL] Analyzer test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("FLORIDA HOUSING MONTE CARLO ANALYZER - MODULE TESTS")
    print("="*80)

    # Test 1: Household Generation
    households = test_household_generator()

    # Test 2: Monte Carlo Simulation
    results_df = test_monte_carlo_simulator(households)

    # Test 3: Financial Analysis
    analyzer_ok = test_analyzer(households, results_df)

    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)

    all_passed = (households is not None) and (results_df is not None) and analyzer_ok

    if all_passed:
        print("[SUCCESS] ALL TESTS PASSED")
        print("\nThe application is ready to deploy!")
        print("\nNext steps:")
        print("1. Run the app locally: streamlit run app.py")
        print("2. Push to GitHub")
        print("3. Deploy on Streamlit Cloud")
    else:
        print("[FAIL] SOME TESTS FAILED")
        print("\nPlease fix the errors before deploying.")

    print("="*80 + "\n")

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

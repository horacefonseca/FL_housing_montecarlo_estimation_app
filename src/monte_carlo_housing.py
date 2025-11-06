"""
Monte Carlo Simulator for Florida Housing Affordability
Simulates housing outcomes using probabilistic models with Florida-specific factors
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class HousingScenarioParameters:
    """Parameters for housing scenario simulation"""
    scenario_name: str
    home_price_min: float
    home_price_max: float
    down_payment_pct: float
    interest_rate_mean: float
    interest_rate_std: float
    property_tax_rate: float  # Annual % of home value
    hurricane_insurance_annual: float
    hoa_monthly: float
    maintenance_annual_pct: float  # % of home value
    appreciation_mean: float  # Annual %
    appreciation_std: float
    closing_costs_pct: float


class MonteCarloHousingSimulator:
    """Monte Carlo simulation engine for Florida housing affordability analysis"""

    def __init__(
        self,
        random_seed: int = 42,
        income_growth: float = 0.04,
        insurance_increase: float = 0.08,
        affordability_threshold: float = 0.50,
        appreciation_rate: Optional[float] = None,
        interest_rate: Optional[float] = None
    ):
        """
        Initialize the simulator

        Args:
            random_seed: Random seed for reproducibility
            income_growth: Annual income growth rate (default 4%)
            insurance_increase: Annual insurance increase rate (default 8%)
            affordability_threshold: Max housing cost as % of income (default 50%)
            appreciation_rate: Override home appreciation rate (optional)
            interest_rate: Override mortgage interest rate (optional)
        """
        np.random.seed(random_seed)

        # Store sensitivity parameters
        self.income_growth = income_growth
        self.insurance_increase = insurance_increase
        self.affordability_threshold = affordability_threshold
        self.appreciation_rate = appreciation_rate
        self.interest_rate = interest_rate

        # Define housing scenarios with Florida-specific parameters
        self.scenarios = {
            'Keep Renting': HousingScenarioParameters(
                scenario_name='Keep Renting',
                home_price_min=0,
                home_price_max=0,
                down_payment_pct=0,
                interest_rate_mean=0,
                interest_rate_std=0,
                property_tax_rate=0,
                hurricane_insurance_annual=0,
                hoa_monthly=0,
                maintenance_annual_pct=0,
                appreciation_mean=0,
                appreciation_std=0,
                closing_costs_pct=0
            ),
            'Buy Starter Home': HousingScenarioParameters(
                scenario_name='Buy Starter Home',
                home_price_min=200000,
                home_price_max=300000,
                down_payment_pct=0.05,  # 5% down (FHA)
                interest_rate_mean=0.065,  # 6.5%
                interest_rate_std=0.01,
                property_tax_rate=0.009,  # 0.9% Florida average
                hurricane_insurance_annual=3500,  # Lower for starter homes
                hoa_monthly=150,
                maintenance_annual_pct=0.015,  # 1.5% of home value
                appreciation_mean=0.04,  # 4% annual
                appreciation_std=0.08,
                closing_costs_pct=0.03
            ),
            'Buy Standard Home': HousingScenarioParameters(
                scenario_name='Buy Standard Home',
                home_price_min=300000,
                home_price_max=500000,
                down_payment_pct=0.10,  # 10% down
                interest_rate_mean=0.0625,  # 6.25%
                interest_rate_std=0.01,
                property_tax_rate=0.009,
                hurricane_insurance_annual=5500,  # Higher for standard homes
                hoa_monthly=250,
                maintenance_annual_pct=0.015,
                appreciation_mean=0.045,  # 4.5% annual
                appreciation_std=0.10,
                closing_costs_pct=0.03
            ),
            'Buy Premium Home': HousingScenarioParameters(
                scenario_name='Buy Premium Home',
                home_price_min=500000,
                home_price_max=800000,
                down_payment_pct=0.20,  # 20% down
                interest_rate_mean=0.06,  # 6.0%
                interest_rate_std=0.008,
                property_tax_rate=0.009,
                hurricane_insurance_annual=8500,  # Highest for premium homes
                hoa_monthly=400,
                maintenance_annual_pct=0.02,  # 2% for larger homes
                appreciation_mean=0.05,  # 5% annual
                appreciation_std=0.12,
                closing_costs_pct=0.03
            )
        }

        # Region-specific adjustments for Florida
        self.region_adjustments = {
            'Miami-Dade': {'price_multiplier': 1.35, 'insurance_multiplier': 1.40},
            'Tampa Bay': {'price_multiplier': 1.10, 'insurance_multiplier': 1.20},
            'Orlando': {'price_multiplier': 1.05, 'insurance_multiplier': 1.15},
            'Jacksonville': {'price_multiplier': 0.95, 'insurance_multiplier': 1.10},
            'Southwest FL': {'price_multiplier': 1.20, 'insurance_multiplier': 1.35},
            'Panhandle': {'price_multiplier': 0.85, 'insurance_multiplier': 1.25}
        }

    def simulate_renting(
        self,
        household: pd.Series,
        num_simulations: int = 10000,
        time_horizon_years: int = 10
    ) -> Dict:
        """
        Simulate renting scenario over time horizon

        Args:
            household: Household data as pandas Series
            num_simulations: Number of Monte Carlo simulations
            time_horizon_years: Projection period in years

        Returns:
            Dictionary with simulation results
        """
        current_rent = household['current_monthly_rent']
        annual_income = household['annual_income']

        # Arrays to store results
        final_rent = np.zeros(num_simulations)
        total_paid = np.zeros(num_simulations)
        affordability_months = np.zeros(num_simulations)

        for sim in range(num_simulations):
            rent = current_rent
            total_cost = 0
            months_affordable = 0
            income = annual_income

            for year in range(time_horizon_years):
                # Rent increases (Florida: 3-10% annually, triangular distribution)
                rent_increase = np.random.triangular(0.03, 0.05, 0.10)
                rent *= (1 + rent_increase)

                # Income changes (user-adjustable via sensitivity slider)
                income_change = np.random.normal(self.income_growth, 0.08)
                income *= (1 + income_change)

                # Check affordability (rent should be <35% of gross income)
                monthly_income = income / 12
                is_affordable = (rent / monthly_income) <= 0.35

                if is_affordable:
                    months_affordable += 12
                    total_cost += rent * 12
                else:
                    # Becoming unaffordable
                    affordable_months_this_year = 0
                    for month in range(12):
                        if (rent / monthly_income) <= 0.35:
                            affordable_months_this_year += 1
                            total_cost += rent
                        else:
                            break
                    months_affordable += affordable_months_this_year
                    break

            final_rent[sim] = rent
            total_paid[sim] = total_cost
            affordability_months[sim] = months_affordable

        # Calculate results
        results = {
            'household_id': household['household_id'],
            'scenario': 'Keep Renting',
            'simulations': num_simulations,
            'time_horizon_years': time_horizon_years,
            'initial_monthly_cost': current_rent,
            'final_monthly_cost': {
                'mean': final_rent.mean(),
                'median': np.median(final_rent),
                'percentile_5': np.percentile(final_rent, 5),
                'percentile_95': np.percentile(final_rent, 95)
            },
            'total_cost_paid': {
                'mean': total_paid.mean(),
                'median': np.median(total_paid),
                'percentile_5': np.percentile(total_paid, 5),
                'percentile_95': np.percentile(total_paid, 95)
            },
            'equity_built': {
                'mean': 0,
                'median': 0,
                'percentile_5': 0,
                'percentile_95': 0
            },
            'probability_affordable': (affordability_months == time_horizon_years * 12).sum() / num_simulations,
            'probability_unaffordable': (affordability_months < time_horizon_years * 12).sum() / num_simulations,
            'mean_affordable_months': affordability_months.mean()
        }

        return results

    def simulate_buying(
        self,
        household: pd.Series,
        scenario_name: str,
        num_simulations: int = 10000,
        time_horizon_years: int = 10
    ) -> Dict:
        """
        Simulate home buying scenario

        Args:
            household: Household data as pandas Series
            scenario_name: Name of housing scenario
            num_simulations: Number of simulations
            time_horizon_years: Projection period in years

        Returns:
            Dictionary with simulation results
        """
        params = self.scenarios[scenario_name]
        annual_income = household['annual_income']
        savings = household['savings']
        credit_score = household['credit_score']
        debt_to_income = household['debt_to_income_ratio']
        region = household['region']

        # Get region adjustments
        region_adj = self.region_adjustments.get(region, {'price_multiplier': 1.0, 'insurance_multiplier': 1.0})

        # Arrays to store results
        final_equity = np.zeros(num_simulations)
        monthly_costs = np.zeros(num_simulations)
        total_paid = np.zeros(num_simulations)
        default_occurred = np.zeros(num_simulations, dtype=bool)
        months_solvent = np.zeros(num_simulations)

        for sim in range(num_simulations):
            # Determine home price within range
            home_price = np.random.uniform(params.home_price_min, params.home_price_max)
            home_price *= region_adj['price_multiplier']

            # Down payment
            down_payment = home_price * params.down_payment_pct
            closing_costs = home_price * params.closing_costs_pct

            # Check if household has enough savings
            if savings < (down_payment + closing_costs):
                # Cannot afford, mark as default
                default_occurred[sim] = True
                final_equity[sim] = -closing_costs if savings >= closing_costs else -savings
                months_solvent[sim] = 0
                # Record lost savings as total cost
                total_paid[sim] = min(savings, closing_costs)
                continue

            # Mortgage amount
            loan_amount = home_price - down_payment

            # Interest rate (adjusted by credit score)
            credit_adjustment = (750 - credit_score) * 0.0001  # Better credit = lower rate
            interest_rate = np.random.normal(params.interest_rate_mean + credit_adjustment, params.interest_rate_std)
            interest_rate = np.clip(interest_rate, 0.03, 0.10)

            # Monthly mortgage payment (principal + interest)
            monthly_rate = interest_rate / 12
            num_payments = 30 * 12  # 30-year mortgage
            if monthly_rate > 0:
                monthly_mortgage = loan_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
            else:
                monthly_mortgage = loan_amount / num_payments

            # Initial monthly costs
            monthly_property_tax = (home_price * params.property_tax_rate) / 12
            monthly_insurance = (params.hurricane_insurance_annual * region_adj['insurance_multiplier']) / 12
            monthly_hoa = params.hoa_monthly
            monthly_maintenance = (home_price * params.maintenance_annual_pct) / 12

            total_monthly = monthly_mortgage + monthly_property_tax + monthly_insurance + monthly_hoa + monthly_maintenance

            # Simulate over time horizon
            current_home_value = home_price
            current_loan_balance = loan_amount
            income = annual_income
            total_costs = down_payment + closing_costs
            months_affordable = 0

            for year in range(time_horizon_years):
                # Income changes (user-adjustable via sensitivity slider)
                income_change = np.random.normal(self.income_growth, 0.08)
                income *= (1 + income_change)

                # Home appreciation
                appreciation = np.random.normal(params.appreciation_mean, params.appreciation_std)
                current_home_value *= (1 + appreciation)

                # Hurricane insurance increases (user-adjustable via sensitivity slider)
                # Clamp mode to valid range [0.03, 0.12] for triangular distribution
                insurance_mode = np.clip(self.insurance_increase, 0.03, 0.12)
                insurance_increase = np.random.triangular(0.03, insurance_mode, 0.12)
                monthly_insurance *= (1 + insurance_increase)

                # Property tax adjusts with home value
                monthly_property_tax = (current_home_value * params.property_tax_rate) / 12

                # Maintenance varies
                monthly_maintenance = (current_home_value * params.maintenance_annual_pct) / 12 * np.random.uniform(0.8, 1.5)

                # Recalculate total monthly cost
                total_monthly = monthly_mortgage + monthly_property_tax + monthly_insurance + monthly_hoa + monthly_maintenance

                # Check affordability (housing costs should be <50% of gross income for buying)
                monthly_income = income / 12
                housing_ratio = total_monthly / monthly_income

                for month in range(12):
                    if housing_ratio <= self.affordability_threshold:  # User-adjustable threshold
                        months_affordable += 1
                        total_costs += total_monthly
                        # Pay down mortgage
                        interest_payment = current_loan_balance * (interest_rate / 12)
                        principal_payment = monthly_mortgage - interest_payment
                        current_loan_balance -= principal_payment
                    else:
                        # Default risk
                        if np.random.random() < 0.3:  # 30% chance of default when unaffordable
                            default_occurred[sim] = True
                            break

                if default_occurred[sim]:
                    break

            # Calculate final equity
            if default_occurred[sim]:
                # Lost home, negative equity
                final_equity[sim] = -(down_payment + closing_costs + total_costs * 0.2)  # Partial loss
            else:
                final_equity[sim] = current_home_value - max(0, current_loan_balance)

            monthly_costs[sim] = total_monthly
            total_paid[sim] = total_costs
            months_solvent[sim] = months_affordable

        # Calculate results
        results = {
            'household_id': household['household_id'],
            'scenario': scenario_name,
            'simulations': num_simulations,
            'time_horizon_years': time_horizon_years,
            'initial_monthly_cost': {
                'mean': monthly_costs[~default_occurred].mean() if (~default_occurred).sum() > 0 else 0,
                'median': np.median(monthly_costs[~default_occurred]) if (~default_occurred).sum() > 0 else 0
            },
            'final_monthly_cost': {
                'mean': monthly_costs[~default_occurred].mean() if (~default_occurred).sum() > 0 else 0,
                'median': np.median(monthly_costs[~default_occurred]) if (~default_occurred).sum() > 0 else 0,
                'percentile_5': np.percentile(monthly_costs[~default_occurred], 5) if (~default_occurred).sum() > 0 else 0,
                'percentile_95': np.percentile(monthly_costs[~default_occurred], 95) if (~default_occurred).sum() > 0 else 0
            },
            'total_cost_paid': {
                'mean': total_paid.mean(),
                'median': np.median(total_paid),
                'percentile_5': np.percentile(total_paid, 5),
                'percentile_95': np.percentile(total_paid, 95)
            },
            'equity_built': {
                'mean': final_equity[~default_occurred].mean() if (~default_occurred).sum() > 0 else final_equity.mean(),
                'median': np.median(final_equity[~default_occurred]) if (~default_occurred).sum() > 0 else np.median(final_equity),
                'percentile_5': np.percentile(final_equity, 5),
                'percentile_95': np.percentile(final_equity, 95)
            },
            'probability_affordable': (months_solvent == time_horizon_years * 12).sum() / num_simulations,
            'probability_default': default_occurred.sum() / num_simulations,
            'probability_negative_equity': (final_equity < 0).sum() / num_simulations,
            'mean_affordable_months': months_solvent.mean()
        }

        return results

    def simulate_household(
        self,
        household: pd.Series,
        scenario: str,
        num_simulations: int = 10000,
        time_horizon_years: int = 10
    ) -> Dict:
        """
        Simulate a specific scenario for a household

        Args:
            household: Household data
            scenario: Housing scenario name
            num_simulations: Number of simulations
            time_horizon_years: Time horizon

        Returns:
            Simulation results
        """
        if scenario == 'Keep Renting':
            return self.simulate_renting(household, num_simulations, time_horizon_years)
        else:
            return self.simulate_buying(household, scenario, num_simulations, time_horizon_years)

    def compare_scenarios(
        self,
        household: pd.Series,
        num_simulations: int = 10000,
        time_horizon_years: int = 10
    ) -> Dict:
        """
        Compare all housing scenarios for a household

        Args:
            household: Household data
            num_simulations: Number of simulations
            time_horizon_years: Time horizon

        Returns:
            Dictionary with all scenario results
        """
        comparison = {}

        for scenario_name in self.scenarios.keys():
            result = self.simulate_household(household, scenario_name, num_simulations, time_horizon_years)
            comparison[scenario_name] = result

        return comparison

    def simulate_timeline(
        self,
        household: pd.Series,
        scenario_name: str,
        num_simulations: int = 1000,
        time_horizon_years: int = 10
    ) -> Dict:
        """
        Simulate scenario with year-by-year tracking for timeline visualization

        Args:
            household: Household data
            scenario_name: Housing scenario name
            num_simulations: Number of simulations (default 1000 for performance)
            time_horizon_years: Time horizon in years

        Returns:
            Dictionary with yearly timelines (equity, costs, affordability)
        """
        params = self.scenarios[scenario_name]
        annual_income = household['annual_income']
        savings = household['savings']
        credit_score = household['credit_score']
        region = household['region']

        # Get region adjustments
        region_adj = self.region_adjustments.get(region, {'price_multiplier': 1.0, 'insurance_multiplier': 1.0})

        # Track yearly metrics across all simulations
        yearly_equity = np.zeros((num_simulations, time_horizon_years + 1))  # +1 for year 0
        yearly_costs = np.zeros((num_simulations, time_horizon_years + 1))
        yearly_total_paid = np.zeros((num_simulations, time_horizon_years + 1))

        for sim in range(num_simulations):
            if scenario_name == 'Keep Renting':
                # Renting simulation
                rent = household['current_monthly_rent']
                income = annual_income
                cumulative_cost = 0

                yearly_equity[sim, 0] = 0
                yearly_costs[sim, 0] = rent
                yearly_total_paid[sim, 0] = 0

                for year in range(1, time_horizon_years + 1):
                    # Rent increases
                    rent_increase = np.random.triangular(0.03, 0.05, 0.10)
                    rent *= (1 + rent_increase)

                    # Income changes
                    income_change = np.random.normal(self.income_growth, 0.08)
                    income *= (1 + income_change)

                    # Accumulate costs
                    cumulative_cost += rent * 12

                    yearly_equity[sim, year] = 0
                    yearly_costs[sim, year] = rent
                    yearly_total_paid[sim, year] = cumulative_cost

            else:
                # Buying simulation
                home_price = np.random.uniform(params.home_price_min, params.home_price_max)
                home_price *= region_adj['price_multiplier']

                down_payment = home_price * params.down_payment_pct
                closing_costs = home_price * params.closing_costs_pct

                # Check if can afford
                if savings < (down_payment + closing_costs):
                    # Cannot afford - all years show negative
                    yearly_equity[sim, :] = -min(savings, closing_costs)
                    yearly_costs[sim, :] = 0
                    yearly_total_paid[sim, :] = min(savings, closing_costs)
                    continue

                loan_amount = home_price - down_payment

                # Interest rate
                credit_adjustment = (750 - credit_score) * 0.0001
                interest_rate = np.random.normal(params.interest_rate_mean + credit_adjustment, params.interest_rate_std)
                interest_rate = np.clip(interest_rate, 0.03, 0.10)

                # Monthly mortgage
                monthly_rate = interest_rate / 12
                num_payments = 30 * 12
                if monthly_rate > 0:
                    monthly_mortgage = loan_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
                else:
                    monthly_mortgage = loan_amount / num_payments

                # Initial costs
                monthly_insurance = (params.hurricane_insurance_annual * region_adj['insurance_multiplier']) / 12
                monthly_hoa = params.hoa_monthly

                current_home_value = home_price
                current_loan_balance = loan_amount
                income = annual_income
                cumulative_cost = down_payment + closing_costs

                # Year 0
                yearly_equity[sim, 0] = down_payment
                yearly_costs[sim, 0] = (monthly_mortgage + (home_price * params.property_tax_rate) / 12 + monthly_insurance + monthly_hoa)
                yearly_total_paid[sim, 0] = cumulative_cost

                for year in range(1, time_horizon_years + 1):
                    # Income changes
                    income_change = np.random.normal(self.income_growth, 0.08)
                    income *= (1 + income_change)

                    # Home appreciation
                    appreciation = np.random.normal(params.appreciation_mean, params.appreciation_std)
                    current_home_value *= (1 + appreciation)

                    # Insurance increases
                    insurance_mode = np.clip(self.insurance_increase, 0.03, 0.12)
                    insurance_increase = np.random.triangular(0.03, insurance_mode, 0.12)
                    monthly_insurance *= (1 + insurance_increase)

                    # Property tax and maintenance
                    monthly_property_tax = (current_home_value * params.property_tax_rate) / 12
                    monthly_maintenance = (current_home_value * params.maintenance_annual_pct) / 12

                    total_monthly = monthly_mortgage + monthly_property_tax + monthly_insurance + monthly_hoa + monthly_maintenance

                    # Pay down mortgage for the year
                    for month in range(12):
                        interest_payment = current_loan_balance * (interest_rate / 12)
                        principal_payment = monthly_mortgage - interest_payment
                        current_loan_balance -= principal_payment
                        cumulative_cost += total_monthly

                    # Calculate equity at end of year
                    equity = current_home_value - max(0, current_loan_balance)

                    yearly_equity[sim, year] = equity
                    yearly_costs[sim, year] = total_monthly
                    yearly_total_paid[sim, year] = cumulative_cost

        # Calculate percentiles for each year
        years = list(range(time_horizon_years + 1))
        equity_p5 = [np.percentile(yearly_equity[:, y], 5) for y in years]
        equity_p50 = [np.percentile(yearly_equity[:, y], 50) for y in years]
        equity_p95 = [np.percentile(yearly_equity[:, y], 95) for y in years]

        costs_p5 = [np.percentile(yearly_costs[:, y], 5) for y in years]
        costs_p50 = [np.percentile(yearly_costs[:, y], 50) for y in years]
        costs_p95 = [np.percentile(yearly_costs[:, y], 95) for y in years]

        total_p5 = [np.percentile(yearly_total_paid[:, y], 5) for y in years]
        total_p50 = [np.percentile(yearly_total_paid[:, y], 50) for y in years]
        total_p95 = [np.percentile(yearly_total_paid[:, y], 95) for y in years]

        return {
            'scenario': scenario_name,
            'years': years,
            'equity': {
                'pessimistic': equity_p5,  # 5th percentile
                'expected': equity_p50,     # median
                'optimistic': equity_p95    # 95th percentile
            },
            'monthly_costs': {
                'pessimistic': costs_p95,   # 95th percentile (higher is worse)
                'expected': costs_p50,
                'optimistic': costs_p5      # 5th percentile (lower is better)
            },
            'cumulative_costs': {
                'pessimistic': total_p95,
                'expected': total_p50,
                'optimistic': total_p5
            }
        }


if __name__ == "__main__":
    # Test the simulator
    print("=" * 80)
    print("Florida Housing Monte Carlo Simulator - Test Run")
    print("=" * 80)
    print("\nSimulator initialized successfully!")
    print(f"Available scenarios: {list(MonteCarloHousingSimulator().scenarios.keys())}")

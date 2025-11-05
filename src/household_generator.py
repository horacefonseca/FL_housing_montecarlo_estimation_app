"""
Florida Household Data Generator with Synthetic Data Amplification
Generates realistic household profiles for Florida housing affordability analysis
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from datetime import datetime


class FloridaHouseholdGenerator:
    """Generate synthetic household data with realistic Florida characteristics"""

    def __init__(self, random_seed: int = 42):
        """
        Initialize the household generator

        Args:
            random_seed: Random seed for reproducibility
        """
        np.random.seed(random_seed)

        self.florida_regions = ['Miami-Dade', 'Tampa Bay', 'Orlando', 'Jacksonville', 'Panhandle', 'Southwest FL']
        self.employment_sectors = ['Tourism/Hospitality', 'Healthcare', 'Technology', 'Education',
                                   'Retail', 'Construction', 'Finance', 'Government', 'Agriculture']
        self.housing_scenarios = ['Currently Renting', 'First-Time Buyer', 'Move-Up Buyer', 'Investor']

    def generate_base_population(self, n_households: int = 1000) -> pd.DataFrame:
        """
        Generate base household population with realistic Florida characteristics

        Args:
            n_households: Number of households to generate

        Returns:
            DataFrame with household characteristics
        """
        # Generate age of head of household (skewed toward working age)
        ages = np.random.gamma(shape=6, scale=6, size=n_households) + 25
        ages = np.clip(ages, 25, 75).astype(int)

        # Generate household size (1-5 people, mode at 2)
        household_sizes = np.random.choice([1, 2, 3, 4, 5], size=n_households,
                                          p=[0.25, 0.35, 0.20, 0.15, 0.05])

        # Generate annual income (correlated with age and household size)
        base_income = 35000 + (ages - 25) * 800  # Income increases with age
        household_factor = (household_sizes - 1) * 8000  # Multi-earner households
        income_variation = np.random.normal(0, 15000, size=n_households)
        annual_income = base_income + household_factor + income_variation
        annual_income = np.clip(annual_income, 25000, 200000)

        # Generate employment sector (affects income stability)
        employment_sectors = np.random.choice(self.employment_sectors, size=n_households,
                                             p=[0.20, 0.15, 0.12, 0.10, 0.12, 0.08, 0.08, 0.10, 0.05])

        # Adjust income based on sector (Tech and Finance higher, Tourism/Retail lower)
        sector_adjustments = {
            'Technology': 1.35,
            'Finance': 1.25,
            'Healthcare': 1.15,
            'Government': 1.10,
            'Education': 1.05,
            'Construction': 1.00,
            'Agriculture': 0.85,
            'Retail': 0.80,
            'Tourism/Hospitality': 0.75
        }

        for idx, sector in enumerate(employment_sectors):
            annual_income[idx] *= sector_adjustments.get(sector, 1.0)

        annual_income = np.clip(annual_income, 25000, 200000)

        # Generate Florida region (affects housing costs)
        regions = np.random.choice(self.florida_regions, size=n_households,
                                  p=[0.25, 0.20, 0.18, 0.15, 0.12, 0.10])

        # Generate credit score (correlated with income and age)
        base_credit = 550 + (annual_income - 25000) / 1000 + (ages - 25) * 2
        credit_variation = np.random.normal(0, 40, size=n_households)
        credit_scores = base_credit + credit_variation
        credit_scores = np.clip(credit_scores, 550, 850).astype(int)

        # Generate current debt (student loans, car loans, credit cards)
        debt_factor = np.random.beta(2, 5, size=n_households)  # Most have moderate debt
        current_debt = debt_factor * (annual_income * 0.8)  # Up to 80% of income
        current_debt = np.clip(current_debt, 0, 150000)

        # Generate current monthly rent (if renting)
        region_rent_base = {
            'Miami-Dade': 1800,
            'Tampa Bay': 1500,
            'Orlando': 1450,
            'Jacksonville': 1300,
            'Southwest FL': 1600,
            'Panhandle': 1200
        }

        current_rent = []
        for region in regions:
            base_rent = region_rent_base[region]
            # Rent varies by household size
            rent = base_rent + (household_sizes[len(current_rent)] - 1) * 200
            rent += np.random.normal(0, 150)
            current_rent.append(max(800, rent))

        current_rent = np.array(current_rent)

        # Generate savings (down payment potential)
        savings_rate = np.clip((annual_income - current_rent * 12 - 20000) / annual_income, 0, 0.25)
        years_saving = np.random.uniform(0, 10, size=n_households)
        savings = savings_rate * annual_income * years_saving * np.random.uniform(0.5, 1.5, size=n_households)
        savings = np.clip(savings, 0, 150000)

        # Calculate debt-to-income ratio
        monthly_debt_payment = current_debt * 0.01  # Assume ~1% of debt as monthly payment
        monthly_income = annual_income / 12
        debt_to_income = (monthly_debt_payment / monthly_income)
        debt_to_income = np.clip(debt_to_income, 0, 0.65)

        # Calculate financial risk score (0-100, higher = riskier)
        risk_score = (
            (1 - (credit_scores - 550) / 300) * 30 +  # Credit score contribution
            debt_to_income * 40 +  # DTI contribution
            (1 - savings / 50000) * 0.2 * 30  # Savings contribution (low weight if high)
        )
        risk_score = np.clip(risk_score, 0, 100)

        # Assign housing scenario based on age, income, savings
        housing_scenarios = []
        for idx in range(n_households):
            if savings[idx] < 10000:
                scenario = 'Currently Renting'
            elif savings[idx] < 30000:
                scenario = 'First-Time Buyer'
            elif savings[idx] < 60000:
                scenario = 'Move-Up Buyer'
            else:
                scenario = np.random.choice(['Move-Up Buyer', 'Investor'], p=[0.7, 0.3])
            housing_scenarios.append(scenario)

        # Create DataFrame
        df = pd.DataFrame({
            'household_id': [f'HH{str(i).zfill(6)}' for i in range(1, n_households + 1)],
            'age': ages,
            'household_size': household_sizes,
            'annual_income': np.round(annual_income, 0),
            'employment_sector': employment_sectors,
            'region': regions,
            'credit_score': credit_scores,
            'current_debt': np.round(current_debt, 0),
            'monthly_debt_payment': np.round(monthly_debt_payment, 0),
            'current_monthly_rent': np.round(current_rent, 0),
            'savings': np.round(savings, 0),
            'debt_to_income_ratio': np.round(debt_to_income, 3),
            'financial_risk_score': np.round(risk_score, 1),
            'housing_scenario': housing_scenarios
        })

        return df

    def amplify_edge_cases(self, df: pd.DataFrame, amplification_factor: float = 0.3) -> pd.DataFrame:
        """
        Amplify edge cases (high-risk and wealthy households) using synthetic data

        Args:
            df: Original household dataframe
            amplification_factor: Proportion of additional synthetic households to generate

        Returns:
            Amplified dataframe with additional edge case households
        """
        n_synthetic = int(len(df) * amplification_factor)

        # Generate high-risk households (top 10% risk score)
        high_risk_samples = df[df['financial_risk_score'] > df['financial_risk_score'].quantile(0.9)]
        n_high_risk = n_synthetic // 2

        synthetic_high_risk = []
        for _ in range(n_high_risk):
            base_household = high_risk_samples.sample(1).iloc[0].copy()
            synthetic_household = base_household.copy()
            synthetic_household['household_id'] = f'SYN{np.random.randint(100000, 999999)}'

            # Add noise while maintaining high risk
            synthetic_household['annual_income'] += np.random.normal(0, 5000)
            synthetic_household['current_debt'] += np.random.normal(0, 10000)
            synthetic_household['credit_score'] += np.random.randint(-20, 10)
            synthetic_household['savings'] += np.random.normal(0, 2000)

            # Recalculate derived fields
            synthetic_household['monthly_debt_payment'] = synthetic_household['current_debt'] * 0.01
            synthetic_household['debt_to_income_ratio'] = (
                synthetic_household['monthly_debt_payment'] / (synthetic_household['annual_income'] / 12)
            )

            synthetic_high_risk.append(synthetic_household)

        # Generate wealthy/low-risk households (bottom 10% risk score)
        low_risk_samples = df[df['financial_risk_score'] < df['financial_risk_score'].quantile(0.1)]
        n_low_risk = n_synthetic - n_high_risk

        synthetic_low_risk = []
        for _ in range(n_low_risk):
            base_household = low_risk_samples.sample(1).iloc[0].copy()
            synthetic_household = base_household.copy()
            synthetic_household['household_id'] = f'SYN{np.random.randint(100000, 999999)}'

            # Add noise while maintaining low risk
            synthetic_household['annual_income'] += np.random.normal(0, 8000)
            synthetic_household['current_debt'] += np.random.normal(0, 5000)
            synthetic_household['credit_score'] += np.random.randint(-10, 20)
            synthetic_household['savings'] += np.random.normal(0, 5000)

            # Recalculate derived fields
            synthetic_household['monthly_debt_payment'] = synthetic_household['current_debt'] * 0.01
            synthetic_household['debt_to_income_ratio'] = (
                synthetic_household['monthly_debt_payment'] / (synthetic_household['annual_income'] / 12)
            )

            synthetic_low_risk.append(synthetic_household)

        # Combine all data
        synthetic_df = pd.DataFrame(synthetic_high_risk + synthetic_low_risk)
        amplified_df = pd.concat([df, synthetic_df], ignore_index=True)

        return amplified_df

    def generate_household_cohort(
        self,
        n_households: int = 1000,
        amplify: bool = True,
        amplification_factor: float = 0.3
    ) -> pd.DataFrame:
        """
        Generate complete household cohort with optional amplification

        Args:
            n_households: Number of base households
            amplify: Whether to amplify edge cases
            amplification_factor: Proportion of synthetic households to add

        Returns:
            Complete household cohort dataframe
        """
        base_df = self.generate_base_population(n_households)

        if amplify:
            cohort_df = self.amplify_edge_cases(base_df, amplification_factor)
        else:
            cohort_df = base_df

        return cohort_df


if __name__ == "__main__":
    # Test the household generator
    generator = FloridaHouseholdGenerator(random_seed=42)
    households = generator.generate_household_cohort(n_households=1000, amplify=True)

    print("=" * 80)
    print("Florida Household Data Generator - Test Run")
    print("=" * 80)
    print(f"\nGenerated {len(households)} households")
    print(f"\nDataset shape: {households.shape}")
    print(f"\nFirst 5 households:")
    print(households.head())
    print(f"\nDataset summary:")
    print(households.describe())
    print(f"\nRegion distribution:")
    print(households['region'].value_counts())
    print(f"\nEmployment sector distribution:")
    print(households['employment_sector'].value_counts())
    print(f"\nHousing scenario distribution:")
    print(households['housing_scenario'].value_counts())

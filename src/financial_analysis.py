"""
Financial Analysis Module for Florida Housing Monte Carlo Simulations
Provides comprehensive analysis and visualization functions
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional
from scipy import stats


class FloridaHousingAnalyzer:
    """Comprehensive analysis tools for housing simulation results"""

    def __init__(self):
        """Initialize the analyzer with plotting defaults"""
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 10

    def generate_summary_statistics(self, results_df: pd.DataFrame) -> Dict:
        """
        Generate comprehensive summary statistics from simulation results

        Args:
            results_df: DataFrame with simulation results

        Returns:
            Dictionary with summary statistics
        """
        summary = {
            'total_households': len(results_df),
            'scenarios': {
                'distribution': results_df['scenario'].value_counts().to_dict(),
                'affordability_rates': {}
            },
            'overall_metrics': {
                'mean_affordability_rate': results_df['probability_affordable'].mean(),
                'mean_default_rate': results_df.get('probability_default', pd.Series([0])).mean(),
                'high_risk_households': (results_df.get('probability_affordable', pd.Series([1])) < 0.5).sum(),
                'low_risk_households': (results_df.get('probability_affordable', pd.Series([1])) > 0.8).sum()
            }
        }

        # Calculate affordability rates by scenario
        for scenario in results_df['scenario'].unique():
            scenario_data = results_df[results_df['scenario'] == scenario]
            summary['scenarios']['affordability_rates'][scenario] = {
                'mean': scenario_data['probability_affordable'].mean(),
                'std': scenario_data['probability_affordable'].std(),
                'median': scenario_data['probability_affordable'].median()
            }

        return summary

    def compare_scenarios_analysis(self, results_df: pd.DataFrame) -> pd.DataFrame:
        """
        Compare housing scenarios across different metrics

        Args:
            results_df: DataFrame with simulation results

        Returns:
            DataFrame with comparative analysis
        """
        comparison = []

        for scenario in results_df['scenario'].unique():
            scenario_data = results_df[results_df['scenario'] == scenario]

            comparison.append({
                'Scenario': scenario,
                'N_Households': len(scenario_data),
                'Mean_Affordability_Rate': scenario_data['probability_affordable'].mean(),
                'Mean_Default_Rate': scenario_data.get('probability_default', pd.Series([0])).mean(),
                'Mean_Equity_Built': scenario_data['equity_built'].apply(lambda x: x['mean'] if isinstance(x, dict) else 0).mean(),
                'Mean_Total_Cost': scenario_data['total_cost_paid'].apply(lambda x: x['mean'] if isinstance(x, dict) else 0).mean(),
                'Affordability_Rate_Std': scenario_data['probability_affordable'].std()
            })

        comparison_df = pd.DataFrame(comparison)
        comparison_df = comparison_df.sort_values('Mean_Affordability_Rate', ascending=False)

        return comparison_df

    def income_stratification_analysis(self, households_df: pd.DataFrame, results_df: pd.DataFrame) -> Dict:
        """
        Analyze outcomes by income stratification

        Args:
            households_df: Original household data
            results_df: Simulation results

        Returns:
            Dictionary with income-stratified analysis
        """
        # Merge to get income data
        merged = results_df.merge(households_df[['household_id', 'annual_income', 'region']],
                                  on='household_id', how='left')

        # Define income brackets (Florida-specific)
        merged['income_bracket'] = pd.cut(
            merged['annual_income'],
            bins=[0, 40000, 60000, 85000, 120000, 250000],
            labels=['Under $40k', '$40k-$60k', '$60k-$85k', '$85k-$120k', 'Over $120k']
        )

        income_analysis = {}

        for bracket in merged['income_bracket'].unique():
            if pd.isna(bracket):
                continue
            bracket_data = merged[merged['income_bracket'] == bracket]

            if len(bracket_data) > 0:
                income_analysis[str(bracket)] = {
                    'n_households': len(bracket_data),
                    'mean_affordability_rate': bracket_data['probability_affordable'].mean(),
                    'mean_default_rate': bracket_data.get('probability_default', pd.Series([0])).mean(),
                    'mean_equity': bracket_data['equity_built'].apply(lambda x: x['mean'] if isinstance(x, dict) else 0).mean(),
                    'mean_income': bracket_data['annual_income'].mean()
                }

        return income_analysis

    def region_analysis(self, households_df: pd.DataFrame, results_df: pd.DataFrame) -> Dict:
        """
        Analyze outcomes by Florida region

        Args:
            households_df: Original household data
            results_df: Simulation results

        Returns:
            Dictionary with region-specific analysis
        """
        # Merge to get region data
        merged = results_df.merge(households_df[['household_id', 'region']],
                                  on='household_id', how='left')

        region_analysis = {}

        for region in merged['region'].unique():
            if pd.isna(region):
                continue
            region_data = merged[merged['region'] == region]

            if len(region_data) > 0:
                region_analysis[region] = {
                    'n_households': len(region_data),
                    'mean_affordability_rate': region_data['probability_affordable'].mean(),
                    'mean_default_rate': region_data.get('probability_default', pd.Series([0])).mean(),
                    'mean_equity': region_data['equity_built'].apply(lambda x: x['mean'] if isinstance(x, dict) else 0).mean()
                }

        return region_analysis

    def generate_visualization_report(
        self,
        households_df: pd.DataFrame,
        results_df: pd.DataFrame,
        output_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Generate comprehensive visualization report

        Args:
            households_df: Original household data
            results_df: Simulation results
            output_path: Optional path to save the figure

        Returns:
            Matplotlib figure object
        """
        fig = plt.figure(figsize=(16, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

        # Merge data
        merged = results_df.merge(households_df[['household_id', 'annual_income', 'region', 'financial_risk_score']],
                                  on='household_id', how='left')

        # 1. Affordability Rate by Scenario
        ax1 = fig.add_subplot(gs[0, 0])
        scenario_afford = merged.groupby('scenario')['probability_affordable'].mean().sort_values()
        scenario_afford.plot(kind='barh', ax=ax1, color='steelblue')
        ax1.set_xlabel('Mean Affordability Rate')
        ax1.set_title('Affordability Rate by Scenario')
        ax1.set_xlim(0, 1)

        # 2. Default Rates
        ax2 = fig.add_subplot(gs[0, 1])
        if 'probability_default' in merged.columns:
            default_rates = merged.groupby('scenario')['probability_default'].mean().sort_values()
            default_rates.plot(kind='barh', ax=ax2, color='coral')
            ax2.set_xlabel('Mean Default Rate')
            ax2.set_title('Default Rate by Scenario')
            ax2.set_xlim(0, 0.5)

        # 3. Equity Built Distribution
        ax3 = fig.add_subplot(gs[0, 2])
        equity_by_scenario = []
        scenario_labels = []
        for scenario in merged['scenario'].unique():
            scenario_data = merged[merged['scenario'] == scenario]
            equity_values = scenario_data['equity_built'].apply(lambda x: x['mean'] if isinstance(x, dict) else 0)
            equity_by_scenario.append(equity_values)
            scenario_labels.append(scenario)
        ax3.boxplot(equity_by_scenario, labels=scenario_labels)
        ax3.set_ylabel('Equity Built ($)')
        ax3.set_title('Equity Distribution by Scenario')
        ax3.tick_params(axis='x', rotation=45)

        # 4. Affordability by Income
        ax4 = fig.add_subplot(gs[1, 0])
        merged['income_bracket'] = pd.cut(
            merged['annual_income'],
            bins=[0, 40000, 60000, 85000, 120000, 250000],
            labels=['<$40k', '$40-60k', '$60-85k', '$85-120k', '>$120k']
        )
        income_afford = merged.groupby('income_bracket')['probability_affordable'].mean()
        income_afford.plot(kind='bar', ax=ax4, color='teal')
        ax4.set_xlabel('Income Bracket')
        ax4.set_ylabel('Mean Affordability Rate')
        ax4.set_title('Affordability by Income Level')
        ax4.tick_params(axis='x', rotation=45)

        # 5. Affordability by Region
        ax5 = fig.add_subplot(gs[1, 1])
        region_afford = merged.groupby('region')['probability_affordable'].mean().sort_values()
        region_afford.plot(kind='barh', ax=ax5, color='green')
        ax5.set_xlabel('Mean Affordability Rate')
        ax5.set_title('Affordability by Florida Region')

        # 6. Risk Score vs Affordability
        ax6 = fig.add_subplot(gs[1, 2])
        ax6.scatter(merged['financial_risk_score'], merged['probability_affordable'], alpha=0.3)
        ax6.set_xlabel('Financial Risk Score')
        ax6.set_ylabel('Probability of Affordability')
        ax6.set_title('Risk Score vs Affordability')
        ax6.axhline(y=0.5, color='r', linestyle='--', label='50% Affordability')
        ax6.legend()

        # 7. Scenario Comparison Heatmap
        ax7 = fig.add_subplot(gs[2, :2])
        comparison_metrics = []
        for scenario in merged['scenario'].unique():
            scenario_data = merged[merged['scenario'] == scenario]
            comparison_metrics.append({
                'Affordability': scenario_data['probability_affordable'].mean(),
                'Default Risk': scenario_data.get('probability_default', pd.Series([0])).mean(),
                'Equity (scaled)': scenario_data['equity_built'].apply(lambda x: x['mean'] if isinstance(x, dict) else 0).mean() / 100000,
                'Total Cost (scaled)': scenario_data['total_cost_paid'].apply(lambda x: x['mean'] if isinstance(x, dict) else 0).mean() / 100000
            })
        heatmap_df = pd.DataFrame(comparison_metrics, index=merged['scenario'].unique())
        sns.heatmap(heatmap_df.T, annot=True, fmt='.3f', cmap='RdYlGn', ax=ax7, cbar_kws={'label': 'Score'})
        ax7.set_title('Scenario Comparison Heatmap')

        # 8. Affordability Distribution
        ax8 = fig.add_subplot(gs[2, 2])
        ax8.hist(merged['probability_affordable'], bins=30, color='skyblue', edgecolor='black')
        ax8.axvline(merged['probability_affordable'].mean(), color='red', linestyle='--', label='Mean')
        ax8.axvline(merged['probability_affordable'].median(), color='green', linestyle='--', label='Median')
        ax8.set_xlabel('Probability of Affordability')
        ax8.set_ylabel('Number of Households')
        ax8.set_title('Overall Affordability Distribution')
        ax8.legend()

        plt.suptitle('Florida Housing Affordability - Monte Carlo Analysis Report', fontsize=16, y=0.995)

        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')

        return fig

    def export_detailed_report(
        self,
        households_df: pd.DataFrame,
        results_df: pd.DataFrame,
        output_path: str
    ) -> None:
        """
        Export detailed analysis report to CSV

        Args:
            households_df: Original household data
            results_df: Simulation results
            output_path: Path to save the CSV report
        """
        # Merge data
        merged = results_df.merge(households_df, on='household_id', how='left')

        # Create detailed report
        report_data = []

        for idx, row in merged.iterrows():
            report_data.append({
                'Household_ID': row['household_id'],
                'Scenario': row['scenario'],
                'Annual_Income': row['annual_income'],
                'Region': row['region'],
                'Credit_Score': row['credit_score'],
                'Financial_Risk_Score': row['financial_risk_score'],
                'Probability_Affordable': row['probability_affordable'],
                'Probability_Default': row.get('probability_default', 0),
                'Mean_Equity_Built': row['equity_built']['mean'] if isinstance(row['equity_built'], dict) else 0,
                'Mean_Total_Cost': row['total_cost_paid']['mean'] if isinstance(row['total_cost_paid'], dict) else 0,
                'Time_Horizon_Years': row['time_horizon_years']
            })

        report_df = pd.DataFrame(report_data)
        report_df.to_csv(output_path, index=False)
        print(f"Detailed report exported to: {output_path}")


if __name__ == "__main__":
    print("=" * 80)
    print("Florida Housing Financial Analysis Module - Test Run")
    print("=" * 80)
    print("\nThis module provides comprehensive analysis tools for housing simulations.")
    print("Import this module in your main application to access analysis functions.")

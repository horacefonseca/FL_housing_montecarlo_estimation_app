"""
Helper functions for Gemini AI integration and report generation
"""

import streamlit as st
import pandas as pd


def create_gemini_button_with_report(report_text: str, stage_name: str):
    """
    Creates a Gemini button with copy-to-clipboard functionality

    Args:
        report_text: Structured report text (max 500 chars)
        stage_name: Name of the analysis stage
    """
    # Ensure report is max 500 characters
    if len(report_text) > 500:
        report_text = report_text[:497] + "..."

    col1, col2 = st.columns([3, 1])

    with col1:
        # Copy button with report text
        st.text_area(
            f"📋 Copy this summary to ask Gemini",
            value=report_text,
            height=150,
            key=f"gemini_report_{stage_name}",
            help="Copy this text and paste in Gemini to get AI interpretation"
        )

    with col2:
        st.markdown("### Ask Gemini")
        st.markdown(
            """
            <a href="https://gemini.google.com/app" target="_blank">
                <img src="https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d4735304ff6292a690345.svg"
                     width="40" height="40" style="vertical-align: middle;">
                <br>
                <button style="
                    background-color: #4285f4;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 14px;
                    margin-top: 10px;
                ">Ask Gemini</button>
            </a>
            """,
            unsafe_allow_html=True
        )
        st.caption("Copy text above, then click to open Gemini")


def generate_household_report(df: pd.DataFrame) -> str:
    """Generate structured report for household generation stage"""
    report = f"""FLORIDA HOUSING DATA SUMMARY
Total: {len(df)} households
Income: Mean ${df['annual_income'].mean():,.0f}, Median ${df['annual_income'].median():,.0f}
Credit: Mean {df['credit_score'].mean():.0f}, Range {df['credit_score'].min():.0f}-{df['credit_score'].max():.0f}
Savings: Mean ${df['savings'].mean():,.0f}
Risk Score: Mean {df['financial_risk_score'].mean():.1f}/100
Top Regions: {', '.join(df['region'].value_counts().head(3).index.tolist())}
Top Sectors: {', '.join(df['employment_sector'].value_counts().head(3).index.tolist())}

Question: What insights can you provide about this Florida household dataset?"""

    return report[:500]


def generate_simulation_report(results_df: pd.DataFrame, params: dict) -> str:
    """Generate structured report for simulation results"""
    overall_afford = results_df['probability_affordable'].mean() * 100
    overall_default = results_df.get('probability_default', pd.Series([0])).mean() * 100

    # Handle equity_built which may be dict or float
    if 'equity_built' in results_df.columns:
        equity_values = results_df['equity_built'].apply(lambda x: x['mean'] if isinstance(x, dict) else x)
        mean_equity = equity_values.mean()
    else:
        mean_equity = 0

    # Handle total_cost which may be dict or float
    if 'total_cost' in results_df.columns:
        cost_values = results_df['total_cost'].apply(lambda x: x['mean'] if isinstance(x, dict) else x)
        mean_cost = cost_values.mean()
    else:
        mean_cost = 0

    report = f"""MONTE CARLO SIMULATION RESULTS
Simulations: {params.get('num_simulations', 10000):,} per household
Time Horizon: {params.get('time_horizon', 10)} years
Sample Size: {params.get('sample_size', 100)} households

OVERALL METRICS:
Affordability Rate: {overall_afford:.1f}%
Default Risk: {overall_default:.1f}%
Mean Equity Built: ${mean_equity:,.0f}
Mean Total Cost: ${mean_cost:,.0f}

Question: What do these results tell about Florida housing affordability?"""

    return report[:500]


def generate_analysis_report(stats: dict) -> str:
    """Generate structured report for comprehensive analysis"""
    report = f"""FLORIDA HOUSING ANALYSIS
Total Scenarios: {stats.get('total_scenarios', 0)}
Overall Affordability: {stats.get('overall_affordability', 0):.1f}%
Overall Default Rate: {stats.get('overall_default', 0):.1f}%

SCENARIO COMPARISON:
"""

    if 'scenario_comparison' in stats:
        for scenario, metrics in list(stats['scenario_comparison'].items())[:3]:
            report += f"{scenario}: {metrics.get('affordability', 0):.0f}% afford, ${metrics.get('equity', 0):,.0f} equity\n"

    report += "\nQuestion: Which housing option is best for median-income Florida households?"

    return report[:500]


def generate_single_household_report(household: dict, results: dict) -> str:
    """Generate structured report for single household analysis"""
    report = f"""HOUSEHOLD PROFILE & RESULTS
Income: ${household.get('annual_income', 0):,.0f}/yr
Credit: {household.get('credit_score', 0):.0f}
Region: {household.get('region', 'N/A')}
Savings: ${household.get('savings', 0):,.0f}
Risk Score: {household.get('financial_risk_score', 0):.1f}/100

SCENARIO RESULTS:
"""

    for scenario, metrics in list(results.items())[:3]:
        afford = metrics.get('probability_affordable', 0) * 100
        equity = metrics.get('mean_equity_built', 0)
        report += f"{scenario}: {afford:.0f}% afford, ${equity:,.0f} equity\n"

    report += f"\nRecommended: {results.get('recommended_scenario', 'N/A')}\n"
    report += "Question: What should this household do and why?"

    return report[:500]


def add_sensitivity_sliders():
    """Add parameter sensitivity adjustment sliders to sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔧 Adjust Assumptions")

    income_growth = st.sidebar.slider(
        "Annual Income Growth",
        min_value=-5.0,
        max_value=10.0,
        value=3.0,
        step=0.5,
        format="%.1f%%",
        help="Expected annual income growth rate"
    )

    insurance_increase = st.sidebar.slider(
        "Hurricane Insurance Annual Increase",
        min_value=5.0,
        max_value=25.0,
        value=15.0,
        step=1.0,
        format="%.0f%%",
        help="Expected annual increase in hurricane insurance"
    )

    appreciation_rate = st.sidebar.slider(
        "Home Appreciation Rate",
        min_value=-2.0,
        max_value=8.0,
        value=4.0,
        step=0.5,
        format="%.1f%%",
        help="Expected annual home value appreciation"
    )

    interest_rate = st.sidebar.slider(
        "Mortgage Interest Rate",
        min_value=3.0,
        max_value=9.0,
        value=6.5,
        step=0.25,
        format="%.2f%%",
        help="Mortgage interest rate assumption"
    )

    affordability_threshold = st.sidebar.slider(
        "Affordability Threshold (% of income)",
        min_value=28.0,
        max_value=50.0,
        value=43.0,
        step=1.0,
        format="%.0f%%",
        help="Maximum % of income for housing costs"
    )

    return {
        'income_growth': income_growth / 100,
        'insurance_increase': insurance_increase / 100,
        'appreciation_rate': appreciation_rate / 100,
        'interest_rate': interest_rate / 100,
        'affordability_threshold': affordability_threshold / 100
    }


def interpret_results_locally(affordability: float, income: float, scenario: str, credit_score: float) -> str:
    """
    Local rule-based interpretation when AI is not available
    """
    if affordability < 20:
        risk_level = "⚠️ HIGH RISK"
        interpretation = f"Monthly housing costs likely exceed safe debt-to-income threshold. "
        if income < 50000:
            interpretation += "Consider: Keep renting until income increases, or target lower-priced areas. "
        elif credit_score < 650:
            interpretation += "Improve credit score to access better interest rates. "
        else:
            interpretation += "Build larger emergency fund (6+ months) before buying. "

    elif affordability < 50:
        risk_level = "⚡ MODERATE RISK"
        interpretation = f"{affordability:.0f}% of scenarios succeed. "
        interpretation += "Risk factors: Insurance volatility, income stability. "
        interpretation += "Recommendation: Build 6-month emergency fund, consider FHA starter home. "

    elif affordability < 75:
        risk_level = "✅ MODERATE"
        interpretation = f"{affordability:.0f}% success rate indicates good alignment. "
        interpretation += "This scenario is manageable with proper financial planning. "
        interpretation += "Maintain emergency savings and monitor insurance costs. "

    else:
        risk_level = "✅ LOW RISK"
        interpretation = f"{affordability:.0f}% success rate shows strong affordability. "
        interpretation += "This scenario aligns well with your financial profile. "
        interpretation += "Consider building equity through homeownership. "

    return f"**{risk_level}**: {interpretation}"

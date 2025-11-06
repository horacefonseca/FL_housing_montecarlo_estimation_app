# Executive Summary: Florida Housing Affordability Analyzer

**Author:** Horacio Fonseca, Data Analyst
**Date:** January 2025
**Project Type:** Monte Carlo Decision Support Application

---

## Problem Statement

Florida residents face critical housing decisions amid unprecedented market volatility, with hurricane insurance premiums increasing 10-20% annually and regional price disparities exceeding 35%. Traditional affordability analysis fails to capture the compounding uncertainties of income variability, interest rate fluctuations, property value changes, and insurance shocks over multi-year horizons.

## Solution Approach

This project implements a Monte Carlo simulation framework with 10,000+ scenarios per household, modeling four housing options: Keep Renting, Buy Starter Home ($200k-$300k), Buy Standard Home ($300k-$500k), and Buy Premium Home ($500k+). The analysis incorporates Florida-specific factors including regional price multipliers, hurricane insurance costs, property tax structures, and employment sector income dynamics.

## Key Findings

Results demonstrate that affordability rates vary dramatically by scenario and household profile. For median-income households, starter homes show 70-80% affordability with $50k-$85k equity potential over 10 years, while premium homes carry 3-4× higher default risk despite $150k+ equity upside. Hurricane insurance represents 15-25% of total homeownership costs in high-risk regions, fundamentally altering rent-versus-buy calculations.

## Business Value

The interactive Streamlit application enables data-driven housing decisions for 100,000+ Florida households annually. Stakeholders include home buyers seeking personalized recommendations, financial advisors requiring risk quantification tools, lenders assessing default probabilities beyond traditional metrics, and policymakers understanding affordability crisis dimensions. The Monte Carlo approach provides probability distributions rather than point estimates, supporting risk-adjusted decision-making under uncertainty.

**Repository:** https://github.com/horacefonseca/FL_housing_montecarlo_estimation_app
**Technology:** Python 3.10, NumPy, Pandas, Streamlit, Monte Carlo Simulation

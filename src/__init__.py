"""
Florida Housing Affordability Analysis Package

This package provides tools for generating synthetic household data,
running Monte Carlo housing simulations, and analyzing affordability outcomes.
"""

__version__ = "1.0.0"
__author__ = "Horace Fonseca"

from .household_generator import FloridaHouseholdGenerator
from .monte_carlo_housing import MonteCarloHousingSimulator, HousingScenarioParameters
from .financial_analysis import FloridaHousingAnalyzer

__all__ = [
    'FloridaHouseholdGenerator',
    'MonteCarloHousingSimulator',
    'HousingScenarioParameters',
    'FloridaHousingAnalyzer'
]

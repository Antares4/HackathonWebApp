import numpy as np
import pandas as pd

# 
def calculateAnnualCaptureCost(annualCarbonEmissions, annualCaptureCost):
    return annualCarbonEmissions / annualCaptureCost

#
def calculatesStorageCost(annualCarbonEmissions, costOfStorage):
    return annualCarbonEmissions / costOfStorage


# Returns the annual cost in dollars $ of the transportation cost
#  
def getTransportCost(annualCarbonEmissions, costOfTransport):
    return annualCarbonEmissions / costOfTransport

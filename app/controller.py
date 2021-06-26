from types import ClassMethodDescriptorType
from flask import url_for
import csv
from app.model import asset, component
from app import db
years = [2022, 2025, 2030, 2035, 2040, 2045, 2050] 
NONE = 0
CARB = 1
HYDR = 2
carbon_file = "Carbon.csv"
hydrogen_file = "Hydrogen.csv"
def getAttrbute(file_in, year, type, col):
    with open(file_in) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[0] == str(type) and row[1] == str(year):
                return float(row[col])


def getStartingYear(year):
    for yr in years:
        if int(year) >= yr:
            print("success")
            return yr
    return None

def getDuration(start, end):
    li = []
    this_year = start
    print(start,end)
    while this_year < end:
        for i in range(len(years)):
            if this_year >= years[i] and years[i] not in li:
                print(this_year)
                li.append(this_year)
                if i < len(years)-1: 
                    if years[i+1] < end:
                        this_year = years[i+1]
                    else: 
                        this_year = end
                else:
                    this_year = end
    li.append(end)
    l = len(li)
    x = 0
    while x < l:
        if li[x]<start:
            li.pop(x)
            l-=1
        x+=1
    return li


def getComponentsById(id):
    comp = component.query.filter_by(asset_id=id).all()
    return comp

def decomissionCost(asset_id, exclude):
    components = getComponentsById(asset_id)
    totalCost = 0
    for item in components:
        if item.HydroProd and exclude == HYDR:
            continue
        elif item.CarbProd and exclude == CARB:
            continue
        totalCost += item.decomCost_p_unit * item.decomUnit
    return totalCost

def remainingDecomission(asset_id, include):
    components = getComponentsById(asset_id)
    totalCost = 0
    for item in components:
        if item.HydroProd and include == HYDR:
            totalCost += item.decomCost_p_unit * item.decomUnit
        elif item.CarbProd and include == CARB:
            totalCost += item.decomCost_p_unit * item.decomUnit
        else:
            continue
    return totalCost

def HydrogenProduction(asset_id):
    thisAsset = getAssetById(asset_id)
    startingYear = getStartingYear(thisAsset.yearOfDepletion)
    duration = getDuration(thisAsset.yearOfDepletion, thisAsset.yearOfDecommission)
    decomission = decomissionCost(asset_id, HYDR)
    categories = ["Alkaline", "PEM"]
    data = []
    thisYear = thisAsset.yearOfDepletion
    for typ in categories:
        print(1)
        index = 0
        cost = []
        yearlyCost = []
        while thisYear < duration[len(duration)-1]:
            if thisYear not in years:
                thisYear = startingYear
            print("this year is", thisYear)
            transFee = getAttrbute(hydrogen_file, thisYear, typ, 4) * thisAsset.hydrTrans / 100
            productionFee = getAttrbute(hydrogen_file, thisYear, typ, 3) 
            if thisAsset.stormthd == "Gas":
                storageFee = getAttrbute(hydrogen_file, thisYear, typ, 5) 
            else:
                storageFee = getAttrbute(hydrogen_file, thisYear, typ, 6) 
            salePrice = getAttrbute(hydrogen_file, thisYear, typ, 7)
            balance = transFee + productionFee + storageFee - salePrice
            cost.append(round(balance,2))
            index+=1
            thisYear = duration[index]
            totalCost = 0
        for i in range(len(cost)):
            thisCost = int(cost[i]*thisAsset.expHydrProduction)
            yearlyCost.append(thisCost)
            if i == 0:
                numYear = duration[i]
            else: 
                numYear = duration[i] - duration[i-1]
            print("ny",numYear)
            totalCost += numYear*thisCost
        remainingFund = thisAsset.budget - (totalCost+decomission)
        remaining = remainingDecomission(asset_id, HYDR)
        info = {
            "type": typ,
            "Cost": cost,
            "totalCost":totalCost,
            "yearlyCost": yearlyCost,
            "duration": duration,
            "remaining":remaining,
            "remainingFund":remainingFund
        }
        thisYear = thisAsset.yearOfDepletion
        data.append(info)
    return data

def carbonCaptureCost(asset_id):
    thisAsset = getAssetById(asset_id)
    startingYear = getStartingYear(thisAsset.yearOfDepletion)
    duration = getDuration(thisAsset.yearOfDepletion, thisAsset.yearOfDecommission)
    decomission = decomissionCost(asset_id, CARB)
    categories = ["Onshore", "Offshore"]
    data = []
    for typ in categories:
        index = 0
        cost = []
        yearlyCost = []
        thisYear = thisAsset.yearOfDepletion
        while thisYear < duration[len(duration)-1]:
            if thisYear not in years:
                thisYear = startingYear
            transFee = getAttrbute(carbon_file, thisYear, typ, 3) * thisAsset.carbTrans / 100
            captureFee = getAttrbute(carbon_file, thisYear, typ, 2) 
            storageFee = getAttrbute(carbon_file, thisYear, typ, 4)
            salePrice = getAttrbute(carbon_file, thisYear, typ, 5)
            balance = transFee + captureFee + storageFee - salePrice
            cost.append(round(balance,2))
            index+=1
            thisYear = duration[index]
        for i in range(len(cost)):
            thisCost = int(cost[i]*thisAsset.expCarbProduction)
            yearlyCost.append(thisCost)
            if i == 0:
                numYear = duration[i]
            else: 
                numYear = duration[i] - duration[i-1]
            totalCost = 0
            totalCost += numYear*thisCost
            remainingFund = thisAsset.budget - (totalCost+decomission)
        remaining = remainingDecomission(asset_id, CARB)
        info = {
            "type": typ,
            "Cost": cost,
            "yearlyCost": yearlyCost,
            "duration": duration,
            "remaining":remaining,
            "remainingFund":remainingFund
        }
        thisYear = thisAsset.yearOfDepletion
        data.append(info)
    return data

def genReport(asset_id):
    thisAsset = getAssetById(asset_id)
    if thisAsset:
        if thisAsset.yearOfDepletion > thisAsset.yearOfDecommission:
            return "no action"
        else:
            decom = decomissionCost(asset_id, NONE)
            carbon = carbonCaptureCost(asset_id)
            Hydrogen = HydrogenProduction(asset_id)
            data = {
                "decom": decom,
                "carbon": carbon,
                "hydrogen": Hydrogen,
            }
            return data
    else:
        return None

def getAssetIdByName(n):
    thisAsset = asset.query.filter_by(assetName=n).first()
    if not thisAsset:
        return None
    else: 
        return thisAsset.id

def getAssetById(id):
    thisAsset = asset.query.filter_by(id=id).first()
    if not thisAsset:
        return None
    else: 
        return thisAsset

def getAllAssets():
    return asset.query.all()

def getAllComponents():
    return component.query.all()

def removeComponent(cid):
    comp = component.query.filter_by(id=cid).first()
    db.session.delete(comp)
    db.session.commit()
    return True

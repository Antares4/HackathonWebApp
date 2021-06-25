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
        if year >= yr:
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

def carbonCaptureCost(asset_id):
    print("capture")
    thisAsset = getAssetById(asset_id)
    print("2")
    startingYear = getStartingYear(thisAsset.yearOfDepletion)
    print("3")
    duration = getDuration(thisAsset.yearOfDepletion, thisAsset.yearOfDecommission)
    print("4")
    decomission = decomissionCost(asset_id, CARB)
    categories = ["Onshore", "Offshore"]
    data = []
    for typ in categories:
        index = 0
        cost = []
        while startingYear < duration[len(duration)-1]:
            transFee = getAttrbute(carbon_file, startingYear, typ, 3) * thisAsset.carbTrans / 100
            captureFee = getAttrbute(carbon_file, startingYear, typ, 2) 
            storageFee = getAttrbute(carbon_file, startingYear, typ, 4)
            salePrice = getAttrbute(carbon_file, startingYear, typ, 5)
            balance = transFee + captureFee + storageFee - salePrice
            print(balance)
            cost.append(balance)
            index+=1
            startingYear = duration[index]
            print(startingYear)
        info = {
            "type": typ,
            "Cost": cost,
            "duration": duration
        }
        startingYear = getStartingYear(thisAsset.yearOfDepletion)
        print(info)
        data.append(info)
    return data

def genReport(asset_id):
    thisAsset = getAssetById(asset_id)
    if thisAsset:
        if thisAsset.yearOfDepletion > thisAsset.yearOfDecommission:
            return "no action"
        else:
            c = decomissionCost(asset_id, NONE)
            d = carbonCaptureCost(asset_id)
            return None
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

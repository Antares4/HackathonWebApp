from flask import url_for
from app.model import asset, component
from app import db


def getComponentsById(id):
    comp = component.query.filter_by(asset_id=id).all()
    return comp

def decomissionCost(asset_id):
    components = getComponentsById(asset_id)
    totalCost = 0
    for item in components:
        totalCost += item.decomCost_p_unit * item.decomUnit
    return totalCost

def carbonCaptureCost(asset_id):
    
    return None

def getAssetByName(n):
    thisAsset = asset.query.filter_by(assetName=n).first()
    if not thisAsset:
        return None
    else: 
        return thisAsset.id

def getAllAssets():
    return asset.query.all()

def getAllComponents():
    return component.query.all()

def removeComponent(cid):
    comp = component.query.filter_by(id=cid).first()
    db.session.delete(comp)
    db.session.commit()
    return True

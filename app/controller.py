from flask import url_for
from app.model import asset, component
from app import db


#creates user, validates and sets password 
#return flase on exception
def add():
    a = asset.query.filter_by(id=1).first()
    y = int(a.endofservice) + int(a.budget)
    print(y)
    return y

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
from flask import url_for
from app.model import asset
from app import db


#creates user, validates and sets password 
#return flase on exception
def add():
    a = asset.query.filter_by(id=1).first()
    y = int(a.endofservice) + int(a.budget)
    print(y)
    return y


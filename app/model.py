
from app import db
from flask_login import UserMixin
from datetime import datetime
from flask import url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash

class asset(UserMixin, db.Model):
    __tablename__ = 'asset'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    assetName = db.Column(db.String(100), nullable=False)
    yearOfDepletion = db.Column(db.Integer, nullable=False)
    yearOfDecommission = db.Column(db.Integer, nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    expCarbProduction = db.Column(db.Integer, nullable=False)
    carbTrans = db.Column(db.Integer, nullable=False)
    expHydrProduction = db.Column(db.Integer, nullable=False)
    hydrTrans = db.Column(db.Integer, nullable=False)
    stormthd = db.Column(db.String(100), nullable=False)
    components = db.relationship("component", backref="asset")

class component(UserMixin, db.Model):

    __tablename__ = 'components'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    componentName = db.Column(db.String(200), nullable=False)
    decomCost_p_unit = db.Column(db.Integer, nullable=False)
    decomUnit = db.Column(db.Integer, nullable=False)
    HydroProd = db.Column(db.Boolean, nullable=False)
    CarbProd = db.Column(db.Boolean, nullable=False)
    asset_id = db.Column(db.Integer, db.ForeignKey("asset.id"), nullable=False)

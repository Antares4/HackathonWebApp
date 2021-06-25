from app import db
from flask_login import UserMixin
from datetime import datetime
from flask import url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash

class asset(UserMixin, db.Model):
    __tablename__ = 'asset'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    endofservice = db.Column(db.String(100), nullable=False)
    budget = db.Column(db.String(96), nullable=False)
    Carbon_p_y = db.Column(db.String(128), nullable=False)
    components = db.relationship("component", backref="asset")

class component(UserMixin, db.Model):

    __tablename__ = 'components'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    decomCost_p_unit = db.Column(db.Integer, nullable=False)
    decomUnit = db.Column(db.Integer, nullable=False)
    CanBeUsedForHydrogenProduction = db.Column(db.Boolean, nullable=False)
    asset_id = db.Column(db.Integer, db.ForeignKey("asset.id"), nullable=False)

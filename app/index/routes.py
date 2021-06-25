from flask import Flask, request, url_for, redirect, render_template, flash, jsonify
from app.index import bp
from app.index.forms import assetForm, componentForm
from app import db
from app.model import asset, component
from app.model import asset
from app.controller import add 
import json

#route to home page
@bp.route('/',methods=['GET', 'POST'])
@bp.route('/index',methods=['GET', 'POST'])
def index():
    form = assetForm()
    if form.validate_on_submit():
        asse = asset()
        asse.endofservice = form.endofservice.data
        asse.budget = form.budget.data
        asse.Carbon_p_y = form.Carbon_p_y.data
        db.session.add(asse)
        db.session.commit()
        x = add()
        return render_template('success.html', form=form, add=x)
    return render_template('index.html', form=form)

@bp.route('/index',methods=['GET', 'POST'])
def index():
    form = componentForm()
    if form.validate_on_submit():
        asse = asset()
        asse.endofservice = form.endofservice.data
        asse.budget = form.budget.data
        asse.Carbon_p_y = form.Carbon_p_y.data
        db.session.add(asse)
        db.session.commit()
        x = add()
        return render_template('success.html', form=form, add=x)
    return render_template('index.html', form=form)

    

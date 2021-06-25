
from flask import Flask, request, url_for, redirect, render_template, flash, jsonify
from app.index import bp
from app.index.forms import assetForm, componentForm
from app import db
from app.model import asset, component
from app.model import asset
from app.controller import add, getAssetByName
import json

#route to home page
@bp.route('/',methods=['GET', 'POST'])
@bp.route('/index',methods=['GET', 'POST'])
def index():
    form = assetForm()
    if form.validate_on_submit():
        asse = asset()
        asse.name = form.name.data
        asse.endofservice = form.endofservice.data
        asse.budget = form.budget.data
        asse.Carbon_p_y = form.Carbon_p_y.data
        db.session.add(asse)
        db.session.commit()
        x = add()
        return redirect(url_for('index.comp'))
    return render_template('index.html', form=form)

@bp.route('/comp',methods=['GET', 'POST'])
def comp():
    form = componentForm()
    if form.validate_on_submit():
        comp = component()
        comp.decomCost_p_unit = form.decomCost_p_unit.data
        comp.decomUnit = form.decomUnit.data
        comp.CanBeUsedForHydrogenProduction = form.CanBeUsedForHydrogenProduction.data
        a = getAssetByName(form.asset.data)
        comp.asset_id = a
        db.session.add(comp)
        db.session.commit()
        if form.moreComponents:
            return redirect(url_for('index.comp'))
        else:
            x = add()
            return render_template('success.html', form=form, add=a)
    return render_template('index.html', form=form)

    

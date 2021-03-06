
from flask import Flask, request, url_for, redirect, render_template, flash, jsonify
from app.index import bp
from app.index.forms import assetForm, componentForm
from app import db
from app.model import asset, component
from app.model import asset
from app.controller import getAssetIdByName, getAllAssets, getAllComponents, removeComponent, genReport, getAssetById
import json

#route to home page ssss
@bp.route('/',methods=['GET', 'POST'])
@bp.route('/index/<type>',methods=['GET', 'POST'])
def index(type="asset"):
    existing_assets = getAllAssets()
    existing_components = getAllComponents()
    export = {
        "assets":existing_assets,
        "components":existing_components
    }
    if type == "component":
        form = componentForm()
        print("component")
        if form.validate_on_submit():
            comp = component()
            comp.componentName = form.componentName.data
            comp.decomCost_p_unit = form.decomCost_p_unit.data
            comp.decomUnit = form.decomUnit.data
            comp.HydroProd = form.HydroProd.data
            comp.CarbProd = form.CarbProd.data
            comp.asset_id = getAssetIdByName(form.asset.data)
            if comp.asset_id:
                db.session.add(comp)
                db.session.commit()
                return redirect(url_for('index.index',type="component"))
            else:
                print("not exist")
                flash("asset does not exist")
                return redirect(url_for('index.index',type="component"))
        return render_template('index.html', form=form, types="component", data=export)
    else:
        form = assetForm()
        print("asset")
        if form.validate_on_submit():
            asse = asset()
            asse.assetName = form.name.data
            asse.yearOfDepletion = form.yearOfDepletion.data
            asse.yearOfDecommission = form.yearOfDecommission.data
            asse.budget = form.budget.data
            asse.expCarbProduction = form.expCarbCapture.data
            asse.carbTrans = form.carbTrans.data
            asse.expHydrProduction = form.expHydrProduction.data
            asse.hydrTrans = form.hydrTrans.data
            asse.stormthd = form.stormthd.data
            db.session.add(asse)
            db.session.commit()
            return redirect(url_for('index.index',type="asset"))
        return render_template('index.html', form=form, types="asset", data=export)


@bp.route('/delete/<id>')
def delete(id):
    print("id is",id)
    removeComponent(id)
    existing_assets = getAllAssets()
    existing_components = getAllComponents()
    export = {
        "assets":existing_assets,
        "components":existing_components
    }
    form = componentForm()
    return render_template('index.html', form=form, types="component", data=export)

@bp.route('/report/<id>')
def report(id):
    data = genReport(id)
    thisAsset = getAssetById(id)
    form = componentForm()
    return render_template("report.html", data=data, thisAsset=thisAsset)
    #return render_template('index.html', form=form, types="component", data=export)
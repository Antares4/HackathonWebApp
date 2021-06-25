from flask import Flask, request, url_for, redirect, render_template, flash, jsonify
from app.index import bp
from app.index.forms import assetForm
from app import db
from app.model import asset, component
from app.model import asset
import json

#route to home page
@bp.route('/',methods=['GET', 'POST'])
@bp.route('/index',methods=['GET', 'POST'])
def index():
    form = assetForm()
    if form.validate_on_submit():
        asse = asset()
        asse.eof = form.endofservice.data
        asse.carbon = form.Carbon_p_y.data
        return render_template('success.html', form=form)
    return render_template('index.html', form=form)

    

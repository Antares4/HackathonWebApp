from flask import Flask, request, url_for, redirect, render_template, flash, jsonify
from app.register import bp
from app.register.forms import RegisterForm
from app.model import users
from app.controller import createUser, removeUser
from flask_login import login_required, current_user
from app import db
from datetime import datetime


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    #submmit form validates 
    if form.validate_on_submit():
        user = users()
        user.username = form.username.data
        user.email = form.email.data
        user.firstname = form.firstname.data
        user.lastname = form.lastname.data
        user.joinedAt = datetime.utcnow()
        #check password match
        if(form.password.data != form.confirmpassword.data):
            flash("password does not match, try again")
            return render_template("register.html", form=form)
        #create user 
        elif createUser(user, form.password.data):
            return redirect(url_for('auth.login'))
        #user exists
        else:
            return render_template("register.html", form=form, userExist="[Username already exist.]")
    #form submit doesnot validate
    elif(request.method == 'POST' and not form.validate_on_submit()):
        flash('unable to register')
    return render_template('register.html', title='Register', form=form)

#delete user
@bp.route('/deleteUSR/<userId>', methods=['GET'])
@login_required
def deleteUser(userId):
    if not current_user.isAdmin:
        return redirect(url_for("index.index"))
    else:
        if not removeUser(userId):
            flash("unable to remove user")
        return redirect(url_for("index.profile", userId=current_user.id))

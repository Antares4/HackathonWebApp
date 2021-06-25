from flask import Flask, request, url_for, redirect, render_template, flash, jsonify
from app.auth import bp
from app.auth.forms import LoginForm
from app.model import users
from app.controller import updateLoginTime
from app import db
from flask_login import current_user, login_user



#login route
@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    #validate on submit
    if form.validate_on_submit():
        user = users.query.filter_by(username=form.username.data).first()
        #user exist
        if user:
            #check password
            if user.check_password(form.password.data):
                login_user(user,remember=form.remember_me.data)
                updateLoginTime(user)
                return redirect(url_for('index.index', name=user.username))
            # incorrect password
            else:
                error="[Incorrect password]"
                return render_template('login.html', title='Sign In', form=form,  msg=error)
        #user not exist
        else:
            error = "[Invalid user name]"
            return render_template('login.html', title='Sign In', form=form,  msg=error)
    #did not validate on submit
    elif(request.method == 'POST' and form.validate_on_submit() != True):
        error = "[Empty field]"
        return render_template('login.html', title='Sign In', form=form,msg=error)
    #defult
    return render_template('login.html', title='Sign In', form=form)


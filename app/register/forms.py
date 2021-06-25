from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, length, EqualTo
from app.model import users

# register form
class RegisterForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
                             DataRequired(), length(min=6, max=80)])
    confirmpassword = PasswordField('Confirm Password', validators=[
                                    DataRequired(), length(min=6, max=80), EqualTo('password')])
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField('Sign up')

    #custom username validation
    def validate_username(self, username):
        usr = users.query.filter_by(username=username.data).first()
        if usr is not None:
            print("raised")
            raise ValidationError('Please enter a different username.')

    #custom email validation
    def validate_email(self, email):
        usr = users.query.filter_by(email=email.data).first()
        if usr is not None:
            print("raised")
            raise ValidationError('Please enter a different email address.')

    #custom password validation
    def validate_password(self, password):
        if len(password.data) < 6:
            print("raised")
            raise ValidationError("Password has to be atleast 6 characters long")

from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField, BooleanField, SelectField
from wtforms.validators import DataRequired 

# register form
class assetForm(FlaskForm):
    name = StringField('Asset Name', validators=[DataRequired()])
    yearOfDepletion = IntegerField('Expected depletion time(Year)', validators=[DataRequired()])
    yearOfDecommission = IntegerField('Expected year of Decommission', validators=[DataRequired()])
    budget = IntegerField('Decommissioning budget(USD)', validators=[DataRequired()])
    expCarbCapture= IntegerField('Expected carbon capture per year(ton)', validators=[DataRequired()])
    carbTrans = IntegerField('Carbon transport distance required(Km)', validators=[DataRequired()])
    expHydrProduction = IntegerField('Expected Hydrogen production per year(ton)', validators=[DataRequired()])
    hydrTrans = IntegerField('Carbon transport distance required(Km)', validators=[DataRequired()])
    stormthd = SelectField('Method of storage(Hydrogen)', choices=[('Gas', 'Gas'), ('Liquid', 'Liquid')])
    submit = SubmitField('Submit')

class componentForm(FlaskForm):
    asset = StringField("Parent Asset", validators=[DataRequired()])
    componentName = StringField("Component Name", validators=[DataRequired()])
    decomCost_p_unit = IntegerField('Decommission cost per unit', validators=[DataRequired()])
    decomUnit = IntegerField('Units Included', validators=[DataRequired()])
    HydroProd = BooleanField('Reuseable for Hydrogen production')
    CarbProd = BooleanField('Reuseable for Carbon capture')
    submit = SubmitField('Submit')
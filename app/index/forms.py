from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField
from wtforms.validators import DataRequired 

# register form
class assetForm(FlaskForm):
    endofservice = IntegerField('endofservice', validators=[DataRequired()])
    budget = IntegerField('budget', validators=[DataRequired()])
    Carbon_p_y = IntegerField('Carbon_p_y', validators=[DataRequired()])
    submit = SubmitField('submit')

class componentForm(FlaskForm):
    asset = StringField("parrent asset")
    decomCost_p_unit = IntegerField('User Name', validators=[DataRequired()])
    decomUnit = IntegerField('First Name', validators=[DataRequired()])
    CanBeUsedForHydrogenProduction = IntegerField('Last name', validators=[DataRequired()])
    submit = SubmitField('submit')
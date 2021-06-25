from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField, BooleanField
from wtforms.validators import DataRequired 

# register form
class assetForm(FlaskForm):
    name = StringField('Asset Name', validators=[DataRequired()])
    endofservice = IntegerField('endofservice', validators=[DataRequired()])
    budget = IntegerField('budget', validators=[DataRequired()])
    Carbon_p_y = IntegerField('Carbon_p_y', validators=[DataRequired()])
    submit = SubmitField('NEXT')

class componentForm(FlaskForm):
    asset = StringField("parrent asset")
    decomCost_p_unit = IntegerField('User Name', validators=[DataRequired()])
    decomUnit = IntegerField('', validators=[DataRequired()])
    CanBeUsedForHydrogenProduction = BooleanField('Reuseable', validators=[DataRequired()])
    moreComponents = BooleanField("More assets", default=True)
    submit = SubmitField('finish')
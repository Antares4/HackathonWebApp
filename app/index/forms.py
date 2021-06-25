from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField, BooleanField
from wtforms.validators import DataRequired 

# register form
class assetForm(FlaskForm):
    name = StringField('Asset Name', validators=[DataRequired()])
    endofservice = IntegerField('Expected end of service', validators=[DataRequired()])
    budget = IntegerField('budget for recommission', validators=[DataRequired()])
    Carbon_p_y = IntegerField('Carbon emission per year(ton)', validators=[DataRequired()])
    submit = SubmitField('Submit')

class componentForm(FlaskForm):
    asset = StringField("Parent Asset", validators=[DataRequired()])
    componentName = StringField("Component Name", validators=[DataRequired()])
    decomCost_p_unit = IntegerField('Decomposition cost per unit', validators=[DataRequired()])
    decomUnit = IntegerField('Units Included', validators=[DataRequired()])
    CanBeUsedForHydrogenProduction = BooleanField('Reuseable')
    submit = SubmitField('Submit')
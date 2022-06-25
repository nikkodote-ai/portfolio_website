from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,  BooleanField, FloatField, IntegerField, SelectField, DateField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField

#WTForm
class CreateForm(FlaskForm):
    post_url = StringField("Post URL", validators=[DataRequired()])
    title = StringField("Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Image URL", validators=[DataRequired()])
    type = SelectField("Post Type", choices=[("blog", "Blog"), ("app", "App"), ("other", "External Site URL to be used")])
    tags = StringField("Tags")
    body = CKEditorField("Body")
    submit = SubmitField()


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")


class LoginForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")

class MorseCodeForm(FlaskForm):
    raw_input = CKEditorField("Input", validators=[DataRequired()], render_kw={"style":"color:black;font-size:1.5rem;font-family: 'Libre Baskerville', serif;"})
    submit = SubmitField("Translate!", render_kw={"style":"font-size:2rem; font-weight:600; color: coral; width:100%; text-align:center;"})

class StrokeForm(FlaskForm):
    age = IntegerField("Age", validators=[DataRequired()])
    hypertension = BooleanField("History of Hypertension", )
    heart_disease = BooleanField("History of Heart Disease")
    ever_married = BooleanField('Ever Married?',)
    residence_type = SelectField("Residence Type", choices=[(0, "Rural"),(1, "Urban")], validators=[DataRequired()])
    work_type = SelectField("Work Type", choices = [("govt_job","Government Job"),("never_worked", "Never Worked"),("private", "Private"),("self_employed", "Self-employed"), ("children", "Children")], validators = [DataRequired(),])
    avg_glucose_level = FloatField("Average Glucose Level (mg/dl)")
    bmi = FloatField("BMI", validators=[DataRequired()])
    gender = SelectField("Gender",choices = [("male", "Male"), ("female", "Female"), ("other", "Other")], validators=[DataRequired()])
    smoking_status = SelectField("Smoking Status", choices= [
        ("unknown", "Unknown"),("formerly_smoked", "Formerly Smoked"),("never_smoked","Never Smoked"),("smokes", "Smokes")],
                                 validators= [DataRequired()])
    style = {"style":"font-size:2rem; font-weight:600; color: seagreen; width:100%; text-align:center;" }
    submit = SubmitField(render_kw=style)

import os
import pickle

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

import model_stroke
import numpy as np
from forms import CreateForm

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# load model
model = pickle.load(open('../Stroke_Prediction-Web_Deployment/model.pkl', 'rb'))


@app.route("/", methods=['GET', 'POST'])
def home():
    form = CreateForm()
    if request.method == "POST":
        #onehot code some of the answers because that is what the model requires
        gender_onehot = {choice[0]:0 for choice in form.gender.choices}
        gender_onehot[form.gender.data] = 1
        print(gender_onehot)
        worktype_onehot = {choice[0]:0 for choice in form.work_type.choices}
        worktype_onehot[form.work_type.data] = 1
        print(worktype_onehot)
        smoking_status_onehot = {choice[0]:0 for choice in form.smoking_status.choices}
        smoking_status_onehot[form.smoking_status.data] = 1
        print(smoking_status_onehot)
        # collate users answer
        form_answers = [[
            form.age.data, int(form.hypertension.data),
            int(form.heart_disease.data), int(form.ever_married.data),int(form.residence_type.data),
            form.avg_glucose_level.data, form.bmi.data,
            gender_onehot['female'], gender_onehot['male'], gender_onehot['other'],
            worktype_onehot['govt_job'], worktype_onehot['never_worked'], worktype_onehot['private'],
            worktype_onehot['self_employed'], worktype_onehot['children'],
            smoking_status_onehot['unknown'], smoking_status_onehot['formerly_smoked'],
            smoking_status_onehot['never_smoked'], smoking_status_onehot['smokes']]]
        form_answers_np = np.array(form_answers)
        prediction = model.predict(form_answers)

        return render_template("predict.html", form=form, prediction=prediction)

    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)

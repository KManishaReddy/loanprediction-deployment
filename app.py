from flask import Flask, render_template, request,url_for
import pickle
import numpy as np
from flask_cors import CORS,cross_origin

app = Flask(__name__)

model=pickle.load(open('model.pkl','rb'))

@app.route('/')
@cross_origin()
def index():
    return render_template('mypage.html')
    
@app.route('/predict',methods=['POST','GET'])
@cross_origin()
def predict():
    list_of_cols =['Gender','Married','Education','Self_Employed','ApplicantIncome','CoapplicantIncome','LoanAmount','Loan_Amount_Term','Credit_History']
    Name = request.form['Name']
    feature =[]
    for i in list_of_cols:
        feature.append(request.form[i])
    if request.form['Property_Area'] == 0:
        # feature.append(0)
        feature.append(0)
        feature.append(0)
    elif request.form['Property_Area'] == 1:
        # feature.append(0)
        feature.append(1)
        feature.append(0)
    else:
        # feature.append(0)
        feature.append(0)
        feature.append(1)
    if request.form['Dependents'] == 0:
        feature.append(0)
        feature.append(0)
        feature.append(0)
    elif request.form['Dependents'] == 1:
        feature.append(1)
        feature.append(0)
        feature.append(0)
    elif request.form['Dependents'] ==  2:
        feature.append(0)
        feature.append(1)
        feature.append(0)
    else:
        feature.append(0)
        feature.append(0)
        feature.append(1)
    feature = np.array(feature).reshape(1,-1)
    prediction = model.predict(feature)
    string = ""
    if prediction == 1:
        string =  'Congratulations! {}, "Your loan is Approved"'.format(Name)
    else:
        string =  '"Sorry! {}, your loan may not be approved, better luck next time"'.format(Name)

    return render_template('Result.html', Prediction = string)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(port = port,host = '0.0.0.0')

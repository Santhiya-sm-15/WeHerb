import re
from flask import Flask, render_template, request, url_for, redirect
import pandas as pd
app=Flask(__name__)
data=pd.read_csv('data.csv',encoding='latin1')
data2=pd.read_csv('data2.csv',encoding='latin1')
def fetch_remedy(dataframe, search_field, search_value, columns):
    result = dataframe[dataframe[search_field].str.contains(search_value, case=False, na=False)]
    if result.empty:
        return None, f"No remedies found for {search_value}."
    remedy = result[columns].iloc[0].to_dict()
    return remedy, None
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/scheme',methods=['GET','POST'])
def scheme():
    return render_template('scheme.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        return redirect(url_for('index'))
    return render_template('login.html')
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method=='POST':
        return redirect(url_for('index'))
    return render_template('signup.html')
@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/predict',methods=['POST'])
def predict():
    illness=request.form.get('illness')
    system=request.form.get('system')
    result=data[data['Illness'].str.contains(illness,case=False,na=False)]
    if not result.empty:
        remedy=result[[system,system+"_description",system+"_images"]].iloc[0].to_dict()
        if system in remedy:
            remedy[system]=remedy[system].split('\n')
        if system + "_images" in remedy:
            remedy[system + "_images"] = remedy[system + "_images"].split('\n')
        if system + "_description" in remedy:
            description = remedy[system + "_description"]
            lines = description.split('\n')
            f_lines = [f"<strong>{line}</strong>" if re.match(r'.+:$', line) else line for line in lines]
            remedy[system + "_description"] = '<br>'.join(f_lines)
        for key, value in remedy.items():
            if isinstance(value, str):
                value = value.replace('\\n', '<br>')
                remedy[key] = value
        return render_template('index.html',remedy=remedy,illness=illness,system=system)
    else:
        error=f"No remedies found for {illness}."
        return render_template('index.html',error=error)
@app.route('/find',methods=['POST'])
def find():
    system=request.form.get('system')
    age=request.form.get('age')
    result=data2[data2['System'].str.contains(system,case=False,na=False)]
    if not result.empty:
        remedy=result[['System','Scheme','Age','Benefits','Link']].iloc[0].to_dict()
        return render_template('scheme.html',remedy=remedy,system=system,age=age)
    else:
        error=f"No remedies found for {system} for the age group ."
        return render_template('scheme.html',error=error)
if __name__=='__main__':
    app.run(debug=True)
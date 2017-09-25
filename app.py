from flask import Flask, render_template, flash, request, url_for, redirect
import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestRegressor

app = Flask(__name__)


@app.route('/')
@app.route('/index/')
def main():
    return render_template('index.html')


@app.route('/analysis/')
def analysis():
    return render_template("analysis.html")

@app.route('/algorithm/')
def algorithm():
    return render_template("algorithm.html")

@app.route('/predictor/')
def predictor():
    return render_template('predictor.html')


@app.route('/predictor/', methods=['GET','POST'])
def redlight_data():
    tmax = float(request.form['tmax'])	
    tmin = float(request.form['tmin'])
    tavg = (tmax+tmin)/2.
    snow = float(request.form['snow'])
    snowd = float(request.form['snowd'])
    prcp = float(request.form['prcp'])

    df = pd.read_csv("mydata/redlight_add_camera_perdayviolation.csv")
    num_cam=len(df.index)
    df1 = pd.DataFrame({'tmax': [tmax],'tmin': [tmin],'tavg': [tavg],'prcp': [prcp],'snow': [snow],'snowd': [snowd]})
    df2=pd.concat([df1]*num_cam, ignore_index=True)

    df3=pd.concat([df, df2], axis=1)
    X_new = df3[['tavg','prcp','snow','snowd','tmin','tmax', 'perdayviolations']].values

    loaded_model = pickle.load(open('mydata/RF_model_redlight.sav', 'rb'))
    y_pred = loaded_model.predict(X_new)
    y_pred = np.around(y_pred)
    df3['expectedviolationnum'] = y_pred
    df3['camera_id'] = np.around(df3['camera_id'])
    df3.camera_id = df3.camera_id.astype(int)
    df3.expectedviolationnum=df3.expectedviolationnum.astype(int)
    df4=df3.sort_values(by='expectedviolationnum',ascending=False)

    # put top 10 lines into df5
    df5=df4[['address','camera_id','expectedviolationnum']].reset_index(drop=True).head(10)

    df6 = []
    for i in range(0, df5.shape[0]):
	df6.append(dict(address=df5.iloc[i]['address'], camera_id=df5.iloc[i]['camera_id'], expectedviolationnum=df5.iloc[i]['expectedviolationnum']))
    df6_redlight=df6


    df=[]
    df1=[]
    df2=[]
    df3=[]
    df4=[]
    df5=[]
    X_new=[]
    y_pred=[]
    loaded_model=[]
    
    df = pd.read_csv("mydata/speed_add_camera_perdayviolation.csv")
    num_cam=len(df.index)
    df1 = pd.DataFrame({'tmax': [tmax],'tmin': [tmin],'tavg': [tavg],'prcp': [prcp],'snow': [snow],'snowd': [snowd]})
    df2=pd.concat([df1]*num_cam, ignore_index=True)

    df3=pd.concat([df, df2], axis=1)
    X_new = df3[['tavg','prcp','snow','snowd','tmin','tmax', 'perdayviolations']].values

    loaded_model = pickle.load(open('mydata/RF_model_speed.sav', 'rb'))
    y_pred = loaded_model.predict(X_new)
    y_pred = np.around(y_pred)
    df3['expectedviolationnum'] = y_pred
    #df3['camera_id'] = np.around(df3['camera_id'])
    #df3.camera_id = df3.camera_id.astype(int)
    df3.expectedviolationnum=df3.expectedviolationnum.astype(int)
    df4=df3.sort_values(by='expectedviolationnum',ascending=False)

    # put top 10 lines into df5
    df5=df4[['address','camera_id','expectedviolationnum']].reset_index(drop=True).head(10)

    df6 = []
    for i in range(0, df5.shape[0]):
	df6.append(dict(address=df5.iloc[i]['address'], camera_id=df5.iloc[i]['camera_id'], expectedviolationnum=df5.iloc[i]['expectedviolationnum']))
    df6_speed=df6

    return render_template('predictor.html', dataframe_redlight=df6_redlight, dataframe_speed=df6_speed)
    #return render_template('index.html', dataframe=df5.to_html(), length=length)


@app.route('/aboutme/')
def aboutme():
    return render_template('aboutme.html')


if __name__ == '__main__':
    app.run(debug=True, port=5957)

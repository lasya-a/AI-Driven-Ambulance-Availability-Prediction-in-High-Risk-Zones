from django.shortcuts import render
import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split
import sqlite3
from sklearn.preprocessing import LabelEncoder
import seaborn as sns

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers.core import Dense
from keras.optimizers import Adam
from sklearn.impute import SimpleImputer

# Create your views here.
def index(request):
    return render(request,'index.html')

def AdminAction(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    if username=='Admin' and password =='Admin':
        return render(request,'AdminApp/AdminHome.html')
    else:
        context={'data':'Login Failed ....!!'}
        return render(request,'index.html',context)
def Home(request):
    return render(request,'AdminApp/AdminHome.html')
def upload(request):
    return render(request,'AdminApp/UploadDataset.html')

global df
def UploadAction(request):
    global df
    if request.method=='POST':
        filename=request.FILES['file']
        df=pd.read_csv(filename)
        df.dropna(inplace=True)
        context={'msg':'Dataset Uploaded Successfully..!!!'}
        return render(request,'AdminApp/UploadDataset.html',context)

# global df

def preprocess(request):
    # global df
    # path="dataset/accident.csv"
    # df=pd.read_csv(path)
    # df.dropna(inplace=True)
    label_encoder = LabelEncoder()
    #(a) Encoding categorical variables (Label Encoding for 'Yes'/'No' columns)
    df['Help Provided by Ambulance/Patroling Vehicle'] = label_encoder.fit_transform(df['Help Provided by Ambulance/Patroling Vehicle'])
    df['Location'] = label_encoder.fit_transform(df['Location'])
    df['Rural/Urban'] = label_encoder.fit_transform(df['Rural/Urban'])
    df['Nature of Accident'] = label_encoder.fit_transform(df['Nature of Accident'])
    df['Vehicle Involved'] = label_encoder.fit_transform(df['Vehicle Involved'])
    df['Type of Accident'] = label_encoder.fit_transform(df['Type of Accident'])
    df['Causes'] = label_encoder.fit_transform(df['Causes'])
    df['Road Feature'] = label_encoder.fit_transform(df['Road Feature'])
    df['Road condition'] = label_encoder.fit_transform(df['Road condition'])
    df['Weather Condition'] = label_encoder.fit_transform(df['Weather Condition'])


    # b) Feature Scaling for numerical columns
    scaler = StandardScaler()
    df['KM && M'] = scaler.fit_transform(df[['KM && M']])

    context={'msg':'Dataset Preprocessed Successfully...!!'}
    return render(request,'AdminApp/Preprocess.html',context)

global X,y,X_train,X_test,y_train,y_test,df
def Split(request):
    global X,y,X_train,X_test,y_train,y_test,df
    rat=int(request.POST['ratio'])
    final_r=rat/100

    X=df[['Location','Rural/Urban','Nature of Accident','Vehicle Involved','Type of Accident','Causes','Road Feature','Road condition','Weather Condition','No of Affected Persons']].values
    y=df['Help Provided by Ambulance/Patroling Vehicle'].values

    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=final_r,random_state=42)



    imputer = SimpleImputer(strategy='mean')  # Fill missing values with the mean of the column
    X_train = imputer.fit_transform(X_train)
    X_test = imputer.transform(X_test)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    context={"data":"Dataset Preprocess Successfully..!!",'total':len(df),'train':len(X_train),'test':len(X_test)}
    return render(request,'AdminApp/SplittedData.html',context)

global model
from keras.layers import Dropout

def runNeuralNetwork(request):
    global model
    model = Sequential()
    model.add(Dense(128, input_dim=X_train.shape[1], activation='relu'))  # Bigger first layer
    model.add(Dropout(0.3))  # Dropout: randomly ignore 30% neurons
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))  # Binary output

    model.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=0.001), metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=100, batch_size=16, validation_data=(X_test, y_test))

    loss, accuracy = model.evaluate(X_test, y_test)
    print(f'Accuracy on test set: {accuracy * 100:.2f}%')
    model.save("Model/NeuralNetworkModel.h5")

    context={"data":"Upgraded Neural Network Model Generated Successfully...!!", 'Accuracy':f'Accuracy on test set: {accuracy * 100:.2f}%'}
    return render(request,'AdminApp/AlgStatus.html',context)



def RoadFeature(request):
    path="dataset/accident.csv"
    df=pd.read_csv(path)
    sns.set(rc={'figure.figsize':(10.7,8.27)})
    sns.countplot(y=df['Weather Condition'], hue=df['Type of Accident'],data=df)
    plt.savefig('Static/Weather.png',bbox_inches ="tight")
    plt.close()
    return render(request,'UserApp/Weather.html')
def TypeofAccidents(request):
    path="dataset/accident.csv"
    df=pd.read_csv(path)
    sns.set(rc={'figure.figsize':(10.7,8.27)})
    sns.countplot(x=df['Road condition'], hue=df['Type of Accident'],data=df)
    plt.savefig('Static/RoadCondition.png',bbox_inches ="tight")
    plt.close()
    return render(request,'UserApp/RoadCondition.html')

def ulogin(request):
    return render(request,'UserApp/Login.html')

def ULogAction(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    con = sqlite3.connect("ambulance.db")
    cur=con.cursor()
    cur.execute("select *  from user where username='"+username+"'and password='"+password+"'")
    data=cur.fetchone()
    if data is not None:
        request.session['user']=username
        request.session['userid']=data[0]
        return render(request,'UserApp/UserHome.html')
    else:
        context={'data':'Login Failed ....!!'}
        return render(request,'UserApp/Login.html',context)
def userhome(request):
    return render(request,'UserApp/UserHome.html')

def Register(request):
    return render(request, "UserApp/Register.html")
def regaction(request):
    name=request.POST['name']
    email=request.POST['email']
    mobile=request.POST['mobile']
    address=request.POST['address']
    username=request.POST['username']
    password=request.POST['password']

    con = sqlite3.connect("ambulance.db")
    cur=con.cursor()
    #cur.execute("CREATE TABLE user (ID INTEGER PRIMARY KEY AUTOINCREMENT,name varchar(100),email varchar(100),mobile varchar(100),address varchar(100) ,username varchar(100),password varchar(100))")
    i=cur.execute("insert into user values(null,'"+name+"','"+email+"','"+mobile+"','"+address+"','"+username+"','"+password+"')")
    con.commit()
    con.close()
    if i == 0:
        context={'data':'Registration Failed...!!'}
        return render(request,'UserApp/Register.html',context)
    else:
        context={'data':'Registration Successful...!!'}
        return render(request,'UserApp/Register.html',context)

def uHome(request):
    return render(request,'UserApp/UserHome.html')

def predict(request):
    path="dataset/accident.csv"
    df2=pd.read_csv(path)
    df2.dropna(inplace=True)
    NoA = ""
    for d in df2['Nature of Accident'].unique():
        NoA += "<option>" + d + "</option>"
    NoA += ""  # This is unnecessary, but it doesn't harm the code.

    location = ""
    for loc in df2['Location'].unique():
        location += "<option>" + loc + "</option>"  # Fixed the typo here.
    location += ""  # Same as above, unnecessary but harmless.

    VI = ""
    for v in df2['Vehicle Involved'].unique():
        VI += "<option>" + v + "</option>"  # Fixed the typo here.
    VI += ""  # Same as above, unnecessary but harmless.

    ToA = ""
    for t in df2['Type of Accident'].unique():
        ToA += "<option>" + t + "</option>"  # Fixed the typo here.
    ToA += ""  # Same as above, unnecessary but harmless.

    context = {'NoA': NoA, 'loc': location,'VI':VI,'ToA':ToA}
    return render(request,'UserApp/Prediction.html',context)

def PredAction(request):
    loc = request.POST.get('location')
    noa = request.POST.get('noa')
    vi = request.POST.get('vi')
    toa = request.POST.get('toa')
    a = request.POST.get('area')
    b = request.POST.get('cause')
    c = request.POST.get('feature')
    d = request.POST.get('condition')
    e = request.POST.get('weather')
    npe = request.POST.get('npe')

    # Prepare input
    input_data = {
        'Location': [loc],
        'Rural/Urban': [a],
        'Nature of Accident': [noa],
        'Vehicle Involved': [vi],
        'Type of Accident': [toa],
        'Causes': [b],
        'Road Feature': [c],
        'Road condition': [d],
        'Weather Condition': [e],
        'No of Affected Persons': [npe]
    }
    test = pd.DataFrame(input_data)

    # Encoding categorical features
    lbl_encoder = LabelEncoder()
    for column in ['Location', 'Nature of Accident', 'Vehicle Involved', 'Type of Accident']:
        test[column] = lbl_encoder.fit_transform(test[column])

    # Convert to numpy
    test = test.values[:, 0:10]

    # Load trained model
    loaded_model = tf.keras.models.load_model('Model/NeuralNetworkModel.h5')

    # Predict (fixed: don't use deprecated predict_classes)
    pred = loaded_model.predict(test)
    pred_class = (pred > 0.5).astype("int32")  # Proper way in TF 2.x

    print(int(pred_class[0]))
    output = 'none'
    if int(pred_class[0]) > 0:
        output = "Ambulance is Available"
    else:
        output = "Ambulance is Not Available"

    context = {'data': output}
    return render(request, 'UserApp/Availability.html', context)


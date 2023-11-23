import pandas as pd
import warnings
warnings.filterwarnings('ignore')

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from page import streamlitShow

df = pd.read_csv("dataset/fitness_class_2212.csv")

#Data cleaning phase, formatting/cleaning the data to be "schematic"
#Filling the 'weight' column with the mean of the values
df["weight"] = df["weight"].fillna(df["weight"].mean())

#Some of the data contains the string "days", but the "days_before" column is composed as integer
#Here I'm deleting the "days" word, and converting the values into int
df["days_before"] = df["days_before"].str.replace("days","")
df["days_before"] = df["days_before"].astype(int)

#Some inconsistency in the data
df['day_of_week'] = df['day_of_week'].str[:3]

#Some of the elements in the "category" column is "-", I'm replacing it with "unknown" 
df['category'] = df['category'].str.replace("-","unknown")


day_mapping = { 'Mon': 0, 'Tue': 1, 'Wed': 2, 'Thu': 3, 'Fri': 4, 'Sat': 5, 'Sun': 6 }
category_mapping = { "Aqua": 0, "unknown": 1, "Cycling": 2, "HIIT": 3, "Strength": 4, "Yoga": 5 }
time_mapping = { "AM": 0, "PM": 1 }

#Mapping
df['day_of_week'] = df['day_of_week'].map(day_mapping)
df['category'] = df['category'].map(category_mapping)
df['time'] = df['time'].map(time_mapping)

#Removing Outliers
Q1 = df["months_as_member"].quantile(0.25)
Q3 = df["months_as_member"].quantile(0.75)
IQR = Q3 - Q1

#Define the lower and upper bounds for outliers
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

new_df = df[(df['months_as_member'] >= lower_bound) & (df['months_as_member'] <= upper_bound)]

X = new_df.drop(columns=['attended', 'booking_id'],axis=1)
y = new_df["attended"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

#Best models from main.ipynb
lr_pen1 = LogisticRegression(C=0.1, max_iter=100 ,penalty='l1', solver='liblinear', random_state=1)
best_rfcla_gridsearch = RandomForestClassifier(max_depth=50, max_features='sqrt', min_samples_leaf=2, min_samples_split=4, n_estimators=50, random_state=1)

#Model fitting
lr_pen1.fit(X_train, y_train)
best_rfcla_gridsearch.fit(X_train, y_train)

streamlitShow(X_train, y_train, lr_pen1, best_rfcla_gridsearch)
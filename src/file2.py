import mlflow
import mlflow.sklearn
from sklearn.datasets import load_wine
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns 
import os

import dagshub

dagshub.init(repo_owner='saheb123.singha', repo_name='MLflow-tutorial', mlflow=True)

mlflow.set_tracking_uri("https://dagshub.com/saheb123.singha/MLflow-tutorial.mlflow")

wine = load_wine()
X = wine.data
y = wine.target


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

max_depth = 6
n_estimators = 11

mlflow.set_experiment("new_exp2")

with mlflow.start_run():
    rf = RandomForestClassifier(max_depth=max_depth, n_estimators=n_estimators, random_state=42)
    rf.fit(X_train, y_train)
    
    y_pred = rf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    mlflow.log_metric('accuracy', accuracy)
    mlflow.log_param("max_depth", max_depth)
    mlflow.log_param("n_estimators", n_estimators)
    
    
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6,6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=wine.target_names, yticklabels=wine.target_names)
    plt.ylabel("Actual")
    plt.xlabel("Predicted")
    plt.title("Confusion Matrix")
    
    plt.savefig("Confusion-matrix.png")
    
    mlflow.log_artifact("Confusion-matrix.png")
    mlflow.log_artifact(__file__)
    
    mlflow.set_tags({"Author": 'Anamitra', "Project": 'Wine Classification'})

    mlflow.sklearn.log_model(rf, "Random Forest Model")
    
    print(accuracy)
# MLflow Tutorial

This repository is a complete guide and hands-on tutorial for using **MLflow** for tracking machine learning experiments. It demonstrates how to use MLflow to log metrics, parameters, artifacts, and models, and shows how to manage different versions and lifecycles of models. The tutorial also covers how to set up MLflow using **AWS** and **Dagshub** for remote experiment tracking.


All the learnings have been done from Vikash Das's youtube video on MLFlow from the MLOps playlist.
---

## What is MLflow?

**MLflow** is an open-source platform to manage the ML lifecycle, including:
- **Experiment tracking** – record and query experiments: code, data, config, and results
- **Project packaging** – package code in a reusable and reproducible form
- **Model registry** – store, annotate, manage, and deploy models
- **Model deployment** – deploy models from various ML libraries to different platforms

---

## Experiment vs Run

### Experiment
An experiment is a logical collection of **runs**. For example, training a Random Forest classifier is an experiment.

### Run
A run is one single execution of training logic with a specific set of hyperparameters.

#### Example:
| Experiment | Run Name           | Parameters        |
|-----------|--------------------|-------------------|
| Random Forest | run_1           | n_estimators=50   |
| Random Forest | run_2           | n_estimators=100  |
| Neural Network | run_1         | epochs=50         |
| Decision Tree | run_1          | max_depth=10      |

---

## Basic MLflow Setup

### Launching MLflow UI
```bash
mlflow ui
```

This will launch the MLflow tracking UI at `http://localhost:5000`.

---

### Basic MLflow Code Structure

```python
import mlflow

mlflow.set_experiment("Wine_Classifier")

with mlflow.start_run():
    mlflow.log_param("n_estimators", 100)
    mlflow.log_metric("accuracy", 0.89)
    mlflow.set_tags({"Author": 'Vikash', "Project": 'Wine Classification'})
    mlflow.log_artifact("metrics.json")

    mlflow.sklearn.log_model(rf, "Random Forest Model")
```

---

## Autologging

Enable autologging to automatically capture parameters, metrics, models, and more:

```python
mlflow.autolog()
mlflow.set_experiment("Autolog Experiment")
```

> Note: `mlflow.autolog()` logs a lot of details automatically, which can be overwhelming. You may prefer to log specific things manually for more control.

---

## Hyperparameter Tuning with Nested Runs

You can log multiple parameter combinations from `GridSearchCV` using nested runs:

```python
from sklearn.model_selection import GridSearchCV

with mlflow.start_run() as parent:
    grid_search.fit(X_train, y_train)

    for i in range(len(grid_search.cv_results_['params'])):
        with mlflow.start_run(nested=True) as child:
            mlflow.log_params(grid_search.cv_results_["params"][i])
            mlflow.log_metric("accuracy", grid_search.cv_results_["mean_test_score"][i])
```

---

## Model Registry Lifecycle

MLflow allows you to **register models** and manage their lifecycle stages:

| Stage         | Description |
|---------------|-------------|
| `None`        | Default stage; model still in development |
| `Staging`     | Undergoing evaluation and testing |
| `Production`  | Ready and deployed in production |
| `Archived` or `Retired` | Deprecated or replaced by a better model |

---

## MLflow Server Architecture

### Architecture Diagram
![MLFlow Server Architecture](server_arch.png)

### Option 1: AWS Setup

Components you need to configure:
- **IAM**: Define roles and permissions for secure access.
- **EC2**: Hosts the MLflow Tracking Server.
- **S3**: Stores logged artifacts like models, plots, etc.

> AWS setup is secure but involves a lot of manual configuration and maintenance.

---

### Option 2: Dagshub Setup (Recommended)

Dagshub simplifies the entire process:

1. Create a repo on Dagshub and connect it to your GitHub project.
2. Initialize Dagshub in your code:

```python
import dagshub

dagshub.init(repo_owner='saheb123.singha', repo_name='MLflow-tutorial', mlflow=True)
mlflow.set_tracking_uri("https://dagshub.com/saheb123.singha/MLflow-tutorial.mlflow")
```

That’s it! Your MLflow logs are now sent to Dagshub’s hosted server.

**Pros**:
- No infrastructure required
- Easy GitHub integration
- Free tier available

---

## Key Functions and Methods

| Function / Method              | Description |
|-------------------------------|-------------|
| `mlflow.set_experiment()`     | Sets the current experiment |
| `mlflow.start_run()`          | Starts a new run under the current experiment |
| `mlflow.log_param()`          | Logs a single parameter |
| `mlflow.log_metric()`         | Logs a single metric |
| `mlflow.log_artifact()`       | Logs output files (plots, model files, etc.) |
| `mlflow.set_tags()`           | Adds descriptive metadata to a run |
| `mlflow.sklearn.log_model()`  | Logs a scikit-learn model |
| `mlflow.autolog()`            | Automatically logs most things |
| `mlflow.set_tracking_uri()`   | Sets the URI for the tracking server |

---

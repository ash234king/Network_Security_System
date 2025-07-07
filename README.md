# 🛡️ Network Security System - Phishing Detection using ML

This project builds an end-to-end **Network Security System** that identifies whether a website is **phishing** or **legitimate**, using machine learning models deployed via a FastAPI web application. It incorporates full **MLOps**, **EDA**, **CI/CD**, and **Dockerized deployment** on AWS.

---

## 🚀 Features

- ✅ End-to-end ML pipeline: Ingestion → Validation → Transformation → Training
- ✅ Real-time prediction via FastAPI web app
- ✅ Integrated EDA charts for uploaded data
- ✅ Drift detection using `ks_2samp` statistical test
- ✅ ML experiment tracking using **MLflow** + **DagsHub**
- ✅ Dockerized app with **CI/CD via GitHub Actions**
- ✅ Deployed on AWS **Elastic Beanstalk**

---

## 🧠 ML Workflow Overview

### 1. 🔍 Data Ingestion
- Data is read directly from a **MongoDB** database.
- Split into train and test datasets.

### 2. ✅ Data Validation
- Schema validation (number of columns).
- **Drift detection** using Kolmogorov–Smirnov test.

### 3. 🔄 Data Transformation
- Missing values handled using **KNN Imputer**.
- Output is saved as transformed NumPy arrays.

### 4. 🧪 Model Training & Selection
- Models used:
  - Random Forest
  - Decision Tree
  - AdaBoost
  - GradientBoosting
  - Logistic Regression
  - K-Nearest Neighbors
- Metrics: **Precision**, **Recall**, **F1-Score**
- Best model selected using **cross-validated performance**.

---

## 🌐 Web App Pages

| Page            | Description                                               |
|-----------------|-----------------------------------------------------------|
| 🏠 Home         | Welcome page with project introduction                    |
| 🛠️ Train Model  | Retrain models using the complete ML pipeline             |
| 🧠 Prediction   | Upload CSV and predict phishing sites                     |
| 📊 Data Analysis| Display EDA charts (bar, violin, heatmap, pie, etc.)      |
| 👤 About Me     | Short personal and app description  (included on all pages)        |

---

## 📈 EDA Visuals on first feature 

- 📊 Bar Chart  
- 🎻 Violin Plot  
- 🔥 Correlation Heatmap  
- 📦 Boxplot  
- 🥧 Pie Chart  
- 📉 Frequency Chart  

These are dynamically generated based on user-uploaded data.

---

## ⚙️ CI/CD Pipeline

- GitHub Actions Workflow:
  - ✅ Runs tests
  - 🐳 Builds Docker image
  - 📤 Pushes image to **Docker Hub**

---

## 🧾 Secrets & Environment Variables

To run **GitHub Actions** or deploy successfully on **AWS Elastic Beanstalk**, you must provide the following:

### 🔐 GitHub Secrets (for CI/CD):
Make sure these are added to your repository's secrets:
- `MONGO_DB_URL`
- `MLFLOW_TRACKING_USERNAME`
- `MLFLOW_TRACKING_PASSWORD`
- `DAGSHUB_USERNAME`
- `DAGSHUB_PASSWORD`

### 🌐 Environment Variables (for Deployment):
Include these variables in your `.env` file or environment configuration on AWS:
- `MONGO_DB_URL`
- `MLFLOW_TRACKING_URI`
- `MLFLOW_TRACKING_USERNAME`
- `MLFLOW_TRACKING_PASSWORD`

---

## 🐳 Docker & Deployment

- ✅ Dockerfile builds and runs FastAPI app
- ✅ Image pushed to Docker Hub
- ✅ Deployed on **AWS Elastic Beanstalk** 

---

## 📁 Project Structure


```bash
.
├── .ebextensions/               # AWS Elastic Beanstalk Docker configuration
│   └── docker.config
├── .github/
│   └── workflows/
│       └── main.yml             # CI/CD GitHub Actions workflow
├── data_schema/
│   └── schema.yml               # Schema for data validation
├── final_models/
│   ├── model.pkl
│   ├── preprocessor.pkl
│   ├── test_model.pkl
│   └── train_model.pkl
├── Network_Data/
│   └── phishing data.csv        # Original dataset
├── network_security/
│   ├── components/              # Pipeline stages
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   └── model_training.py
│   ├── constant/
│   │   └── training_pipeline/
│   │       └── constants for schema, filenames, etc.
│   ├── eda/
│   │   └── eda.py               # Dynamic EDA generation
│   ├── entity/
│   │   ├── artifact_entity.py
│   │   └── config_entity.py
│   ├── exception/
│   │   └── exception.py
│   ├── logging/
│   │   └── logger.py
│   ├── pipeline/
│   │   └── training_pipeline.py
│   └── utils/
│       ├── ml_utils/
│       │   ├── metric/
│       │   │   └── precision, recall, F1 score scripts
│       │   └── estimator/
│       └── main_utils.py
├── notebooks/
│   └── eda_notebook.py       # EDA on original dataset
├── prediction_output/
│   └── *.csv                    # Predicted output data
├── static/
│   ├── style.css
│   ├── eda_outputs/             # EDA plots on uploaded data
│   └── images/                  # Background/logo/author images
├── templates/
│   ├── index.html
│   ├── predict.html
│   ├── train.html
│   ├── table.html
│   └── data_analysis.html
├── valid_data/
│   └── test.csv                 # Sample data for testing predictions
├── .dockerignore
├── .gitignore
├── app.py                       # FastAPI entrypoint
├── Dockerfile
├── push_data.py                # Script to upload data to MongoDB
├── README.md
├── requirements.txt
└── setup.py

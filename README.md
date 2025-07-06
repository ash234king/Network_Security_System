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
| 👤 About Me     | Short personal description (included on all pages)        |

---

## 📈 EDA Visuals

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
- ✅ Deployed on **AWS Elastic Beanstalk** using `Dockerrun.aws.json`

---

## 📁 Project Structure


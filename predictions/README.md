# Titanic Predictions Web App

## Overview

This project is a **web application built with Django** that utilizes a pre-trained machine learning model to make predictions. Specifically, the application predicts survival outcomes for passengers aboard the Titanic based on their demographic and ticket details. Users can upload an Excel file with the required passenger information, which the app processes and uses to generate predictions, displaying the results in an interactive table on a webpage, it also allows you to download the results of the predictions in an Excel file.

The application demonstrates:
- **Model Integration:** A logistic regression model trained on the Titanic dataset.
- **Excel File Processing:** Reads and validates user-uploaded Excel files.
- **Dynamic Predictions:** Applies the ML model to user-provided data and presents the predictions.

### Sample File for Testing

A sample Excel file, **`excel_titanic.xlsx`**, is available in the `predictions/static/predictions/` directory. This file can be uploaded to the application to test its functionality and observe predictions. Ensure that the file structure and data format are preserved when creating or using custom Excel files.

## Technologies Used

### Backend
- **Django 5.1.3:** Framework for building web applications.
- **Python 3.12.3:** Core programming language.
- **Scikit-learn:** Library for training and using machine learning models.
- **Pandas:** Library for data manipulation and analysis.

### Frontend
- **HTML/CSS:** Used for rendering the user interface.
- **Swagger UI:** Integrated for API documentation.

### Other Tools
- **Docker:** Containerization for easy deployment.
- **Joblib:** For saving and loading the ML model and scaler.
- **OpenPyXL:** For handling Excel files.

## Deployment

The application has been deployed using **Railway** and is available at:  
[https://technical-test-talentob-production.up.railway.app](https://technical-test-talentob-production.up.railway.app)

You can visit this link to upload your Excel file and test the application directly online.

## How to Run the Project

### Prerequisites
- Install [Docker](https://docs.docker.com/get-docker/) if you plan to run the project using a container.
- Alternatively, install Python 3.10 and pip if you want to run the project locally.

### Running Locally (Without Docker)

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
    ```
2. Install dependencies:
    ```bash
   pip install -r requirements.txt
    ```
3. Run the Django server:
    ```bash
   python manage.py runserver
    ```
4. Access the app in your browser at http://127.0.0.1:8000

5. Swagger Documentation: Available at http://127.0.0.1:8000/docs

### Running with Docker

1. Build the Docker image:
    ```bash
   docker build -t titanic-predictions .
    ```
2. Run the container:
    ```bash
   docker run -p 8000:8000 titanic-predictions
    ```
3. Access the app in your browser at http://127.0.0.1:8000

4. Swagger Documentation: Available at http://127.0.0.1:8000/docs

## Additional Notes

- Make sure the uploaded Excel files have the correct column names (`age`, `fare`, `sex`, `sibsp`, `parch`, `pclass`, `embarked`) and formatting as the application validates inputs before making predictions.
- The machine learning model and scaler are pre-loaded and stored in the `predictions/models/` directory.

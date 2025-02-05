
```markdown
# KYC Module Project

This is a **KYC (Know Your Customer)** verification module built with **FastAPI** for the backend and **React** for the frontend. It integrates with **Setu APIs** for PAN and Bank account verification and stores user verification data in a MySQL database.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Technologies Used](#technologies-used)
3. [Project Setup](#project-setup)
   1. [Backend Setup](#backend-setup)
   2. [Frontend Setup](#frontend-setup)
4. [Running the Application Locally](#running-the-application-locally)
5. [Deployment](#deployment)
6. [APIs](#apis)
7. [Frontend Usage](#frontend-usage)

---

## Project Overview

This project provides a KYC verification service. The backend handles requests for **PAN verification** and **Bank account verification** using **Setu APIs** and stores the status in an AWS MySQL database. Admins can delete users and update their verification status.

## Technologies Used

- **Backend**: FastAPI, SQLAlchemy, MySQL (AWS RDS), Docker
- **Frontend**: React, Axios
- **Deployment**: AWS EC2, AWS RDS, AWS S3, AWS CloudFront, Docker
- **CI/CD**: Git, Terraform, Docker Compose
- **Environment**: Python 3.11, Node.js

---

## Project Setup

### Backend Setup

   ```bash
   git clone https://github.com/your-repo/kyc-module.git
   cd kyc-module/backend
   ```

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   ```bash
   pip install -r requirements.txt
   ```

   Create a `.env` file in the backend directory with the following content:

   ```bash
   DATABASE_URL=mysql+pymysql://admin:Secure0987Subh@terraform-20250204162314440000000001.czagm0iaqdg8.ap-south-1.rds.amazonaws.com:3306/mydb
SETU_PAN_API_KEY="NI4iv41XdZmQ1TVtjuowva5EVrAyp5eP"
SETU_BASE_URL="https://api.setu.co"
   ```

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

   ```bash
   npm install
   ```

   ```bash
   REACT_APP_API_URL=http://localhost:8000
   ```

   ```bash
   npm start
   ```

## Running the Application Locally

### Running Backend Locally

- The backend will be running on `http://localhost:8000` once you run the command:
  
  ```bash
  uvicorn app.main:app --host 0.0.0.0 --port 8000
  ```

- You can test the backend APIs with tools like **Postman** or **curl**.

### Running Frontend Locally

- The frontend will be running on `http://localhost:3000` once you run the command:

   ```bash
   npm start
   ```

- Open this URL in your browser to interact with the frontend.

---

## Deployment

1. **Dockerize the Backend**:
   The backend is containerized using Docker. To build and run it:

   ```bash
   docker build -t kyc-backend .
   docker run -d -p 8000:8000 kyc-backend
   ```

2. **Deploy to AWS EC2**:
   Follow these steps to deploy the backend to AWS EC2:
   
   - Launch an EC2 instance and attach a security group that allows port 22 (SSH) and 8000 (for API).
   - SSH into the instance and set up Docker, MySQL, and any other required services.
   - Deploy the backend using Docker or manually install dependencies.
   - Set up an RDS instance for MySQL and link it with the backend.

3. **Frontend Deployment**:
   - Host the frontend on AWS S3 and use AWS CloudFront to serve the static files.

---

## APIs

### POST `/verify-pan`

- **Description**: Verifies a PAN number using Setu's API.
- **Request body**:

  ```json
  {
    "pan_number": "ABCDE1234F"
  }
  ```

- **Response**:

  ```json
  {
    "status": "success",
    "data": { ...response_data_from_setu_api }
  }
  ```

### POST `/verify-bank`

- **Description**: Verifies a bank account using Setu's API.
- **Request body**:

  ```json
  {
    "account_number": "1234567890",
    "ifsc_code": "IFSC0001234"
  }
  ```

- **Response**:

  ```json
  {
    "status": "success",
    "data": { ...response_data_from_setu_api }
  }
  ```

### GET `/analytics`

- **Description**: Provides analytics for the total number of KYC verifications.
- **Response**:

  ```json
  {
    "total_kyc_attempted": 100,
    "total_kyc_successful": 80,
    "total_kyc_failed": 20,
    "total_kyc_failed_due_to_pan": 10,
    "total_kyc_failed_due_to_bank": 5,
    "total_kyc_failed_due_to_both": 5
  }
  ```

### DELETE `/admin/delete-user/{user_id}`

- **Description**: Deletes a user from the KYC database by their `user_id`.
- **Response**:

  ```json
  {
    "status": "success",
    "message": "User deleted successfully"
  }
  ```

### PUT `/admin/update-user/{user_id}`

- **Description**: Updates the KYC verification status of a user.
- **Request body**:

  ```json
  {
    "pan_verified": true,
    "bank_verified": true
  }
  ```

- **Response**:

  ```json
  {
    "status": "success",
    "message": "User verification status updated"
  }
  ```

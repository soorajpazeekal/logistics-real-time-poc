
[![open Linkedin profile](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/soorajpazeekal)


# real-time logistics tracking and management proof of concept

***Proof of Concept for a US-based Grocery Delivery Platform, Ensuring Swift Delivery Within 15 Minutes***

## Overview

🚀 A Proof of Concept demonstrating cutting-edge logistics solutions for a US-based Grocery Delivery Platform. Our focus is on real-time tracking and management, guaranteeing efficient deliveries in less than 15 minutes. Explore the future of rapid and reliable grocery delivery!
## Project Objectives

**1. Real-Time Tracking Implementation:** 
- Develop a user-friendly interface for real-time tracking accessible to both delivery personnel and end-users.
- Integrate GPS technology and geofencing to enhance the accuracy of location data in various delivery scenarios.
- Implement automated alerts and notifications for customers, keeping them informed about their delivery status in real time.

**2. Efficient Data Management:**
- Implement data compression and encryption techniques to optimize storage and secure sensitive information
- Explore cloud-based solutions for scalable and cost-effective data storage, ensuring seamless scalability as the platform grows.
- Integrate data quality checks and validation processes to ensure the accuracy and integrity of incoming data streams.

**3. Guaranteed Delivery Time:**

- Implement dynamic adjustments to delivery routes based on real-time data to minimize delays.
- Develop a feedback loop mechanism for continuous improvement, incorporating user feedback and performance metrics.

**4. Data Visualizations and Actionable Insights:**

- Implement key performance indicators (KPIs) such as delivery time variance, route optimization efficiency, and customer satisfaction metrics.
- Develop custom dashboards for stakeholders to monitor real-time logistics performance
- Develop automated reports highlighting actionable insights, such as areas for route optimization or inventory management improvements.
## System Architecture

![highlevel System Architecture](https://github.com/soorajpazeekal/logistics-real-time-poc/assets/41431605/af9b188a-337f-4884-bd3a-5d3430090421)

## Demo Video

[![Demo Video](https://img.youtube.com/vi/3yVsfVwpqQI/0.jpg)](https://www.youtube.com/watch?v=3yVsfVwpqQI)

## Tech & Prerequisites

- [AWS S3](https://aws.amazon.com/s3/)
- [Pyspark 3.3.2](https://spark.apache.org/docs/3.3.2/api/python/index.html)
- [redpanda](https://go.redpanda.com/redpanda-6x-lower-cloud-spend?utm_content=tcolayer)
- [Docker](https://docs.docker.com/compose/)
- [deephaven](https://deephaven.io/core/docs/)
- [databricks](https://www.databricks.com/blog/what-is-a-data-intelligence-platform)
- [Delta Lake](https://docs.delta.io/latest/delta-intro.html)
## Installation

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/soorajpazeekal/Data-Engineering-Projects-basic)

***This project was tested on Linux platforms. So that's a recommended way to install this project in a Linux environment.***

**1. First Clone this repo and select project directory**
```bash
https://github.com/soorajpazeekal/logistics-real-time-poc.git
cd logistics-real-time-poc
```
**2. Prepare .ini files.**

- Open 'producer' folder and edit *.ini.example* file then save

```json
[DEFAULT]
bootstrap_servers = localhost:19092
docker_bootstrap_servers = redpanda-0:9092
delta_lake_path = <path to delta lake folder> #local
checkpointLocation = <path to checkpoint folder> #local


[AWS]
s3_bucket_path = s3a://<bucket name>/table
aws_access_key = <IAM access key> #s3 read access required
aws_secret_key = <IAM secret key>
```

**3. Start Docker and Verify:**
- Ensure Docker is installed on your system.
- Open a terminal and navigate to the project directory.

```bash
docker-compose up -d
```
*Verify that the Docker containers are successfully running*
```bash
docker ps
```

***Access Redpanda Console: http://localhost:8080***

**4. Access the Application in Your Browser:**

- Open your preferred web browser
- Enter the following URL in the browser's address bar: http://localhost:10000
    - You will be prompted to enter a Token.
    - Use the provided Token: **"password"**.
    - Click on the login button to access the application.

**5. View real-time tables:**

![dashboard table Screenshot](https://github.com/soorajpazeekal/logistics-real-time-poc/assets/41431605/dcf2903c-6338-46ee-9c5f-d3bb151b87c0)

To view real-time data and monitor order placement in a dynamic environment, follow these steps:

- *Navigate to Panels:* Locate the top right side menu in the application interface.
- *Click on Panels:* Click on the "Panels" option to access a comprehensive set of monitoring and visualization tools. *Also you can drag and drop the tables anywhere in the dashboard.*

***Please Note: To experience the real-time order placement functionality, we kindly ask you to wait a few seconds. During this time, the system will auto-generate comprehensive data reflecting live order placement activities.***

**6. Run Pyspark jobs:**
(kafka_to_delta.py, local_to_s3.py)

- Install *requirements.txt*
```bash
pip install -r requirements.txt
```
```bash
python kafka_to_delta.py
```
***Note: This utilize spark structured streaming to read data from redpanda and write to delta table (resource dependent)***
```bash
python local_to_s3.py
```
***The "local_to_s3.py" program is designed to seamlessly transfer data from local Delta tables to an AWS S3 bucket while maintaining the Delta table format. This automated process ensures efficient and structured storage in the cloud.***

## Contact


Please feel free to contact me if you have any questions at: LinkedIn: [![open Linkedin profile](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/soorajpazeekal)
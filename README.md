# Pricing_Case_Study

This project is a web-based solution to upload, search, and manage pricing records for retail stores. It consists of a React.js frontend and a Django REST API backend.

# Project Overview

The Pricing Management Dashboard allows users to:

Upload large CSV files containing pricing data.
Search for records based on criteria such as Store ID, SKU, or Product Name.
Edit and update specific records in real-time.
View records with pagination for better performance.

# Features

Upload CSV Files:
Supports bulk upload of pricing records asynchronously using Celery.
Validates the CSV format before processing.

Search Functionality:
Search by Store ID, SKU, and Product Name.
Caching with Redis for improved search performance.

Edit Records:
Update specific records directly from the UI.

Pagination:
Backend handles pagination for large datasets.

Authentication:
JWT-based authentication secures the API endpoints.

Performance Optimizations:
Caching with Redis.
Asynchronous processing using Celery.

# Technology Stack

Frontend:
React.js
Axios (HTTP Client)
Bootstrap (Styling)

Backend:
Django REST Framework
Celery (Asynchronous Task Queue)
Redis (Caching and Celery Broker)
MySQL (Database)

# Contact

For queries, contact:

Name: Chandan Raj
Email: chandan.raj.s@outlook.com
GitHub: https://github.com/RajChandan

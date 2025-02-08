# Inventory menegment service - FastAPI & PostgeSQL & Kafka  


## Overview
The Inventory Management Service is a microservice-based application designed to efficiently handle inventory operations. It is built using FastAPI, a modern, high-performance web framework, and follows the RESTful API principles for seamless client communication. The service connects to a PostgreSQL database, ensuring robust data storage and retrieval capabilities.

To support event-driven messaging, the system integrates Apache Kafka, enabling real-time event streaming and asynchronous processing of inventory updates. This architecture ensures scalability, allowing other services to react to inventory changes efficiently.

The entire application is containerized using Docker Compose, making it easy to set up, run, and manage in different environments. The service provides full CRUD functionality (Create, Read, Update, Delete), ensuring smooth and scalable inventory management.

## FastAPI Project Structure

```
oveo_task/                              
│── ms_inventory/                        
│   ├── src/
│   │   ├── inventory_module.py          # Inventory management logic
│   │   ├── local_config.py              # Configuration settings
│   │   ├── kafka_driver.py              # Kafka integration
│   ├── main.py                          # FastAPI entry point
│   ├── Dockerfile                       # Docker container setup
│   ├── requirements.txt                 # Python dependencies
│── .gitignore                           # Files to exclude from Git
│── docker-compose.yml                   # Docker Compose configuration
│── init-db.sql                          # Database initialization script
│── README.md                            # Project documentation
│── .env                                 # Environment variables
│── postman_collection.json              # API test collection
```



## Installation
1. Clone the project
2. Run ```docker-compose up --build```


## Testing Instructions

### Option 1: FastAPI Swagger UI
Open Swagger UI [Project documatation].
Use the interactive documentation to test available API endpoints.

### Option 2: Postman Collection
Open Postman.
Import the postman_collection.json file.
Use the predefined requests to interact with the API.

### Option 3: Kafka UI
Ensure Kafka is running.
Open [Kafka UI].
Select a topic and publish or subscribe to messages for testing.





[Project documatation]: <http://127.0.0.1:8000/docs#/>
[Kafka UI]: http://localhost:8080/ui/clusters/local-cluster/all-topics?perPage=25
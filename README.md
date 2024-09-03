# Social Media App Backend APIs

This repository contains the backend APIs for a social media application. It provides functionality for user authentication, friend management, and search features.

## Features

- User registration
- User login/logout
- Search for friends by name/email
- Send friend requests
- Accept/reject friend requests

## Technologies Used

- Django: Python web framework
- PostgreSQL: Database backend
- JWT: JSON Web Tokens for authentication
- Docker: Containerization for deployment

## Setup Instructions

1. **Clone the Repository**: 
    ```bash
    git clone https://github.com/yashaswininaik/socialmediabackend.git
    ```

2. **Build and Run Docker Compose**: 
    ```bash
    cd socialmediabackend
    docker-compose build
    docker-compose up
    ```

3. **Accessing the API**: 
    Once the containers are running, you can access the APIs at `http://localhost:8000`.

4. **API Documentation**: 
    - You can use tools like Postman to explore and test the endpoints.

## Configuration

- The PostgreSQL database configuration can be modified in the `docker-compose.yml` file.
- Django settings related to JWT authentication, database, and other configurations can be found in the `settings.py` file.

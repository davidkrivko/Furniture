# Furniture

***

Welcome to Furniture API

## Installation:

```shell
git clone https://github.com/davidkrivko/Furniture.git
cd Furniture
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run with the Docker:

```shell
docker-compose build
docker-compose up
```

## Getting access

  You must create user and get JWT(token)

- create you user via /api/user/registration/
- get token via /api/user/login/

## Features

- admin access
- JWT authentication
- CRUD for Models
- Permissions for Authenticated Customers
- Write comments near Furniture items
- Creating orders with amount of products
- Filtering Furniture by type

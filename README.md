# TeamGeek Books API
TG Book API is a public service that allows subscribed users to create and modify books.


## Technical Description
Teamgeek Books API project is based on python flask web framework. Other dependencies include SQLAlchemy library and SQLite as the database of choice. This is a dockerize project that can simply be run on Docker, Kubernetes or any containerized environment.


## URLS
User Authentication
    - [POST] /api/auth/         Create a new user profile
        Required data (fulllname, email, password)

    - [POST] /api/auth/in       Sign in obtain login token
        Required data (userid, pwd)

    - [PUT] /api/auth/          Modify User profile  **incomplete feature**
    - [DELETE] /api/auth/       Remove or Delete user profile **incomplete feature**

Book Resources Endpoints
    - [GET] /api/books/:id      Retrieve book item or resource using id
        Required data (id)

    - [GET] /api/books/         Retrieve all book items or resources

    - [POST] /api/books/        Create or add book item or resource
        Required data (isbn, title, author, publish_date)

    - [PUT] or [PATCH] /api/books/:id   Modify a book item or resource
        Required data (id, isbn, title, author, publish_date)


## Additional Libraries
1. Flask (https://flask.palletsprojects.com/)
Flask is a lightweight Python web framework that allows you to build web applications quickly and efficiently. It's known for its simplicity, flexibility, and ease of use.

2. SQLAlchemy (https://www.sqlalchemy.org/)
SQLAlchemy is a popular Python Object-Relational Mapper (ORM) that simplifies database interactions by providing a high-level interface to SQL databases. It allows you to define database models as Python classes and interact with them using object-oriented programming techniques.

3. Pydantic (https://docs.pydantic.dev/latest/)
Pydantic is a Python library that lets you define data models by creating Python classes that validate the data passed to them. It ensures data integrity and provides a convenient way to work with structured data.

4. Gunicorn (https://pypi.org/project/gunicorn/)
Gunicorn, also known as the "Green Unicorn," is a Python WSGI HTTP server. It's a popular choice for serving web applications, including Flask apps, in production environments.

5. Pytest (https://docs.pytest.org)
Pytest is a popular Python testing framework that simplifies the process of writing and running tests. It's known for its simplicity, flexibility, and extensive plugin ecosystem.

6. Requests (https://pypi.org/project/requests/)
Python Requests is a user-friendly HTTP library that simplifies making HTTP requests in Python. It allows you to send HTTP requests, such as GET, POST, PUT, DELETE, etc., and handle responses in a straightforward way.

7. Python-dotenv (https://pypi.org/project/python-dotenv/)
Python-dotenv is a Python library that simplifies the process of managing environment variables in your applications. It allows you to store sensitive information, such as API keys, database credentials, and other configuration settings, in a .env file.

8. JSON Web Tokens (JWT - https://jwt.io/)
JSON Web Token is a proposed Internet standard for creating data with optional signature and/or optional encryption whose payload holds JSON that asserts some number of claims. The tokens are signed either using a private secret or a public/private key. 

9. Redis (https://redis.io/)
Redis is a source-available, in-memory storage, used as a distributed, in-memory key–value database, cache and message broker, with optional durability.



## Setup Service
There are a few ways to deploy this project using either or;
1. Docker
2. Kubernetes
3. Cloud Platforms (AWS, Azure, Digital Ocean, GCP)
4. Locally (through containerization)


## Developed By
Engineer : __Isaac K. Amoah__ 
Company : __Team Geek Pty__
Location : __Cape Town, South Africa__
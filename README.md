# Build a URL Shortener with FastAPI and Python

This tutorial from Real Python walks us through on how to create a URL shortener from scratch with Python and FastAPI. We will have a fully functional *API-driven web-app* that creates shortened URLs that forward to target URLs.

In this tutorial, we will learn how to:

* Create a *REST API* with FastAPI
* Run a development web server with *Uvicorn*
* Model an *SQLite* database
* Investigate the auto-generated *API Documentation*
* Interact with the database with *CRUD Actions*

## Project overview

The URL shortener Python Project will provide *API endpoints* that are capable of receiving different *HTTP request types*

| Endpoint            | HTTP Verb | Request Body    | Action                                                                 |
|---------------------|-----------|-----------------|------------------------------------------------------------------------|
| /                   | GET       |                 | Returns a 'Hello, world!' string.                                      |
| /url                | POST      | Your target URL | Shows the created url_key with additional info, including a secret key |
| /{url_key}          | GET       |                 | Forwards to your target URL                                            |
| /admin/{secret_key} | GET       |                 | Shows administrative info about your shortened URL                     |
| /admin/{secret_key} | DELETE    | Your secret key | Deletes your shortened URL                                             |

* More details to learn more about Python Packages, check out [Python import: Advanced Techniques and Tips](https://realpython.com/python-import/)

### Adding Project Dependencies

In order to run our API, we will need a Web Server and that's what *uvicorn* is for. Uvicorn is a web server implementation for Python that provides an *Asynchronous Server Gateway Interface (ASGI)*. Web Server Gateway Interfaces (WSGI) specify how your web server communicates with your web application.

*NOTE*: Learn more about [AsyncIO in Python](https://realpython.com/async-io-python/) and how FastAPI handles Parallelism, then we can check out the [Concurrency and async / await](https://fastapi.tiangolo.com/async/) page of the FastAPI Docs.

The python-dotenvv package helps us read key-value pairs from an external file and set them as environment variables. And the *validators* library helps us to validate values like email addresses, IP Addresses, or even Finnish Social Security Numbers.

### Defining Environment Variables

*NOTE*: Check out [Python Web Applications: Deploy your script as a Flask App](https://realpython.com/python-web-applications/) or [Deploying a Python Flask Example Application using Heroku](https://realpython.com/flask-by-example-part-1-project-setup/)

In loading our settings over and over again when we call get_settings(), we can take advantage of using the *Least Recently Used (LRU)* strategy.

When we start our web-app, it makes sense to load your settings and then *cache* the data. Caching is an optimization technique that we can use in our applications to keep recent or often-used data in memory. We can implement the [LRU cache strategy](https://realpython.com/lru-cache-python/) to accomplish that behaviour.

By stroing our environment variables externally, we're following the [twelve-factor app methodology](https://12factor.net/). The *twelve-factor app methodology* states twelve principles to enable developers to build portable and scalable web applications.

It's recommended to have different .env files for different environments. Also, we should never add the .env file to our version control system, as our environment variables may store sensitive information.

## Setting up our Python URL Shortener

```[python]
(shortener_app_dev) C:\Users\creyes24\Real-World-Python\URL_Shortener>uvicorn main:app --reload
←[32mINFO←[0m:     Will watch for changes in these directories: ['C:\\Users\\creyes24\\Real-World-Python\\URL_Shortener']
←[32mINFO←[0m:     Uvicorn running on ←[1mhttp://127.0.0.1:8000←[0m (Press CTRL+C to quit)
←[32mINFO←[0m:     Started reloader process [←[36m←[1m36068←[0m] using ←[36m←[1mstatreload←[0m
←[33mWARNING←[0m:  The --reload flag should not be used in production on Windows.
←[32mINFO←[0m:     Started server process [←[36m19904←[0m]
←[32mINFO←[0m:     Waiting for application startup.
←[32mINFO←[0m:     Application startup complete.
```

*NOTE*: Our browser may display the response as unformatted text.

### Deciding what your application can do

To enable for our users to manage our shortened URL, we're sending along a response with some additional information to the client. Here's an example of how a response body can look:

```[json]
{
    "target_url": "https://realpython.com",
    "is_active": true,
    "clicks": 0,
    "url": "JNPGB",
    "admin_url": "MIZJZYVA",
}
```

Our schema states what our API expects as a request body and what the client can expect in the response body. By implementing *type hinting*, we would be able to verify the request and the response that matches the data types that we define.

```[python]
# url_shortener/schemas.py

from pydantic import BaseModel

class URLBase(BaseModel):
    target_url: str
    
class URL(URLBase):
    """Inherits our target_url field from the URLBase class.

    Args:
        is_active (bool): allows us to deactivate shortened URLS.
        clicks (int): counts how many times a shortened URL has
        been visited.
    """
    is_active: bool
    clicks: int
    
    class Config:
        """By setting the orm_mode = True setting will tell
        pydantic that we are working with a database model."""
        orm_mode = True
        
class URLInfo(URL):
    url: str
    admin_url: str
```

```[python]
# URL_Shortener/main.py

import validators
from fastapi import FastAPI
from fastapi import HTTPException

from . import schemas

app = FastAPI()

def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)

@app.get("/")
def read_root():
    return "Welcome to the URL shortener API :)"

@app.post("/")
def create_url(url: schemas.URLBase):
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not valid.")
    return f"TODO: Create database entry for: {url.target_url}"
```

### Preparing our SQLite Database

```[python]
# url_shortener/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import get_settings

engine = create_engine(
    get_settings().db_url, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

# NOTE: the "declarative base" function returns a class that connects
# the database engine to the SQLAlchemy functionality of the models.
# We assign declarative_base() to Base in which it will inherit the
# database model from our models.py file
Base = declarative_base()
```

While database.py contains information about our database connection, the models.py file will describe the content of our database.

```[python]
# url_shortener/models.py

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from .database import Base

class URL(Base):
    __tablename__ = "urls"
    
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, index=True)
    secret_key = Column(String, unique=True, index=True)
    target_url = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    clicks = Column(Integer, default=0)
```

It's common to give our model a singular name and our database tables plural names. Our app's expected behaviour is that any user can create a shortened URL for any target URL without knowing if such a forward already exists.

### Connect our Database

```[python]
# URL_Shortener/main.py

import secrets

import validators
from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import models
from . import schemas
from .database import SessionLocal
from .database import engine


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


@app.get("/")
def read_root():
    return "Welcome to the URL shortener API :)"


@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not valid.")
        
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = "".join(secrets.choice(chars) for _ in range(5))
    secret_key = "".join(secrets.choice(chars) for _ in range(8))
    db_url = models.URL(
        target_url=url.target_url, key=key, secret_key=secret_key
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    db_url.url = key
    db_url.admin_url = secret_key
    
    return db_url
```

Firing-up our SQLite database by using our environment variables and checking in our Python Interpreter, our database urls table doesn't contain any data yet.

```[python]
shortener_app_dev) C:\Users\creyes24\Real-World-Python>python
Python 3.9.0 (tags/v3.9.0:9cf6752, Oct  5 2020, 15:34:40) [MSC v.1927 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>
>>> from URL_Shortener.database import SessionLocal
Loading settings for: Local
>>> db = SessionLocal()
>>>
>>> from URL_Shortener.models import URL
>>> db.query(URL).all()
[]
>>>
```

Once we have created a POST endpoint in the FastAPI docs url, we can verify that the request created the database entries accordingly.

```[python]
>>> from URL_Shortener.models import URL
>>>
>>> db.query(URL).all()
[<URL_Shortener.models.URL object at 0x00000256CDA1E4F0>]
```

Based from the `db.query(URL).all()` we're querying all entries of our URL table. In return, we get a list of all database entries that we created with the POST requests that we sent over to our API.

Further reading: [PEP 506](https://peps.python.org/pep-0506/)

### [TBC] Forwarding a Shortened URL

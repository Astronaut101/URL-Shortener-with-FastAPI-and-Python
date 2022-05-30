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

### [TBC] Deciding what your application can do

# Flask Water Quality Application

This is GitHub repository for a web app that deploys a machine learning model using RESTAPI. The purpose of the web app is to forecast data about the quality of water at different locations on an interactive map. 

This application provides an API for users to log in, upload water quality data, and view predictions and historical data insights.

## Getting Started

These instructions will get the web application running on your local machine for development and testing purposes.

### Installing

Follow these steps to get your development environment running:

1. **Clone the repository:**
   
  ```
  git clone xxx
  ```

  ```
    cd xxx
  ```


2. **Create and activate a virtual environment:**

   -On macOS and Linux:

      ```
      python3 -m venv .venv
      ```

      ```
      source .venv/bin/activate
      ```

   -On Windows:

      ```
      python -m venv .venv
      ```

      ```
      .venv\Scripts\activate
      ```

3. **Install the dependencies:**
   
```
pip install -r requirements.txt
```


5. **(Optional) Set environment variables:**

You may wish to set environment variables such as `FLASK_APP` and `FLASK_ENV`:

On macOS and Linux:

```
export FLASK_APP=webapp
```

```
export FLASK_ENV=development
```

On Windows:

```
set FLASK_APP=webapp
```

```
set FLASK_ENV=development
```


5. **(Optional) Initialise the database:**

To create the initial database, you can use the Flask CLI command:

```
flask init-db
```


6. **Run the application:**

```
python app.py
```

Alternatively you may use the Flask commmand:

```
'flask run'
```

After running the command, you should see output in app.log that the server is running. By default, the server will be accessible at `http://127.0.0.1:5000`.

7. **Running the tests**

To run the automated tests for this web application, use the following commands:

```
pytest -v
```

### Coverage

To check the test coverage, you can use the following command:

```
pytest --cov=webapp
```

For an HTML report of the coverage, run:

```
pytest --cov=webapp --cov-report html
```

## Authors

* **Rakin Ahmed** 


## References

Liang Zhao, Olga Gkountouna, and Dieter Pfoser. 2019. Spatial Auto-regressive Dependency Interpretable Learning Based on Spatial Topological Constraints. ACM Trans. Spatial Algorithms Syst. 5, 3, Article 19 (August 2019), 28 pages. DOI: https://doi.org/10.1145/3339823








#  Banking API
A FastAPI-based banking application that provides user registration, authentication, balance checking, and money transfers.
For more information on why I chose FastAPI, Schema explanation, and architecture, please take a look at the write up that is included.


## TODO: 
If your DB connections are different than the ones provided in these steps, please search for "TODO" in the project files and you will find where those
connection variables need to change.

## Dockered app:

This app is now dockerized and the only thing you need to do is is run Docker Desktop then:

`docker-compose up --build`

This will build the entire app for you and install all the dependencies.

The API will now be running at (THIS IS THE SSR FRONTEND):   
`http://localhost:8000`

For the SPA Frontend (please note it takes a minute to start up and wont be available right away):
`http://localhost:5173`

The grafana dashboard will be running at:
`http://localhost:3000`

The Prometheus dashboard will be running at:
`http://localhost:9090`


## Grafana:
Included is the grafana-yaml.txt. If for whatever reason Grafana dashboard is not saved, you can import the grafana dashboard manually. 
Please note that you will not be able to import the file, but you can just copy and paste the dashboard into the text field that expects JSON.

Set the time of data to 5 minutes and refresh since there is not much data to run off of for our graphs to look populated.

### **API Documentation**

After starting the server, you can view the Swagger UI and OpenAPI JSON which can be converted online to a YAML if needed:

-   **Swagger Docs**: http://localhost:8000/docs
-   **OpenAPI JSON**: http://localhost:8000/openapi.json

## **Running Tests**

To run tests, ensure you have `pytest` installed (included in requirements.txt) then run:
`python -m pytest tests`

NOTE: Due to the limiter, some tests will need to be ran solo and not in the the script above. 
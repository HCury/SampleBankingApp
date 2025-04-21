# This file initializes and configures the FastAPI application. It includes the following key components:
# - Imports: Necessary libraries and modules, including FastAPI, SQLAlchemy, Prometheus metrics, logging, and CORS middleware.
# - App Initialization: Creates an instance of FastAPI and initializes the database.
# - Logging: Configured using loguru to log information and errors to a JSON file.
# - Routers: Includes routers for authentication, balance, transactions, transfers, and registration routes.
# - Middleware: Adds CORS and rate limiting middleware, and tracks API requests and response times.
# - Exception Handlers: Custom handlers for HTTP exceptions, validation errors, and generic exceptions.
# - Prometheus Metrics: Counters and histograms to track API requests, response times, and exceptions.
# - Static Files: Serves static files and templates for SSR.
# - HTML Endpoints: Defines endpoints for rendering HTML pages.
# - Metrics Endpoint: Exposes Prometheus metrics.
# - Main Entry Point: Runs the application using uvicorn.

from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from prometheus_client import Counter, Histogram, generate_latest
from slowapi.middleware import SlowAPIMiddleware
from loguru import logger
import time
import traceback

from rate_limiter import limiter
from database import init_db
from routes import auth_routes, balance_routes, transactions_routes, transfer_routes, registration_routes

# Initialize FastAPI app
app = FastAPI()
app.state.limiter = limiter
init_db()

# Configure logging
logger.add("logs.json", format="{time} {level} {message}", level="INFO", rotation="1 week", serialize=True)

# Include routers
app.include_router(auth_routes.router)
app.include_router(balance_routes.router)
app.include_router(transactions_routes.router)
app.include_router(transfer_routes.router)
app.include_router(registration_routes.router)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SlowAPIMiddleware)

# Prometheus Metrics
REQUEST_COUNT = Counter("request_count", "Total number of API requests", ["method", "endpoint"])
REQUEST_LATENCY = Histogram("request_latency_seconds", "Request latency in seconds", ["method", "endpoint"])
RESPONSE_STATUS = Counter("response_status", "Response status count", ["status_code"])
EXCEPTION_COUNT = Counter("exception_count", "Total exceptions raised", ["endpoint"])

# Serve static files
templates = Jinja2Templates(directory="ssr-frontend/templates")
app.mount("/static", StaticFiles(directory="ssr-frontend/static"), name="static")


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.warning(f"HTTPException | Path: {request.url.path} | Status: {exc.status_code} | Detail: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"ValidationError | Path: {request.url.path} | Errors: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"error": "Validation failed", "details": exc.errors()},
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    error_trace = traceback.format_exc()
    logger.error(f"Unhandled Exception | Path: {request.url.path} | Error: {str(exc)}\n{error_trace}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"},
    )

# Middleware to track API requests and response times
@app.middleware("http")
async def track_requests(request: Request, call_next):
    method = request.method
    endpoint = request.url.path
    client_ip = request.client.host

    REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()

    start_time = time.time()
    try:
        response = await call_next(request)
        latency = time.time() - start_time
        REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(latency)
        RESPONSE_STATUS.labels(status_code=response.status_code).inc()

        # Log API requests
        logger.info(f"Request: {method} {endpoint} | Status: {response.status_code} | Latency: {latency:.4f}s | IP: {client_ip}")

        return response
    except Exception as e:
        EXCEPTION_COUNT.labels(endpoint=endpoint).inc()

        # Log errors
        logger.error(f"Exception at {endpoint} | Method: {method} | IP: {client_ip} | Error: {str(e)}")
        raise


# Expose Prometheus metrics
@app.get("/metrics")
def get_metrics():
    return Response(generate_latest(), media_type="text/plain")


# HTML Endpoints (SSR)
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

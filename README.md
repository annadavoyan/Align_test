# Align_test
# Aligh_test
# Employee Application

This project is a web application that processes a photo of an Employee ID tag and additional employee information, then saves it to a database. It consists of two microservices.

## Service 1: Web Application

Handles client requests and stores data.

- **Port:** 8800

### Endpoints

- `POST /employees/new`: Add a new employee
- `GET /employees/list`: List existing employees
- `GET /employees/{id}`: Get employee information

## Service 2: Image Processing

Interacts with Service 1 to process the employee ID image.

- **Port:** 9000

### Endpoint

- `POST /image`: Process an image and return the employee ID

## Setup Instructions

### Prerequisites

- Python 3.11
- Virtual environment setup

### Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/your_username/your_repository_name.git
   cd your_repository_name


###Create and activate a virtual environment:
python -m venv env
.\env\Scripts\activate  # Windows
source env/bin/activate  # macOS/Linux

###Install the dependencies:
pip install -r requirements.txt


###Running the Application
Start Service 2 (Image Processing):
cd service_2
uvicorn main:app --host 0.0.0.0 --port 9000 --reload


Open a new terminal and start Service 1 (Web Application):
cd service_1
uvicorn main:app --host 0.0.0.0 --port 8800 --reload

Testing the Application
Open http://127.0.0.1:8800/docs in your browser.
Use the Swagger UI to interact with the endpoints.

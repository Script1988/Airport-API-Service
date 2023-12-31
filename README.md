# Airport-API-Service
System for tracking flights from airports across the globe. Project helps potential customers of 
our airline to find the best route from one country to another using various filters.

# Features
* JWT authentication
* Email authorization
* Creating and updating crew, routes, flights, airports etc.
* Managing orders and tickets
* Filtering flight source airport, destination airport, source city and destination city
* Filtering flight by departure time
* Detailed route and flight info
* Ticket validation
* Admin panel
* Documentation in swagger and redoc


# Getting access
* create a new user `user/register/`
* download ModHeader extension for your browser
* get access token from `user/token/`
* create request header in ModHeader extension
* write Authorization in the first line
* write Bearer and paste access token from `user/token/` in the second line


# Installing using git
* Install PostgresSQL
* Create DB
* `git clone https://github.com/Script1988/Airport-API-Service.git`
* `python -m venv venv`
* `venv\Scripts\activate (on Windows)`
* `source venv/bin/activate (on macOS)`
* `pip install -r requirements.txt`
* create `.env` file in the root directory
* set all environment variables in `.env` file using examples from `.env.sample`
* set POSTGRES_USER = your username
* set POSTGRES_PASSWORD = your password
* set SECRET_KEY = your secret key
* `python manage.py migrate`
* `python manage.py runserver`
* you can load data from fixture for testing. Just use ` python manage.py loaddata sample_data.json`


![Airport schema](readme_photos/airport_schema.png)  
![API root](readme_photos/api_root.png)  
![Route detail](readme_photos/route_detail.png)  
![Flight list](readme_photos/flight_list.png)  
![Flight detail](readme_photos/flight_detail.png)  

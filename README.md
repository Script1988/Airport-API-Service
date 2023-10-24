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
* set DB_HOST = your db_hostname
* set DB_NAME = your db_name 
* set DB_USER = your db_username
* set DB_PASSWORD = your db_password
* set SECRET_KEY = your secret key
* `python manage.py migrate`
* `python manage.py runserver`

# Run with docker
* Install Docker
* `docker-compose build`
* `docker-compose up`


![Actors list](readme_photos/api_root.png)  
![Api root](readme_photos/route_detail.png)  
![Movie detail](readme_photos/flight_list.png)  
![Token obtain](readme_photos/flight_detail.png) 
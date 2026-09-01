# Fuel Route Optimization API

A Django REST API that calculates a driving route between two USA locations and recommends cost-effective fuel stops along the route.

The API uses a maximum vehicle range of 500 miles and assumes fuel efficiency of 10 miles per gallon (MPG).

## Features

- Accepts start and finish locations within the USA
- Geocodes locations using OpenStreetMap Nominatim
- Calculates driving routes using OSRM
- Returns route distance and duration
- Returns the route as GeoJSON geometry
- Uses the provided fuel-price CSV dataset
- Finds fuel stations along the route
- Supports a maximum vehicle range of 500 miles
- Selects cost-effective fuel stops based on fuel prices
- Calculates fuel consumption using 10 MPG
- Calculates total fuel cost
- Provides API validation and error handling
- Includes unit and API tests

## Tech Stack

- Python
- Django 6.1
- Django REST Framework
- SQLite
- OpenStreetMap Nominatim
- OSRM Routing API

## Project Structure

```text
fuel-route-api/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── fuel/
│   ├── models.py
│   ├── migrations/
│   └── management/
│       └── commands/
│           ├── import_fuel_prices.py
│           ├── clean_station_data.py
│           └── geocode_stations.py
│
├── routing/
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── services/
│   │   ├── geocoding_service.py
│   │   ├── routing_service.py
│   │   ├── station_service.py
│   │   └── fuel_optimizer.py
│   └── tests/
│       ├── test_api.py
│       ├── test_optimizer.py
│       └── test_station_service.py
│
├── data/
│   └── fuel-prices-for-be-assessment.csv
│
├── manage.py
├── requirements.txt
└── README.md
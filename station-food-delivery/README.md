# Station Food Delivery 🚉🍱

StationEats is a Flask prototype for delivering food from one station to another station or district station.

## Problem
Passengers travelling by train or bus may not have enough time to buy food at a station. This system lets a passenger order food in advance, select a destination station, and receive the meal there.

## Main flow
Customer → Select source station → Select destination station → Select food → Enter coach/seat → Place order → Track status → Delivery at destination station

## Order status
1. Order Confirmed
2. Preparing Food
3. At Source Station
4. In Transit
5. Reached Destination Station
6. Delivered

## Features
- Station-to-station food ordering
- Food menu and quantity
- Coach/seat or pickup reference
- Order tracking page
- Admin/delivery dashboard
- Status updates
- SQLite database
- JSON APIs
- Responsive presentation-friendly UI

## Run in VS Code
1. Open the station-food-delivery folder.
2. Run: python -m venv venv
3. Run: venv\Scripts\activate
4. Run: pip install -r requirements.txt
5. Run: python app.py
6. Open http://127.0.0.1:5000
7. Admin demo: http://127.0.0.1:5000/admin

## Presentation example
A passenger travelling Visakhapatnam → Vijayawada can order Chicken Biryani and provide a coach/seat reference. The food is prepared, taken to the source station, transported through the route, and marked delivered when it reaches Vijayawada.

This is a college/demo prototype. Real railway access, live train location, payment gateways, identity verification and station/vendor partnerships would require production integrations and authorization.

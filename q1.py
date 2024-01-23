# Defining a class for the passengers to include in all of the following Passenger name, passport number, DOB, membership status
class Passenger:
    def __init__(self, name, passport, DOB, membership_tier):
        self.name = name
        self.passport = passport
        self.DOB = DOB
        # this membership status will be set to only gold, silver or non-member
        self.membership_tier = membership_tier

# Defininf a class to include the flight details such as Flight number, maximum capacity, departure (location date and time), arrival (location date and time), list of confirmed passengers and list of passenger under waiting list
class Flight:
    def __init__(self, flight_number, max_capacity, departure, arrival):
        self.flight_number = flight_number
        self.max_capacity = max_capacity
        # This departure and arrival will be set to the location, date and time
        self.departure = departure
        # This arrival will be set to the location, date and time
        self.arrival = arrival
        self.confirmed_passengers = []
        self.waiting_list = []

# Defining a class to act as the overall system to include the list of flights and the list of passengers
class AirlineReservationSystem:
        # This initisalises the list of flights and the list of passengers
        def __init__(self):
            self.flights = []
            self.passengers = []

        # This function will be used to add passengers to the list of passengers
        def add_passenger(self, name, passport, DOB, membership_tier):
            passenger = Passenger(name, passport, DOB, membership_tier)
            self.passengers.append(passenger)

        # This function will be used to add flights to the list of flights
        def add_flight(self, flight_number, max_capacity, departure, arrival):
            flight = Flight(flight_number, max_capacity, departure, arrival)
            self.flights.append(flight)

        # This function will be used to add passengers to the confirmed passenger flight
        def add_passenger_to_flight(self, flight_number, passenger_index):
            flight = next((f for f in self.flights if f.flight_number == flight_number), None)
            if flight:
                if len(flight.confirmed_passengers) < flight.max_capacity:
                    flight.confirmed_passengers.append(self.passengers[passenger_index])
                else:
                    flight.waiting_list.append(self.passengers[passenger_index])

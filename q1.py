# Import a priority queue algotrithm to be used in the waiting list
import heapq


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

     # This function will be used to add passenger to the waiting list
    def add_passenger_to_waiting_list(self, flight_number, passenger):
        # Use a tuple (priority, passenger) where priority is based on membership tier
        priority = {'gold': 1, 'silver': 2, 'non-member': 3}[passenger.membership_tier]
        heapq.heappush(self.waiting_list, (priority, passenger))

    # This function will be used to assign the passenger from the waiting list
    def assign_passenger_from_waiting_list(self):
        if self.waiting_list:
            # This will assign the passenger from the waiting list to the confirmed passenger list
            _, passenger = heapq.heappop(self.waiting_list)
            self.confirmed_passengers.append(passenger)

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

        # This function will be be used to get all of the names of the passengers in the confirmed passenger list
        def get_passenger_on_flight(self, flight_number):
            # This finds the flights with the flight number in the list of flights
            # This will return a value of none if the flight number is not found
            flight = next((f for f in self.flights if f.flight_number == flight_number), None)
            # Checking if the flight exists and if it has a confirmed passenger list
            if flight and flight.confirmed_passengers:
                # This returns the name of the passenger in the confirmed passenger list
                return [p.name for p in flight.confirmed_passengers]

        # This function will be used to get the sorted list of flights based on their occupancy
        def get_flights_with_highest_occupancy(self):
            # Sorting of the flights by occupancy
            sorted_flights = sorted(self.flights, key=lambda x: len(x.confirmed_passengers) / x.max_capacity, reverse=True)
            # Return the flight numbers of the sorted flights
            return [flight.flight_number for flight in sorted_flights]
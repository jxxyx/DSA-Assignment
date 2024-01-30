# Import a priority queue algotrithm to be used in the waiting list
import heapq
import random
import string
from collections import deque


# Defining a class for the passengers to include in all of the following Passenger name, passport number, DOB, membership status
class Passenger:
    def __init__(self, name, passport, DOB, membership_tier):
        self.name = name
        self.passport = passport
        self.DOB = DOB
        # this membership status will be set to only gold, silver or non-member
        self.membership_tier = membership_tier

# Defining a class to include the flight details such as Flight number, maximum capacity, departure (location date and time), arrival (location date and time), list of confirmed passengers and list of passenger under waiting list
class Flight:
    def __init__(self, flight_number, max_capacity, departure, arrival):
        self.flight_number = flight_number
        self.max_capacity = max_capacity
        # This departure and arrival will be set to the location, date and time
        self.departure = departure
        # This arrival will be set to the location, date and time
        self.arrival = arrival
        self.confirmed_passengers = set() # This initialises the confirmed passenger as a set
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
            # Making the passengers and flights a dictionary
            self.flights = {}
            self.passengers = {}
            self.waiting_list = {'gold' : deque(), 'silver' : deque(), 'non-member' : deque()}

        # This function will be used to add passengers to the list of passengers
        def add_passenger(self, name, passport, DOB, membership_tier):
            passenger = Passenger(name, passport, DOB, membership_tier)
            self.passengers[passport] = passenger

        # This function will be used to add flights to the list of flights
        def add_flight(self, flight_number, max_capacity, departure, arrival):
            flight = Flight(flight_number, max_capacity, departure, arrival)
            self.flights[flight_number] = flight

        # This function will be used to add passengers to the confirmed passenger flight
        def add_passenger_to_flight(self, flight_number, passport):
            flight = self.flights.get(flight_number)
            passenger = self.passengers.get(passport)
            if flight and passenger:
                if len(flight.confirmed_passengers) < flight.max_capacity:
                    flight.confirmed_passengers.add(passenger)
                else:
                    self.waiting_list[passenger.membership_tier].append((flight, passenger))

        # This function will be be used to get all of the names of the passengers in the confirmed passenger list
        def get_passenger_on_flight(self, flight_number):
            flight = self.flights.get(flight_number)
            if flight and flight.confirmed_passengers:
                return [p.name for p in flight.confirmed_passengers]

        # This function will be used to get the sorted list of flights based on their occupancy
        def get_flights_with_highest_occupancy(self):
            sorted_flights = sorted(self.flights.values(), key=lambda x: len(x.confirmed_passengers) / x.max_capacity, reverse=True)
            return [flight.flight_number for flight in sorted_flights]
        
        def assign_passenger_from_waiting_list(self):
            for tier in ['gold', 'silver', 'non-member']:
                while self.waiting_list[tier]:
                    flight, passenger = self.waiting_list[tier].popleft()
                    if len(flight.confirmed_passengers) < flight.max_capacity:
                        flight.confirmed_passengers.add(passenger)
                        return passenger
            

# This is to generate random passengers and flights
def generate_random_passengers_and_flights():
    system = AirlineReservationSystem()
    # This will generate a list of random passengers
    for _ in range(150000):
        name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        passport = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        DOB = "01-01-1990"
        membership_tier = random.choice(['gold', 'silver', 'non-member'])
        system.add_passenger(name, passport, DOB, membership_tier)

    # This will generate a list of random flights
    for _ in range(250):
        flight_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        max_capacity = random.randint(400, 500)
        departure = "Location1, Date1, Time1"
        arrival = "Location2, Date2, Time2"
        system.add_flight(flight_number, max_capacity, departure, arrival)

    return system

def main():
    system = generate_random_passengers_and_flights()

    while True:
        print("\n1. Add passengers to flight")
        print("2. Retreiving passengers on flight")
        print("3. Assign passengers to Flight")
        print("4. Retreiving flights with highest occupancy")
        print("5. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            # This will add passengers to the flight
            flight_number = input("Enter flight number: ")
            passport = input("Enter passport number: ")
            print("Passengers added to flight")
            print(system.add_passenger_to_flight(flight_number, passport))

        # This is to retrieve passenger info from specific flight
        elif choice == "2":
            # Give user a prompt on what flight number to enter
            flight_number = input("Enter flight number: ")

            # This will retreive the passengers on the flight
            print("Retreiving passengers on flight")
            print(system.get_passenger_on_flight(flight_number))

        elif choice == "3":
            # This will assign passengers to the flight
            print("Assigning passengers to flight")
            print(system.assign_passenger_from_waiting_list())
        
        elif choice == "4":
            # This will retreive the flights with the highest occupancy
            print("Retreiving flights with highest occupancy")
            print(system.get_flights_with_highest_occupancy())


        elif choice == "5":
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
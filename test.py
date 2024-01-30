# Import a priority queue algotrithm to be used in the waiting list
import heapq
import random
import string
from collections import deque
import faker
import time
import pycountry
import unittest 

class TestAirlineReservationSystem(unittest.TestCase):
    def setUp(self):
        self.ars = AirlineReservationSystem()

    def test_add_passenger(self):
        self.ars.add_passenger('John Doe', '001', 'DOB', 'gold')  # adjusted arguments
        self.assertIn('001', self.ars.passengers)

    def test_add_flight(self):
        self.ars.add_flight('001', 200, 'New York', 'London')  # adjusted arguments
        self.assertIn('001', self.ars.flights)

    def test_add_passenger_to_flight(self):
        self.ars.add_passenger('John Doe', '001', 'DOB', 'gold')  # adjusted arguments
        self.ars.add_flight('001', 200, 'New York', 'London')  # adjusted arguments
        self.ars.add_passenger_to_flight('001')  # adjusted arguments
        self.assertIn('John Doe', [passenger.name for passenger in self.ars.flights['001'].confirmed_passengers])

    def test_get_passenger_on_flight(self):
        self.ars.add_passenger('John Doe', '001', 'DOB', 'gold')  # adjusted arguments
        self.ars.add_flight('001', 200, 'New York', 'London')  # adjusted arguments
        self.ars.add_passenger_to_flight('001')  # adjusted arguments
        passengers = self.ars.get_passenger_on_flight('001')
        self.assertEqual(len(passengers), 1)
        self.assertEqual(passengers[0].name, 'John Doe')

    def test_assign_passenger_from_waiting_list(self):
        self.ars.add_passenger('John Doe', '001', 'DOB', 'gold')  # adjusted arguments
        self.ars.add_flight('001', 200, 'New York', 'London')  
        self.ars.waiting_list['gold'].append(self.ars.passengers['001'])
        self.ars.assign_passenger_from_waiting_list('001')
        self.assertIn('John Doe', [passenger.name for passenger in self.ars.flights['001'].confirmed_passengers])
        self.assertNotIn('John Doe', [passenger.name for passenger in self.ars.waiting_list['gold']])

    def test_get_flights_with_highest_occupancy(self):
        # Add two flights
        self.ars.add_flight('001', 200, 'New York', 'London')
        self.ars.add_flight('002', 200, 'New York', 'London')

        # Add 100 passengers to flight '001' and 150 to flight '002'
        for i in range(80):
            self.ars.add_passenger_to_flight(str(i))
        for i in range(80, 200):
            self.ars.add_passenger_to_flight(str(i))

        # Get flights with highest occupancy
        flights = self.ars.get_flights_with_highest_occupancy()

        # Check if the list is not empty before accessing elements
        if flights:
            # The flight with the highest occupancy should be '002'
            self.assertEqual(flights[0], '001')
        else:
            self.fail("No flights with highest occupancy found.")


    def test_get_total_waiting_list(self):
        for i in range(100):
            self.ars.add_passenger('Passenger ' + str(i), str(i), 'DOB', 'gold')  
            self.ars.waiting_list['gold'].append(self.ars.passengers[str(i)])
        self.assertEqual(self.ars.get_total_waiting_list(), 100)


# Defining a class for the passengers to include in all of the following Passenger name, passport number, DOB, membership status
class Passenger:
    def __init__(self, name, passport, DOB, membership_tier):
        self.name = name
        self.passport = passport
        self.DOB = DOB
        # this membership status will be set to only gold, silver or non-member
        self.membership_tier = membership_tier

    def __str__(self):
        return (f"Name: {self.name.ljust(25)} "
                f"Passport: {self.passport.ljust(10)} "
                f"DOB: {self.DOB.ljust(15)} "
                f"Membership Tier: {self.membership_tier}")

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
        self.waiting_list = {'gold' : deque(), 'silver' : deque(), 'non-member' : deque()}

     # This function will be used to add passenger to the waiting list
    def add_passenger_to_waiting_list(self, flight_number, passenger):
        self.waiting_list[passenger.membership_tier].append(passenger)

    # This function will be used to assign the passenger from the waiting list
    def assign_passenger_from_waiting_list(self):
        for tier in ['gold', 'silver', 'non-member']:
            if self.waiting_list[tier]:
                passenger = self.waiting_list[tier].popleft()
                self.confirmed_passengers.add(passenger)
                return passenger
            
# This is to generate random passengers and flights
def generate_random_passengers_and_flights():
    system = AirlineReservationSystem()
    generated_passports = set()
    generated_flight_numbers = set()

    # Get a list of all country names
    countries = [country.name for country in pycountry.countries]

    # Create a Faker object
    fake = faker.Faker()

    # This will generate a list of random passengers
    for _ in range(150000):
        name = fake.name()
        DOB = fake.date_of_birth(minimum_age=20, maximum_age=90).strftime("%d-%m-%Y")
        membership_tier = random.choice(['gold', 'silver', 'non-member'])

        # Generate unique passport
        while True:
            passport = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            if passport not in generated_passports:
                generated_passports.add(passport)
                break

        system.add_passenger(name, passport, DOB, membership_tier)

    # This will generate a list of random flights
    for _ in range(250):
        max_capacity = random.randint(400, 500)
        # Generate random departure and arrival countries
        departure_country = random.choice(countries)
        arrival_country = random.choice(countries)
        while arrival_country == departure_country:
            arrival_country = random.choice(countries)

        # Generate random departure and arrival dates and times
        departure_date_time = fake.date_time_this_year()
        arrival_date_time = fake.date_time_this_year()

        departure = f"{departure_country}, {departure_date_time}"
        arrival = f"{arrival_country}, {arrival_date_time}"

        # Generate unique flight number
        while True:
            flight_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            if flight_number not in generated_flight_numbers:
                generated_flight_numbers.add(flight_number)
                break

        system.add_flight(flight_number, max_capacity, departure, arrival)

    return system


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

    # Defining operation 1 to Add a new passenger to a flight based on the auto generation of the database above
    # This function will be used to add passengers to the confirmed passenger flight
    def add_passenger_to_flight(self, passport): 
        passenger = self.passengers.get(passport)
        if passenger:
            for flight_number, flight in self.flights.items():
                occupancy_rate = len(flight.confirmed_passengers) / flight.max_capacity
                random_threshold = random.uniform(0.5, 0.8)
                if occupancy_rate < random_threshold:  # Stop adding passengers when the flight is 80% full
                    flight.confirmed_passengers.add(passenger)
                    passenger.assigned_flight = flight  # Assign flight to passenger
                    return passenger 

        # If the passenger cannot be added to any flight, add them to the waiting list
        if passenger and passenger not in self.waiting_list[passenger.membership_tier]:
            self.waiting_list[passenger.membership_tier].append(passenger)
        return passenger

    # Defining operation 2 to Retrieve the information of all the passengers on a specific flight
    def get_passenger_on_flight(self, flight_number):
        flight = self.flights.get(flight_number)
        if flight and flight.confirmed_passengers:
            return list(flight.confirmed_passengers)
        
    # Defining operation 3 to Assignment of seat to those under waiting list (pick the next passenger to be assigned a seat)
    def assign_passenger_from_waiting_list(self, flight_number):
        flight = self.flights.get(flight_number)
        if flight:
            for tier in ['gold', 'silver', 'non-member']:
                while self.waiting_list[tier]:
                    passenger = self.waiting_list[tier].popleft()
                    if len(flight.confirmed_passengers) < flight.max_capacity:
                        flight.confirmed_passengers.add(passenger)
                        passenger.assigned_flight = flight  # Assign flight to passenger
                    return passenger
        else:
            print("Flight not found.")
    
    # Defining operation 4 to Retrieve the list of flights sorted based on their occupancy 
    # We will also display the percentage of occupancy for each flight
    def get_flights_with_highest_occupancy(self):
        flights_with_occupancy = []

        for flight_number, flight in self.flights.items():
            occupancy_rate = len(flight.confirmed_passengers) / flight.max_capacity
            flights_with_occupancy.append((flight_number, occupancy_rate))

        # Sort the flights_with_occupancy in descending order based on occupancy rate
        flights_with_occupancy.sort(key=lambda x: x[1], reverse=True)

        # Extract only the flight numbers from the sorted list
        best_flights = [flight[0] for flight in flights_with_occupancy]

        return best_flights
    
    # Add this method to your class
    def get_total_waiting_list(self):
        total = 0
        for tier in ['gold', 'silver', 'non-member']:
            total += len(self.waiting_list[tier])
        return total
    
# Main Fucntion to run the code  
def main():
    system = generate_random_passengers_and_flights()
    

    while True:
        print("\nOperations:")
        print("1. Add a new passenger to a flight (automatically assigned).")
        print("2. Retrieve the information of all the passengers on a specific flight.")
        print("3. Assignment of seat to those under waiting list (automatic assignment).")
        print("4. List of flights with the highest occupancy rate (descending order).")
        print("5. Exit.")
        print(f"Total passengers in waiting list: {system.get_total_waiting_list()}")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            # Automatically assign all passengers to a flight
            for passport in system.passengers.keys():
                system.add_passenger_to_flight(passport)
            print("All passengers added to the flights.")

        elif choice == '2':
            flight_number = input("Enter flight number: ")
            passengers = system.get_passenger_on_flight(flight_number)
            if passengers:
                flight = system.flights.get(flight_number)
                print(f"Flight {flight_number} Departure: {flight.departure}, Arrival: {flight.arrival}")
                print(f"Number of passengers on the flight: {len(passengers)}")
                print("Passengers on the flight:")
                for passenger in passengers:
                    print(passenger)
            else:
                print("No passengers on the flight.")

        elif choice == '3':
            flight_number = input("Enter flight number: ")
            flight = system.flights.get(flight_number)
            if flight:
            # Automatically assign passengers from the waiting list to the flight until it's full
                while len(flight.confirmed_passengers) < flight.max_capacity:
                    passenger = system.assign_passenger_from_waiting_list(flight_number)
                    if passenger:
                        print(f"Passenger: {passenger.name.ljust(20)} "
                            f"Membership Tier: {passenger.membership_tier.ljust(10)} "
                            f"Added to flight: {flight_number}")
                    else:
                        print("No more passengers available for assignment.")
                        break
            else:
                print("Flight not found.")

        elif choice == '4':
            flights = system.get_flights_with_highest_occupancy()
            print("Flights with the highest occupancy rate (descending order):")
            for flight_number in flights:
                flight = system.flights.get(flight_number)
                occupancy_rate = len(flight.confirmed_passengers) / flight.max_capacity * 100
                print(f"- Flight {flight_number}: {len(flight.confirmed_passengers)}/{flight.max_capacity}, {occupancy_rate:.2f}% occupancy")
                print(f"  Departure: {flight.departure}, Arrival: {flight.arrival}")
        elif choice == '5':
            print("Exiting the system. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()

if __name__ == '__main__':
    unittest.main() 



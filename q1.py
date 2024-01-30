# Import a priority queue algorithm to be used in the waiting list
import heapq
import re  # Added import for regular expressions
from datetime import datetime  # Added import for handling dates
import random
import string
from collections import deque

# Generate random passenger data
for _ in range(150000):
    name = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=5))
    passport = ''.join(random.choices(string.ascii_uppercase, k=1)) + ''.join(random.choices(string.digits, k=8))
    DOB = f"{random.randint(1950, 2002)}-{random.randint(1, 12)}-{random.randint(1, 28)}"
    membership_tier = random.choice(['gold', 'silver', 'non-member'])
    airline_system.add_passenger(name, passport, DOB, membership_tier)

# Generate random flight data
for i in range(250):
    flight_number = f"FL{i}"
    max_capacity = random.randint(100, 500)
    departure = f"Location{i} 2022-{random.randint(1, 12)}-{random.randint(1, 28)} {random.randint(0, 23)}:{random.randint(0, 59)}"
    arrival = f"Location{i+250} 2022-{random.randint(1, 12)}-{random.randint(1, 28)} {random.randint(0, 23)}:{random.randint(0, 59)}"
    airline_system.add_flight(flight_number, max_capacity, departure, arrival)

# Defining a class for the passengers to include in all of the following Passenger name, passport number, DOB, membership status
class Passenger:
    def init(self, name, passport, DOB, membership_tier):
        self.name = name
        self.passport = passport
        self.DOB = DOB
        # this membership status will be set to only gold, silver, or non-member
        self.membership_tier = membership_tier.lower()  # Convert to lowercase

# Defining a class to include the flight details such as Flight number, maximum capacity, departure (location date and time),
# arrival (location date and time), list of confirmed passengers, and list of passengers under the waiting list
class Flight:
    def init(self, flight_number, max_capacity, departure, arrival):
        self.flight_number = flight_number
        self.max_capacity = max_capacity
        # This departure and arrival will be set to the location, date, and time
        self.departure_location, self.departure_date, self.departure_time = departure.split()
        # This arrival will be set to the location, date, and time
        self.arrival_location, self.arrival_date, self.arrival_time = arrival.split()
        self.confirmed_passengers = []  # List to store confirmed passengers
        self.waiting_list = []  # Priority queue to store passengers in the waiting list

    # This function will be used to add a passenger to the waiting list
    def add_passenger_to_waiting_list(self, passenger):
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
    # This initializes the list of flights and the list of passengers
    def init(self):
        self.flights = []  # List to store flight objects
        self.passengers = []  # List to store passenger objects
        self.waiting_list = {'gold': deque(), 'silver': deque(), 'non-member': deque()}

    def add_flight(self, flight_number, max_capacity):
        flight_number_pattern = re.compile(r'^[a-zA-Z]{2}\d{3}$', re.IGNORECASE)
        if not flight_number_pattern.match(flight_number):
            print("Invalid flight number format. Please enter in the format: 2 letters followed by 3 numbers.")
            return
        
        flight_number = flight_number.upper()  # Convert to uppercase
        while True:
            departure_time = input("Enter departure time (HH:MM): ")
            departure_date = input("Enter departure date (YYYY-MM-DD): ")

            departure_time =input("Enter departure time (HH:MM): ")
            if not self.validate_time(departure_time):
                print("Invalid time format. Please enter the time in 24-hour format (HH:MM). Retry.")
                continue

            departure = f"{departure_location} {departure_date} {departure_time}"

            if self.validate_datetime(departure_date, departure_time):
                departure_time = datetime.strptime(f"{departure_date} {departure_time}", "%Y-%m-%d %H:%M")
                if departure_time < datetime.now():
                    print("Departure time cannot be in the past. Please retry.")
                    continue
                break
            else:
                print("Invalid date or time format. Please retry.")

    # This function will be used to add passengers to the list of passengers
    def add_passenger(self, name, passport, DOB, membership_tier):
        while True:
            # Validate and format passport number
            passport_pattern = re.compile(r'^[a-zA-Z]\d{8}$', re.IGNORECASE)
            if not passport_pattern.match(passport):
                passport = input("Invalid passport number format. Please enter in the format: 1 letter followed by 8 numbers. Retry: ")
                continue

            passport = passport.upper()  # Convert to uppercase

            # Validate and format date of birth
            try:
                dob = datetime.strptime(DOB, "%Y-%m-%d").date()
            except ValueError:
                DOB = input("Invalid date of birth format. Please enter in the format: YYYY-MM-DD. Retry: ")
                continue

            # Validate membership tier
            if membership_tier.lower() not in {'gold', 'silver', 'non-member'}:
                membership_tier = input("Invalid membership tier. Please enter 'gold', 'silver', or 'non-member'. Retry: ").lower()
                continue

            passenger = Passenger(name, passport, dob, membership_tier)
            self.passengers.append(passenger)
            print(f"Passenger {name} added successfully!")
            break# This function will be used to add flights to the list of flights
    def add_flight(self, flight_number, max_capacity):
        # Validate and format departure input
        while True:
            departure_location = input("Enter departure location: ")
            departure_date = input("Enter departure date (YYYY-MM-DD): ")

            # Prompt user to enter time in 24-hour format
            departure_time = input("Enter departure time (HH:MM): ")
            if not self.validate_time(departure_time):
                print("Invalid time format. Please enter the time in 24-hour format (HH:MM). Retry.")
                continue

            departure = f"{departure_location} {departure_date} {departure_time}"

            # Validate datetime
            if self.validate_datetime(departure_date, departure_time):
                break
            else:
                print("Invalid date or time format. Please retry.")

        # Validate and format arrival input
        while True:
            arrival_location = input("Enter arrival location: ")
            arrival_date = input("Enter arrival date (YYYY-MM-DD): ")

            # Prompt user to enter time in 24-hour format
            arrival_time = input("Enter arrival time (HH:MM): ")
            if not self.validate_time(arrival_time):
                print("Invalid time format. Please enter the time in 24-hour format (HH:MM). Retry.")
                continue

            arrival = f"{arrival_location} {arrival_date} {arrival_time}"

            # Validate datetime
            if self.validate_datetime(arrival_date, arrival_time):
                break
            else:
                print("Invalid date or time format. Please retry.")

        while True:
            try:
                max_capacity = int(max_capacity)
            except ValueError:
                max_capacity = input("Invalid input for maximum capacity. Please enter a valid integer. Retry: ")
                continue

            self.flights.append(Flight(flight_number, max_capacity, departure, arrival))
            print(f"Flight {flight_number} added successfully!")
            break

    def validate_datetime(self, date_str, time_str):
        try:
            datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            return True
        except ValueError:
            return False

    def validate_time(self, time_str):
        try:
            datetime.strptime(time_str, "%H:%M")
            return True
        except ValueError:
            return False

    # This function will be used to add passengers to the confirmed passenger flight
    def add_passenger_to_flight(self, flight_number):
        while True:
            # Display passengers for selection
            print("Passengers:")
            for i, passenger in enumerate(self.passengers):
                print(f"{i}. {passenger.name}")

            try:
                passenger_index = int(input("Enter passenger index: "))
            except ValueError:
                print("Invalid input for passenger index. Please enter a valid integer.")
                continue

            flight = next((f for f in self.flights if f.flight_number == flight_number), None)
            if flight:
                if len(flight.confirmed_passengers) < flight.max_capacity:
                    flight.confirmed_passengers.append(self.passengers[passenger_index])
                    print(f"Passenger {self.passengers[passenger_index].name} added to flight {flight_number}")
                else:
                    flight.waiting_list.append(self.passengers[passenger_index])
                    print(f"Passenger {self.passengers[passenger_index].name} added to waiting list for flight {flight_number}")
                break
            else:
                print(f"Flight {flight_number} not found.")
                break# This function will be used to get all the information of the passengers on the flight
    def get_passenger_info_on_flight(self, flight_number):
        flight = next((f for f in self.flights if f.flight_number == flight_number), None)
        if flight and flight.confirmed_passengers:
            print(f"Passenger information on Flight {flight_number}:")
            for passenger in flight.confirmed_passengers:
                print(f"Name: {passenger.name}, Passport: {passenger.passport}, DOB: {passenger.DOB}, Membership: {passenger.membership_tier}")
        else:
            print(f"No passengers on Flight {flight_number}")

    # This function will be used to get the sorted list of flights based on their occupancy
    def get_flights_with_highest_occupancy(self):
        sorted_flights = sorted(self.flights, key=lambda x: len(x.confirmed_passengers) / x.max_capacity, reverse=True)
        print("Flights with highest occupancy:")
        for flight in sorted_flights:
            print(f"Flight {flight.flight_number}: {len(flight.confirmed_passengers)} / {flight.max_capacity} passengers")

# Example usage with a simple CLI UI
if name == "main":
    airline_system = AirlineReservationSystem()

    while True:
        print("\nAirline Reservation System")
        print("1. Add Passenger")
        print("2. Assign Seats from Waiting List")
        print("3. View Passenger Information on Flight")
        print("4. View Flights with Highest Occupancy")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter passenger name: ")
            passport = input("Enter passport number: ")
            dob = input("Enter date of birth (YYYY-MM-DD): ")
            membership_tier = input("Enter membership tier (gold/silver/non-member): ").lower()  # Convert to lowercase
            airline_system.add_passenger(name, passport, dob, membership_tier)

        elif choice == "2":
            flight_number = input("Enter flight number: ")
            flight = next((f for f in airline_system.flights if f.flight_number == flight_number), None)
            if flight:
                airline_system.assign_seats_from_waiting_list(flight)
            else:
                print(f"Flight {flight_number} not found.")

        elif choice == "3":
            flight_number = input("Enter flight number: ")
            airline_system.get_passenger_info_on_flight(flight_number)

        elif choice == "4":
            airline_system.get_flights_with_highest_occupancy()

        elif choice == "5":
            print("Exiting. Thank you!")
            break

        else:
            print("Invalid choice. Please enter a valid option.")
# DSA-Assignment

Passenger Information:

Use a hash table or a dictionary to store passenger information.
Key: Passport number
Value: Passenger details (name, passport number, DOB, membership status)
Flight Information:

Use an array or list to store information about each flight.
Each element represents a flight, containing details such as flight number, maximum capacity, departure, arrival, list of confirmed passengers, and list of passengers under the waiting list.
Waiting List:

Use a priority queue to manage the waiting list.
Priority is based on membership status (gold > silver > non-member) and then on a first-come-first-serve basis within the same status.
Operations:
Add a New Passenger to a Flight:

Add the passenger to the hash table.
If the flight has available seats, add the passenger to the confirmed list.
If the flight is full, add the passenger to the waiting list based on priority.
Time Complexity: O(1) for adding a passenger to the hash table, O(n) for adding to the waiting list or confirmed list (considering linear search in the list).

Space Complexity: O(n) for storing passenger information and flight details.

Retrieve Information of All Passengers on a Specific Flight:

Retrieve the flight details from the array.
Access the confirmed passenger list and waiting list.
Time Complexity: O(1) for retrieving flight details, O(n) for accessing the passenger lists.

Space Complexity: O(1) for retrieving flight details, O(n) for the passenger lists.

Assignment of Seat to Those Under Waiting List:

Dequeue the next passenger from the waiting list based on priority.
Assign a seat to the passenger in the confirmed list.
Time Complexity: O(log n) for dequeueing from the priority queue, O(1) for assigning a seat.

Space Complexity: O(1) for dequeueing from the priority queue, O(n) for assigning a seat.

List of Flights with the Highest Occupancy Rate:

Traverse the array of flight details.
Calculate the occupancy rate for each flight and maintain a list of flights with the highest occupancy.
Time Complexity: O(m * n), where m is the number of flights and n is the average number of passengers in each flight.

Space Complexity: O(m) for storing the list of flights with the highest occupancy.

Additional Considerations:
Use efficient searching algorithms for passenger lookup and seat assignment.
Implement proper error handling for edge cases, such as when a flight is full or when a passenger is already on the waiting list.
Implement appropriate data validation to ensure the integrity of the data in the system.

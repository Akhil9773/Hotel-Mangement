import mysql.connector as ms

# Connect to MySQL
con = ms.connect(host="localhost", user="root", passwd="9773", database="HOTEL_RESERVATION")
cur = con.cursor()

# Check if connected to MySQL
if con.is_connected():
    print("Connected to MySQL.")

##SQL CODE
##CREATE DATABASE IF NOT EXISTS HOTEL_RESERVATION;
##USE HOTEL_RESERVATION;
##CREATE TABLE IF NOT EXISTS HOTELS (
##    HOTEL_ID INT PRIMARY KEY,
##    NAME VARCHAR(100) NOT NULL,
##    LOCATION VARCHAR(50) NOT NULL);
##
##CREATE TABLE IF NOT EXISTS ROOMS (
##    ROOM_ID INT PRIMARY KEY,
##    HOTEL_ID INT,
##    ROOM_NUMBER INT NOT NULL,
##    CAPACITY INT,
##    PRICE DECIMAL(10, 2) NOT NULL,
##    AVAILABLE BOOLEAN,
##    FOREIGN KEY (HOTEL_ID) REFERENCES HOTELS(HOTEL_ID) ON DELETE CASCADE
##    );
##
##CREATE TABLE IF NOT EXISTS RESERVATIONS (
##    RESERVATION_ID INT PRIMARY KEY,
##    ROOM_ID INT,
##    CHECK_IN DATE NOT NULL,
##    CHECK_OUT DATE NOT NULL,
##    GUEST_NAME VARCHAR(100) NOT NULL,
##    STATUS VARCHAR(20) NOT NULL,
##    FOREIGN KEY (ROOM_ID) REFERENCES ROOMS(ROOM_ID) ON DELETE CASCADE
##
##);

# Function to add a hotel
def add_hotel():
    ch = "y"
    while ch.lower() == "y":
        hotel_id = int(input("Enter Hotel ID: "))
        name = input("Enter Hotel Name: ")
        location = input("Enter Hotel Location: ")

        q = "INSERT INTO HOTELS VALUES (%s, '%s', '%s')" % (hotel_id, name, location)

        cur.execute(q)
        con.commit()
        print("Hotel added.")
        ch = input("Press 'y' to add another hotel: ")

# Function to add a room
def add_room():
    ch = "y"
    while ch.lower() == "y":
        room_id = int(input("Enter Room ID: "))
        hotel_id = int(input("Enter Hotel ID: "))
        room_number = int(input("Enter Room Number: "))
        capacity = int(input("Enter Room Capacity: "))
        price = float(input("Enter Room Price: "))
        available = True  # Initially, the room is available

        q = "INSERT INTO ROOMS VALUES (%s, %s, %s, %s, %s, %s)" % (room_id, hotel_id, room_number, capacity, price, available)

        cur.execute(q)
        con.commit()
        print("Room added.")
        ch = input("Press 'y' to add another room: ")

# Function to book a room
def book_room():
    ch = "y"
    while ch.lower() == "y":
        room_id = int(input("Enter Room ID to book: "))
        check_in = input("Enter Check-in Date (YYYY-MM-DD): ")
        check_out = input("Enter Check-out Date (YYYY-MM-DD): ")
        guest_name = input("Enter Guest Name: ")

        # Check if the room is available for the specified dates
        availability_query = "SELECT AVAILABLE FROM ROOMS WHERE ROOM_ID = %s" % room_id
        cur.execute(availability_query)
        result = cur.fetchone()

        if result and result[0]:
            # Update room availability status
            update_query = "UPDATE ROOMS SET AVAILABLE = FALSE WHERE ROOM_ID = %s" % room_id
            cur.execute(update_query)
            con.commit()

            # Add reservation
            reservation_query = "INSERT INTO RESERVATIONS (ROOM_ID, CHECK_IN, CHECK_OUT, GUEST_NAME, STATUS) VALUES (%s, '%s', '%s', '%s', 'Booked')" % (room_id, check_in, check_out, guest_name)
            cur.execute(reservation_query)
            con.commit()

            print("Room booked.")
        else:
            print("Room is not available for the specified dates.")

        ch = input("Press 'y' to book another room: ")

# Function to display available rooms
def display_available_rooms():
    hotel_id = int(input("Enter Hotel ID to display available rooms: "))
    availability_query = "SELECT ROOM_NUMBER, CAPACITY, PRICE FROM ROOMS WHERE HOTEL_ID = %s AND AVAILABLE = TRUE" % hotel_id
    cur.execute(availability_query)
    results = cur.fetchall()

    if results:
        print("Available Rooms:")
        for row in results:
            print(f"Room Number: {row[0]}, Capacity: {row[1]}, Price: ${row[2]}")
    else:
        print("No available rooms.")

# Update and Delete functions can be added similarly

def display_menu():
    print("Hotel Reservation System")
    print("1. Add Hotel")
    print("2. Add Room")
    print("3. Book Room")
    print("4. Display Available Rooms")
    print("5. Exit")

def menu(choice):
    if choice == '1':
        add_hotel()
    elif choice == '2':
        add_room()
    elif choice == '3':
        book_room()
    elif choice == '4':
        display_available_rooms()
    elif choice == '5':
        print("Exiting...")
        exit()
    else:
        print("Invalid choice. Please enter a valid option.")

while True:
    display_menu()
    uc = input("Enter your choice (1-5): ")
    menu(uc)

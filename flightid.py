# Team 'Cheese' CanSat -- FlightID file

# Allows generation of flightID
from os import urandom, path

def init(): # Initially generates the ID
    global id
    id = urandom(5).hex()
    while path.exists(f"datadump/datadump_{id}"): # Rarely but possibly the id can be a duplicate. 
        id = urandom(5).hex()

def get(): # Returns the ID. 
    return id

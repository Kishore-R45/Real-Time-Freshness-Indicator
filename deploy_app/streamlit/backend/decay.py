from datetime import date
import math

# Ideal storage-based shelf-life (days) - Refrigerated
IDEAL_SHELF = {
    "apple": 35,
    "banana": 5,
    "tomato": 7,
    "orange": 28,
    "potato": 30,
    "cucumber": 10,
    "capsicum": 14,
    "okra": 3
}

# Normal room storage shelf-life (days)
ROOM_SHELF = {
    "apple": 7,
    "banana": 3,
    "tomato": 5,
    "orange": 10,
    "potato": 7,
    "cucumber": 3,
    "capsicum": 3,
    "okra": 1
}

# High humidity shelf-life (days)
HIGH_HUMIDITY_SHELF = {
    "apple": 3,
    "banana": 2,
    "tomato": 3,
    "orange": 5,
    "potato": 3,
    "cucumber": 2,
    "capsicum": 2,
    "okra": 0.5
}

def nonlinear_decay(initial, days, shelf):
    """
    Calculate non-linear decay of freshness
    Uses quadratic decay model for more realistic freshness degradation
    """
    if shelf <= 0:
        return 0
    
    fraction = days / shelf
    if fraction >= 1:
        return 0
    
    return round(initial * (1 - fraction**2), 2)

def compute_all_decay(initial, fruit, upload_date):
    """
    Compute freshness decay for all storage conditions
    """
    # Calculate days passed since upload
    if isinstance(upload_date, str):
        upload_date = date.fromisoformat(upload_date)
    
    days = (date.today() - upload_date).days
    
    # Handle unknown fruits - use average shelf life
    fruit = fruit.lower()
    if fruit not in IDEAL_SHELF:
        fruit = "apple"  # Default to apple if unknown
    
    # Calculate final freshness for each condition
    ideal_final = nonlinear_decay(initial, days, IDEAL_SHELF[fruit])
    room_final = nonlinear_decay(initial, days, ROOM_SHELF[fruit])
    humid_final = nonlinear_decay(initial, days, HIGH_HUMIDITY_SHELF[fruit])
    
    # Calculate estimated days left
    ideal_days_left = round((ideal_final / 100) * IDEAL_SHELF[fruit], 2) if ideal_final > 0 else 0
    room_days_left = round((room_final / 100) * ROOM_SHELF[fruit], 2) if room_final > 0 else 0
    humid_days_left = round((humid_final / 100) * HIGH_HUMIDITY_SHELF[fruit], 2) if humid_final > 0 else 0
    
    return {
        "days_passed": days,
        "ideal_final": ideal_final,
        "room_final": room_final,
        "humid_final": humid_final,
        "ideal_days_left": ideal_days_left,
        "room_days_left": room_days_left,
        "humid_days_left": humid_days_left
    }
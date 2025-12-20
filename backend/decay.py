from datetime import date
import math

# Ideal storage-based shelf-life (days)
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
    fraction = days / shelf
    if fraction >= 1:
        return 0
    return round(initial * (1 - fraction**2), 2)

def compute_all_decay(initial, fruit, upload_date):
    days = (date.today() - upload_date).days

    ideal_final = nonlinear_decay(initial, days, IDEAL_SHELF[fruit])
    room_final = nonlinear_decay(initial, days, ROOM_SHELF[fruit])
    humid_final = nonlinear_decay(initial, days, HIGH_HUMIDITY_SHELF[fruit])

    ideal_days_left = round((ideal_final / 100) * IDEAL_SHELF[fruit], 2)
    room_days_left = round((room_final / 100) * ROOM_SHELF[fruit], 2)
    humid_days_left = round((humid_final / 100) * HIGH_HUMIDITY_SHELF[fruit], 2)

    return {
        "days_passed": days,
        "ideal_final": ideal_final,
        "room_final": room_final,
        "humid_final": humid_final,
        "ideal_days_left": ideal_days_left,
        "room_days_left": room_days_left,
        "humid_days_left": humid_days_left
    }
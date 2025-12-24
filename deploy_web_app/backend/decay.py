from datetime import date

# --------------------------------
# Shelf-life configuration (days)
# --------------------------------
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

# --------------------------------
# Core decay logic
# --------------------------------
def nonlinear_decay(initial, days, shelf):
    """
    Quadratic freshness decay.
    Returns remaining freshness percentage.
    """
    if shelf <= 0:
        return 0

    if days < 0:
        days = 0

    fraction = days / shelf

    if fraction >= 1:
        return 0

    return round(initial * (1 - fraction ** 2), 2)

def compute_all_decay(initial, fruit, upload_date):
    """
    Compute freshness decay for all storage conditions.
    """
    fruit = fruit.lower()

    # Safety: fallback fruit
    if fruit not in IDEAL_SHELF:
        fruit = "apple"

    # Days since upload
    if not isinstance(upload_date, date):
        raise ValueError("upload_date must be a datetime.date instance")

    days_passed = max(0, (date.today() - upload_date).days)

    ideal_final = nonlinear_decay(initial, days_passed, IDEAL_SHELF[fruit])
    room_final = nonlinear_decay(initial, days_passed, ROOM_SHELF[fruit])
    humid_final = nonlinear_decay(initial, days_passed, HIGH_HUMIDITY_SHELF[fruit])

    ideal_days_left = round((ideal_final / 100) * IDEAL_SHELF[fruit], 2) if ideal_final > 0 else 0
    room_days_left = round((room_final / 100) * ROOM_SHELF[fruit], 2) if room_final > 0 else 0
    humid_days_left = round((humid_final / 100) * HIGH_HUMIDITY_SHELF[fruit], 2) if humid_final > 0 else 0

    return {
        "days_passed": days_passed,
        "ideal_final": ideal_final,
        "room_final": room_final,
        "humid_final": humid_final,
        "ideal_days_left": ideal_days_left,
        "room_days_left": room_days_left,
        "humid_days_left": humid_days_left
    }

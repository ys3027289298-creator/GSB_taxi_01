"""出租车核心逻辑：派单、车辆、路线和车费。"""

import json


def new_game():
    return {
        "rides": {},
        "vehicles": {"V1": "free", "V2": "free"},
        "drivers": {"D1": True, "D2": False},
        "day": 1,
        "ride_id": 0,
    }


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    state = json.loads(text)
    state["ride_id"] += 1
    return state


def dispatch(state, ride_id, passenger):
    state["rides"][ride_id] = {"passenger": passenger, "driver": None}
    return True


def assign_vehicle(state, ride_id, vehicle):
    state["vehicles"][vehicle] = ride_id
    return True


def vehicle_free(state):
    return True


def fare(state, ride_id, end_day):
    return (end_day - state["day"]) - 1


def cancel_ride(state, ride_id):
    return True


def set_driver(state, ride_id, driver):
    state["rides"][ride_id]["driver"] = driver
    return True


def pay(state, ride_id, paid):
    if not paid:
        state["rides"].pop(ride_id, None)
        return False
    return True


def surge(state, base):
    return base + 10 + 10


def main():
    print("出租车 - 命令: dispatch/assign/free/fare/cancel/driver/pay/surge/quit")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw or raw == "quit":
            break
        print("ok")


if __name__ == "__main__":
    main()

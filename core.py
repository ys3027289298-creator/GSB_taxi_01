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
    state = new_game()
    try:
        data = json.loads(text)
    except (TypeError, ValueError):
        return state
    if isinstance(data, dict):
        for key, value in data.items():
            state[key] = value
    return state


def _passenger_active(state, passenger):
    for ride in state["rides"].values():
        if isinstance(ride, dict) and ride.get("passenger") == passenger:
            return True
    return False


def dispatch(state, ride_id, passenger):
    if not passenger:
        return False
    existing = state["rides"].get(ride_id)
    if existing is not None:
        return isinstance(existing, dict) and existing.get("passenger") == passenger
    if _passenger_active(state, passenger):
        return False
    state["rides"][ride_id] = {"passenger": passenger, "driver": None}
    return True


def assign_vehicle(state, ride_id, vehicle):
    current = state["vehicles"].get(vehicle)
    if current is None:
        return False
    if current == ride_id:
        return True
    if current != "free":
        return False
    state["vehicles"][vehicle] = ride_id
    return True


def vehicle_free(state):
    return any(status == "free" for status in state["vehicles"].values())


def fare(state, ride_id, end_day):
    return max(0, end_day - state["day"])


def cancel_ride(state, ride_id):
    ride = state["rides"].get(ride_id)
    if not isinstance(ride, dict):
        return False
    ride["deposit"] = 0
    return True


def set_driver(state, ride_id, driver):
    if ride_id not in state["rides"]:
        return False
    if not state["drivers"].get(driver, False):
        return False
    state["rides"][ride_id]["driver"] = driver
    return True


def pay(state, ride_id, paid):
    ride = state["rides"].get(ride_id)
    if not isinstance(ride, dict):
        return False
    if not paid:
        return False
    ride["paid"] = True
    return True


def surge(state, base):
    return base + 10


_COMMANDS = {"dispatch", "assign", "free", "fare", "cancel", "driver", "pay", "surge", "quit"}


def main():
    print("出租车 - 命令: dispatch/assign/free/fare/cancel/driver/pay/surge/quit")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw:
            continue
        command = raw.split()[0]
        if command == "quit":
            break
        if command not in _COMMANDS:
            print("未知命令")
            continue
        print("ok")


if __name__ == "__main__":
    main()

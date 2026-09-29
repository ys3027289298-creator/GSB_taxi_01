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
    if not text or not text.strip():
        return new_game()
    state = json.loads(text)
    for key, value in new_game().items():
        state.setdefault(key, value)
    return state


def dispatch(state, ride_id, passenger):
    rides = state["rides"]
    existing = rides.get(ride_id)
    if existing is not None:
        return existing.get("passenger") == passenger
    for other in rides.values():
        if other.get("passenger") == passenger:
            return False
    rides[ride_id] = {"passenger": passenger, "driver": None, "deposit": 0}
    return True


def assign_vehicle(state, ride_id, vehicle):
    vehicles = state["vehicles"]
    if vehicle not in vehicles:
        return False
    current = vehicles[vehicle]
    if current == "free" or current == ride_id:
        vehicles[vehicle] = ride_id
        return True
    return False


def vehicle_free(state):
    return any(status == "free" for status in state["vehicles"].values())


def fare(state, ride_id, end_day):
    days = end_day - state["day"]
    return max(0, days)


def cancel_ride(state, ride_id):
    ride = state["rides"].get(ride_id)
    if ride is None:
        return False
    ride["deposit"] = 0
    for vehicle, holder in state["vehicles"].items():
        if holder == ride_id:
            state["vehicles"][vehicle] = "free"
    return True


def set_driver(state, ride_id, driver):
    ride = state["rides"].get(ride_id)
    if ride is None:
        return False
    if ride.get("driver") == driver:
        return True
    if not state["drivers"].get(driver, False):
        return False
    ride["driver"] = driver
    return True


def pay(state, ride_id, paid):
    if not paid:
        return False
    state["rides"].pop(ride_id, None)
    for vehicle, holder in state["vehicles"].items():
        if holder == ride_id:
            state["vehicles"][vehicle] = "free"
    return True


def surge(state, base):
    return base + 10


def _run_command(state, parts):
    cmd = parts[0]
    try:
        if cmd == "dispatch" and len(parts) == 3:
            return dispatch(state, int(parts[1]), parts[2])
        if cmd == "assign" and len(parts) == 3:
            return assign_vehicle(state, int(parts[1]), parts[2])
        if cmd == "free" and len(parts) == 1:
            print("free" if vehicle_free(state) else "full")
            return True
        if cmd == "fare" and len(parts) == 3:
            print(fare(state, int(parts[1]), int(parts[2])))
            return True
        if cmd == "cancel" and len(parts) == 2:
            return cancel_ride(state, int(parts[1]))
        if cmd == "driver" and len(parts) == 3:
            return set_driver(state, int(parts[1]), parts[2])
        if cmd == "pay" and len(parts) == 3:
            return pay(state, int(parts[1]), parts[2].lower() in ("yes", "true", "1"))
        if cmd == "surge" and len(parts) == 2:
            print(surge(state, int(parts[1])))
            return True
    except ValueError:
        return None
    return None


def main():
    state = new_game()
    print("出租车 - 命令: dispatch/assign/free/fare/cancel/driver/pay/surge/quit")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw or raw == "quit":
            break
        result = _run_command(state, raw.split())
        if result is None:
            print("非法命令")
        elif result:
            print("ok")
        else:
            print("fail")


if __name__ == "__main__":
    main()

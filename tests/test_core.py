import unittest

import core


class TestCore(unittest.TestCase):
    def test_01_no_duplicate_passenger(self):
        state = core.new_game()
        self.assertTrue(core.dispatch(state, 1, "P1"))
        self.assertFalse(core.dispatch(state, 2, "P1"))

    def test_02_vehicle_capacity(self):
        state = core.new_game()
        core.assign_vehicle(state, 1, "V1")
        core.assign_vehicle(state, 2, "V2")
        self.assertFalse(core.vehicle_free(state))

    def test_03_fare_exact(self):
        state = core.new_game()
        self.assertEqual(core.fare(state, 1, 4), 3)

    def test_04_cancel_refunds_deposit(self):
        state = core.new_game()
        state["rides"] = {1: {"deposit": 20}}
        core.cancel_ride(state, 1)
        self.assertEqual(state["rides"][1].get("deposit", 0), 0)

    def test_05_no_dispatch_to_offline_driver(self):
        state = core.new_game()
        core.dispatch(state, 1, "P1")
        result = core.set_driver(state, 1, "D2")
        self.assertFalse(result)

    def test_06_pay_failure_keeps_ride(self):
        state = core.new_game()
        core.dispatch(state, 1, "P1")
        result = core.pay(state, 1, False)
        self.assertFalse(result)
        self.assertIn(1, state["rides"])

    def test_07_surge_once(self):
        state = core.new_game()
        self.assertEqual(core.surge(state, 100), 110)

    def test_08_load_preserves_ride_id(self):
        state = core.new_game()
        state["ride_id"] = 5
        loaded = core.load_state(core.save_state(state))
        self.assertEqual(loaded["ride_id"], 5)


if __name__ == "__main__":
    unittest.main()

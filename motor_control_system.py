"""
Project:     Python Motor Control System
Author:      Romil Chauhan
Board:       LabJack UE9 (Ethernet)
Driver:      L293 H-Bridge Motor Driver
Description: Controls DC motor direction and state via a LabJack UE9
             connected over Ethernet. Supports forward, reverse, and
             emergency stop with reset-gated resume logic — motor only
             resumes after explicit user confirmation following a stop.
             Demonstrates hardware-software interfacing, FIO pin I/O
             control, and debounced hardware button detection in Python.

Usage:       Update the UE9 IP address on line 21 before running.
             Run: python motor_control_system.py
"""

import ue9
import time
import LabJackPython

# ── Pin Assignments (L293 H-Bridge) ──────────────────────────────
DIR_A_PIN = 1   # FIO1 → Direction A (through optocoupler OP1)
DIR_B_PIN = 2   # FIO2 → Direction B (through optocoupler OP2)
EN_PIN    = 0   # FIO0 → Enable     (through optocoupler OP3)
RESET_PIN = 3   # FIO3 → Reset button input


def connect_labjack():
    """Establish Ethernet connection to LabJack UE9."""
    return ue9.UE9(ethernet=True, firstFound=False, ipAddress="10.32.89.104")


def write_fio(d, fio, state):
    """Write digital state to a FIO pin."""
    d.singleIO(1, fio, Dir=1, State=state)


def read_fio(d, fio):
    """Read digital state from a FIO pin."""
    result = d.singleIO(0, fio)
    return result[f"FIO{fio} State"]


# ── L293 Active-Low Logic Helpers ────────────────────────────────
def l293_high(d, fio):
    """Drive FIO pin LOW (active-low logic → L293 input HIGH)."""
    write_fio(d, fio, 0)


def l293_low(d, fio):
    """Drive FIO pin HIGH (active-low logic → L293 input LOW)."""
    write_fio(d, fio, 1)


# ── Motor Control Functions ───────────────────────────────────────
def motor_stop(d):
    """Disable motor by pulling EN pin LOW."""
    l293_low(d, EN_PIN)


def motor_forward(d):
    """Run motor in forward direction."""
    l293_high(d, DIR_A_PIN)
    l293_low(d, DIR_B_PIN)
    l293_high(d, EN_PIN)


def motor_reverse(d):
    """Run motor in reverse direction."""
    l293_low(d, DIR_A_PIN)
    l293_high(d, DIR_B_PIN)
    l293_high(d, EN_PIN)


def safe_start(d):
    """Initialize all pins to safe state before motor operation."""
    motor_stop(d)
    l293_low(d, DIR_A_PIN)
    l293_low(d, DIR_B_PIN)


def wait_for_reset(d):
    """
    Block until hardware RESET button is pressed.
    Debounced — requires stable LOW signal for 50ms confirmation.
    """
    print("Waiting for RESET button press...")
    while True:
        if read_fio(d, RESET_PIN) == 0:
            time.sleep(0.05)                    # debounce delay
            if read_fio(d, RESET_PIN) == 0:
                return
        time.sleep(0.02)


def main():
    """Main control loop — accepts user commands via terminal."""
    d = connect_labjack()
    safe_start(d)

    print("=" * 50)
    print("  Motor Control System — Romil Chauhan")
    print("=" * 50)
    print("  FIO0 = ENABLE  (OP3)")
    print("  FIO1 = DIR_A   (OP1)")
    print("  FIO2 = DIR_B   (OP2)")
    print("  FIO3 = RESET button")
    print("-" * 50)
    print("  Commands: f=forward  r=reverse  s=stop  q=quit")
    print("=" * 50)

    last_direction = "forward"

    while True:
        cmd = input("\nEnter command: ").strip().lower()

        if cmd == "f":
            motor_forward(d)
            last_direction = "forward"
            print("Motor running FORWARD")

        elif cmd == "r":
            motor_reverse(d)
            last_direction = "reverse"
            print("Motor running REVERSE")

        elif cmd == "s":
            motor_stop(d)
            print("Motor STOPPED — press RESET button to resume")
            wait_for_reset(d)

            ans = input("RESET pressed. Resume motor? (y/n): ").strip().lower()
            if ans == "y":
                if last_direction == "forward":
                    motor_forward(d)
                    print("Motor resumed FORWARD")
                else:
                    motor_reverse(d)
                    print("Motor resumed REVERSE")
            else:
                print("Motor remains stopped")

        elif cmd == "q":
            motor_stop(d)
            print("Program ended — motor stopped safely")
            break

        else:
            print("Invalid command. Use: f / r / s / q")

    d.close()


if __name__ == "__main__":
    main()

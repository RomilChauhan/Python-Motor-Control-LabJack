# Python Motor Control System — LabJack UE9

> Python application controlling a DC motor via LabJack UE9 over Ethernet — forward/reverse direction, emergency stop, and reset-gated resume logic.

![Language](https://img.shields.io/badge/Language-Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Hardware](https://img.shields.io/badge/Hardware-LabJack_UE9-00D4FF?style=flat-square)
![Driver](https://img.shields.io/badge/Driver-L293_H--Bridge-00FF94?style=flat-square)
![Interface](https://img.shields.io/badge/Interface-Ethernet-FF6900?style=flat-square)
![Status](https://img.shields.io/badge/Status-Complete-00FF94?style=flat-square)

---

## Overview

This project implements a **hardware motor control system** in Python, communicating with a **LabJack UE9** data acquisition device over Ethernet to drive an **L293 H-bridge motor driver**. The system supports forward and reverse motor control, an emergency stop with hardware button detection, and a safety gate that prevents the motor from resuming until the user explicitly confirms after a reset button press.

---

## Hardware

| Component | Detail |
|-----------|--------|
| Controller | LabJack UE9 (Ethernet) |
| Motor Driver | L293 H-Bridge |
| Interface | Ethernet TCP/IP |
| Input | Hardware reset button (FIO3) |
| Output | DC Motor (bidirectional) |
| Logic | Active-low via optocouplers |

---

## Pin Mapping

| FIO Pin | Signal | Function |
|---------|--------|----------|
| FIO0 | ENABLE (OP3) | Motor enable — HIGH = running |
| FIO1 | DIR_A (OP1) | Direction control A |
| FIO2 | DIR_B (OP2) | Direction control B |
| FIO3 | RESET | Hardware reset button input |

**Motor direction truth table:**

| DIR_A | DIR_B | EN | Result |
|-------|-------|----|--------|
| HIGH | LOW | HIGH | Forward |
| LOW | HIGH | HIGH | Reverse |
| X | X | LOW | Stop |

---

## Features

- **Forward / Reverse** motor control via terminal commands
- **Emergency stop** — immediately disables motor enable pin
- **Reset-gated resume** — motor only restarts after hardware button press AND explicit user confirmation
- **Debounced reset detection** — 50ms hardware debounce on reset button
- **Safe initialization** — all pins set to safe state before operation begins
- **Clean shutdown** — motor stopped safely on quit

---

## Setup

### Requirements
```bash
pip install LabJackPython
```

### Configuration
Update the LabJack UE9 IP address in `motor_control_system.py`:
```python
return ue9.UE9(ethernet=True, firstFound=False, ipAddress="YOUR_UE9_IP")
```

### Run
```bash
python motor_control_system.py
```

---

## Commands

| Key | Action |
|-----|--------|
| `f` | Run motor forward |
| `r` | Run motor reverse |
| `s` | Emergency stop (requires reset button + confirmation to resume) |
| `q` | Quit and stop motor safely |

---

## System Flow

```
Start → safe_start() → wait for command
  f → motor_forward()
  r → motor_reverse()
  s → motor_stop() → wait_for_reset() → user confirm → resume / stay stopped
  q → motor_stop() → close connection → exit
```

---

## Author

**Romil Chauhan** — Computer Engineering Technology, Seneca Polytechnic
📧 chauhanromil1@gmail.com
🌐 [romilchauhan.github.io](https://romilchauhan.github.io)
💼 [linkedin.com/in/romilchauhan1111](https://linkedin.com/in/romilchauhan1111)

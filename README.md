This code requires a few things to work:
1) Raspberry Pi (if not Model 3 B+, GPIO connections may be different)
2) Pulolu DRV 8825 motor driver chip
3) NEMA 17 stepper motor (if using a different NEMA, degrees per step may differ -- see Motor_Control.py)
4) A debounce switch (button) for interrupting the code  if something goes wrong
5) a way of attaching the stepper motor shaft to the micrometer you wish to turn. We used 3D-printed PLA "fingers".

This code was written primarily by Adam Abate with interrupt service routine (ISR) assistance from Chipper Soulen.
This was part of a final project for "PHYS 351 - Scientific Instrumentation Lab" at the College of William & Mary in Fall 2018

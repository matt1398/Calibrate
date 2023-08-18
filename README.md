# Calibrate
Repo for calibrating bldc motor

For controlling the motor using tview:

command: `` python3 -m moteus_gui.tview ``

1. if you want torque control: 
``` d pos nan 0 nan p0 d0 f0.1```

I recommend that the value after f is lower than 0.35(0.35 will be super-fast).

3. if you want current control:
`` d dq 0 5``

Left value is Id, and right value is Iq. You should calculate proper amount of current to give certain torque.

5. if you want position control:
`` d pos nan 0.2 0.3 s0.8 ``, which is particularly:

`d pos <starting position> <velocity> <max torque> <ending position>`

7. if you want velocity control:
`` d pos nan 0.2 0.2 snan ``

same command as position control, but as you want certain velocity, you should set start/end pos to nan


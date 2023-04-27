Diffrent Modes
--------------
There are three ways(mods) to work with this project. These mods are: `Manual, Semi-Auto, Automatic`.<br>
- In `Manual` mode, the user controols everything - from the movemnt of the motor to the actuall shooting
- In `Semi-Auto` mode, the machine learning model will lead the motor and zoom enoght for a good detection but the user will give the athoriztion for the activation of the laser.
- In `Automaic` mode, the machine learning controlls everything, from moving and zooming up to the shooting. In this mode the user cannot control anything and in order for him to gain control back, he must change the mode to one of the other modes. 

Special Binds:
--------------
This project uses the `customtkinter` key binds in order to give orders to the main project. All the keyboard keys are being captured with the command: <br>
```py
import customtkinter as ctk

# [...]

main_window.window.bind("<KeyPress>", lambda event: handle_bind(main_window, event, l))
main_window.window.bind("<KeyRelease>", lambda event: handle_release())

# [...]
```
Later the `handle_bind` funtion filters the keys and proccess it forward.<br>
* `A` | `a` - these keys are used to move the motor counterclockwise.
* `D` | `d` - these keys are used to move the motor clockwise.
* `space`   - this keys is used to activate/deactivae the laser.
* `Q` | `q` - these keys are used to zoom out.
* `E` | `E` - there keys are used to zoom in.


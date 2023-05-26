AntiAir Balloon Detection AI
============================

About This Project
------------------
This project is a prototype of a system that can detect and shoot down incendiary balloons that are sent to harm people and destory property. In Israel the issue of incendiary balloons became a coomon thing. In order to combat the situation, the `IDF` created a complex system that relays on a lot of sensors and calculations, this project aims to make the same system but only to use less complex stuff in order to achive the same goal. This project relays on a simple machine learning model that knows how to detects ballons and with a basic mathemaic algorithem to get to the balloon and shoot it down. I believe that this project can be a gamechanger in the air-protection field. 

How does it work?
-----------------
Currently, Apr 27th 2023, The project has:
* DC Motor that moves horizontally 360 degrees
* Host computer(can be any computer or a raspberry pi 4) with a compatible camera
* 350mm Lazer module
* Raspberry Pi Pico micorprocessor
* HC-06 bluetooth module
* L293D chip<br>
Rectangular diagram: 
![תרשים מלבני](https://user-images.githubusercontent.com/67858186/234962568-d8af8023-f385-4ece-a5ec-46a85fda4275.png)
These components work in this order: 
1. The host's computer camera detects a balloon on the screen.
2. The distance in pixels between the middle point of the of the screen to the middle point of the bbox is being calulated. 
3. The distance is being compared to the constant ratio: the horizontal distance in meters from the camera to the middle of the ballom / the distance in pixels between the middle point of the of the screen to the middle point of the bbox. This gives how much the motor has to move to put the X point of the middle screen middle on the X point of the bbox.
4. The Lazer is being activated until the balloon 'pops'.<br>

Reflection
----------
This project is the product of my senior year of electronics major. I chose this project because of it's complexity, I enjoyed taking this project as something that I could learn from and experiance how it is to start something from zero with only the mentors the the internet to help me. 

Upcoming Updates
----------------
* (Application) A dot that will represent the laser location on the screen.
* (Application) Adding the `TensorFlow` Model to the Camera in order to detect Balloons. [DONE]
* (Application) Update for the `Automatic` and `semo-auto` modes that will make them work with the machine learning model.

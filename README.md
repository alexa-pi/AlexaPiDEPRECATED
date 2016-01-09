# AlexaCHIP
 
---
 
### Contributors
 
* Sam Machin
 
---
 
This is the code needed to Turn a Raspberry Pi into a client for Amazon's Alexa service, I have developed this against the Pi 2 but I see no reason it shouldn't run on the other models. Feedback welcome.
---
 
### Requirements

You will need:
A Raspberry Pi
An SD Card with a fresh install of Raspbian (tested against build 2015-11-21 Jessie)
An External Speaker with 3.5mm Jack
A USB Sound Dongle and Microphone
A push to make button connected between GPIO 18 and GND
(Optionally) A Dual colour LED (or 2 signle LEDs) Connected to GPIO 24 & 25


Next you need to obtain a set of credentials from Amazon to use the Alexa Voice service, login at http://developer.amazon.com and Goto Alexa then Alexa Voice Service
You need to create a new product type as a Device, for the ID use something like AlexaCHIP, create a new security profile and under the web settings allowed origins put http://localhost:5000 and as a return URL put http://localhost:5000/code you can also create URLs replacing localhost with the IP of your Pi  eg http://192.168.1.123:5000
Make a note of these credentials you will be asked for them during the install process

### Installation

Boot your fresh Pi and login to a command prompt as root.

Make sure you are in /root

Clone this repo to the Pi

Run the setup script
./setup.sh

Follow instructions....


Enjoy :)

### Issues/Bugs etc.

If your alexa isn't running on startup you can check /var/log/alexa.log for errrors.

If the error is complaining about alsaaudio you may need to check the name of your soundcard input device



---
 


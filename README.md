# AlexaCHIP
 
---
 
### Contributors
 
* Sam Machin
 
---
 
This is the code needed to Turn a CHIP into a client for Amazon's Alexa service, it should be farly easy to port it over to the Raspberry Pi or other similar boards that can run python and have audio and network interfaces. I'd welcome any pull requests for doing so.
---
 
### Setup
 
First obtain a CHIP from http://getchip.com at time of writing (Jan 2016) orders wern't shipping till June 2016 Sorry!

Assuming you have a CHIP and its connected to your wifi network you then to do the hardware mod to enable mic input on the 3.5mm jack http://docs.getchip.com/#microphone-and-audio-input You could also just use the header pins on the board to access speaker and mic depending on your project.

You'll also want to connect a small normally open push button across GPIO1 and GND (pins 14 an 1 on U14)

Copy the contents of the repo into a new folder on the CHIP and then run the following

apt-get update
apt-get install  libasound2-dev memcahed python-pip
pip install -r requirements.txt

Next you need to obtain a set of credentials from Amazon to use the Alexa Voice service, login at http://developer.amazon.com and Goto Alexa then Alexa Voice Service

You need to create a new product type as a Device, for the ID use something like AlexaCHIP, create a new security profile and under the web settings allowed origins put http://localhost:5000 and as a return URL put http://localhost:5000/code you can also create URLs replacing localhost with the IP of your CHIP/Pi etc eg http://192.168.1.123:5000

Once you've got the security credentials put them into the creds.py file on your device.

Now you can run the signup web server to create a login token, run
python ./auth_web.py

Now if you setup localhost then you need to open a browser on your CHIP and goto http://localhost:5000 or if you added your IP as well then you can connect from your PC using that URL. This is a simple web app which will take you through authorising your developer credentials to access your alexa account as a user and finally it will return a refresh token that you then need to add to the creds.py file on your CHIP. 
Sorry this is a bit of a faff but you should only need to do it once for as many CHIP's as you want to use.

Finally you need to tell the CHIP to activate the GPIO pin, run the setup_gpio.sh script from the terminal, you need to do this after each reboot as well.

Now that you've got the refresh token on you CHIP you're all set, just run main.py from the console and after a few secs it should print Ready, now you can press the button say a command and await the response.

Enjoy :)

You'll probbly want to put the setup_gpio and main.py scripts into crontab or something to auto run them at boot up.



---
 
### Improvements
 
* Improve the setup guide.
* Improve the experience of setting up the token.
* Add LED's to indicate status
* Port to RasPi

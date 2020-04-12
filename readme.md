# TitanHacks 2020

## Project Name
Webcam Music (scroll all the way to bottom for installation instructions)

## Github Link
https://github.com/lchsiteam/theremin

## Here's the elevator pitch
What's your idea? This will be a short tagline for the project
An instrument that you can play with your webcam anytime from anywhere.

## It's built with
Python, OpenCV, Tkinter, Numpy, Scipy, Sounddevice, threading

## About Us
Team: Clawdawgs-19

## School and Club
LCHS iTeam of La Cañada High School - https://github.com/lchsiteam

## Team members devpost, github, and discord
Bryan Wang - https://devpost.com/the-non-feline - https://github.com/the-non-feline - not a cat#9738\n
Ryan King - https://devpost.com/RyantheKing - https://github.com/RyantheKing - RyantheKing#9710\n
Devyn Oh - https://devpost.com/thepnkprkr - https://github.com/MC-Atom - MC_Atom#1733\n
Kai Bredemann - https://devpost.com/awesomehaze - https://github.com/awesomehaze - haze#2948\n
Ean Jeffries - https://devpost.com/epicean - https://github.com/epicodaboss - Epico (Ean)#2393\n


# Here's the whole story

## Inspiration
We were inspired by music. Half of our group is in choir, and half of our group makes original music for fun. Making music is very fun and rewarding, but it’s very hard for beginners to figure out some of the more complicated aspects. This project makes it easier for those beginners to have some fun creating music, even if it’s not super practical.

## What it does
This project is conceptually very simple. The application watches your webcam, and with the help of OpenCV, it recognizes where your hands are. This is fed into a simple function that converts the x and y positions of your hands into parameters. These parameters control a wave function, which outputs to the speakers of the computer. At the end of a recording, it will also save the audio to a .wav file. 

## How we built it
We split into two teams, one two work on hand tracking, and one to work on converting hand location into audio signals.  We used OpenCV to analyze webcam feed in real time, and used a picture of the background without the hands in frame and a the live feed to subtract out (mostly) everything that wasn’t the hands, so that we could then get the contours for the hands. We then used numpy and the built-in math module to crunch the numbers required to produce the desired sounds, and sounddevice was used to produce the sounds. Numpy and SciPy were used to write the audio to a .wav file. 

## Challenges we ran into
At first it was difficult to recognize the hands with a noisy background, and we relied on a black background and for the user to wear dark clothes. However we were able to overcome this by removing a photo of the background from the image in the live feed. We also ran into many problems with the audio quality, which were eventually solved by lowering the sample rate. 

## Accomplishments that we’re proud of
Tracking 2 hands at once and tracking hands with a noisy and bright background.

## What we learned
How to better and more efficiently work on programs in teams, as well as learning aspects of OpenCV, tkinter, sounddevice, and SciPy python libraries.

## What's next for Webcam Music
We plan to improve and eventually publish our creation so that others can have fun with the tool we enjoy.  We will likely code the system to recognize hand gestures, and perform more musical features such as holding a note or a staccato.


##


# How to install project
Install opencv: pip install opencv-python

Add Cascadia Code font: [Github](https://github.com/microsoft/cascadia-code/releases/download/v1911.21/CascadiaPL.ttf)

project information: https://docs.google.com/document/d/1BpdIwYHkR49n2461MQNBnICoQtzkQPQGrQGLbpesn-E/edit?usp=sharing

to install dependences, use `pip install --upgrade -r requirements.txt` 

# VirtualMouse_openCV
in this prj we have a mouse that we can control it by just moving our fingers and there are some gesture that you can use them to click 

# Libraries

import cv2 as cv

import numpy as np

import autopy

import mediapipe as mp

import math

>you have to install  ( opencv-python , numpy , pip , autopy , mediapip , math )
>
>my python version was 3.8 


# Test Video
if you use your Index Finger you can adjust and move the mouse

if you want to click all you have to do is raising your middle finger and putting it next to your Index

![](https://github.com/mohammadst99/VirtualMouse_openCV/blob/main/test.gif)


# Explian code 
 we have writen hand Tracking module before and you have to read it before since we used this module in this prj 
 
 first we have to import some libraries that we need in this code
 
 then we have import our VideoCamera using cv2 libraries 
 
 then we have detect the hand if there is a hand or not 
 
 in the next step we need to get the position of INDEX and MIDDLE FINGER as x,y to use them to control our mouse 
 
 following this step we have to detect which finger is up ( INDEX or MIDDLE and INDEX) 
 
 if Index is up so we have to write a program as moving mode
  > so we need to detect the position of our finger and make an area that we have to move our finger in 
  > 
  > then we need to turn our finger position to our Screen size 
 
 and if Index and Middle finger is up we have to CLICK 

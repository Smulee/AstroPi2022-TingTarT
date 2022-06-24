# 

# What this program does? 
# This program first takes a photo with low resolution then-
# check if this photo is dark or not then-
# if the photo isnt dark, program takes one photo more this time with
# higher resolution and stores it and write information like latitude and current time to csv file 

import cv2
import numpy as np
from pathlib import Path
import csv
from datetime import datetime
from picamera import PiCamera
from orbit import ISS
from time import sleep
import os

base_folder = Path(__file__).parent.resolve()      # path to folder for this script
data_file = base_folder / 'data.csv'    # ya, same. If we want we can change name of this file

camera = PiCamera()
camera.resolution = (100, 100)

lower_bound = np.array([0, 0, 0])       # those arrays helps to find darkenes of photos
upper_bound = np.array([350, 55, 100])  
day = True      # bool that says if its day or not
nameNumber = 1  # helps to name photos

hourStart = datetime.now().hour     # Variabel that stores hour of beginning of program
minuteStart = datetime.now().minute # Variabel that stores minute of beginning of program

size = 0 # variabel to store size of photos


def check_photo():  # This checks if photo is dark 
    image = cv2.imread(f'{base_folder}/testImage.jpg') # reads low resolution photo 
    image_mask = cv2.inRange(image, lower_bound, upper_bound)  # mask for finding darkness of picture
    if cv2.countNonZero(image_mask) == 10000:  # cheking if a photo is dark
        print("found")  # doesnt need to be in code
        return False    # means that its night
    return True     # means that its day


sleep(2) # just to be sure that everyting is working
with open(data_file, 'w', buffering=1) as f:    # i just found it in phase 2 guild, it creates data file for logger
    writer = csv.writer(f)  # this is a logger
    while True:
        try:
            location = ISS.coordinates() 
        except:
            row = (datetime.now(), "failed to find the location of ISS")  # writing information to row 
            writer.writerow(row) # write row to csv file
            location = "location error"
        try:
            if datetime.now().hour - 3 == hourStart  and datetime.now().minute +2 == minuteStart: # Checking if 2 hours and 58 minutes past
                break 
        except:
            row = (datetime.now(), "failed to check current time", location)  # writing information to row 
            writer.writerow(row) # write row to csv file
        try: 
            if size > 2900000000: # checks if photos takes more then 2.9GB of space
                break
        except: 
            row = (datetime.now(), "failed to check size of files", location)  # writing information to row 
            writer.writerow(row) # write row to csv file
        
        try:
            camera.capture(f'{base_folder}/testImage.jpg')
        except: 
            row = (datetime.now(), "failed to take a photo", location)  # writing information to row 
            writer.writerow(row) # write row to csv file
        try: 
            day = check_photo()  # day is a bool
        except: 
            row = (datetime.now(), "failed to check the darkness of an image",location)  # writing information to row 
            writer.writerow(row) # write row to csv file
            day = True
        try:
            if day:     # if its a day then...
                camera.resolution = (3280, 2464) # resolution of store photos
                camera.capture(f'{base_folder}/Image' + nameNumber.__str__() + ".jpg") #store photos and add name to it, all have diffrent number in name 
                camera.resolution = (100, 100)  # resolution for checking darkness 
                print("nice")
                row = (datetime.now(), nameNumber, "day", location)  # write information to row
                writer.writerow(row)    # write a row to csv file

                size = os.path.getsize(f'{base_folder}/Image' + nameNumber.__str__() + ".jpg") + size # adds size of photos to variabel size
                print('Size of file is', size, 'bytes')

            else:
                row = (datetime.now(), nameNumber, "night", location)  # writing information to row 
                writer.writerow(row)  # write row to csv file
        except:
            row = (datetime.now(), "something failed while storing photo",location)  # writing information to row 
            writer.writerow(row) # write row to csv file
        nameNumber += 1  # number of photo, helps to find photo that corresponds to csv file
        sleep(15)  # delay between taken photos. Should be between 15 and 20 sec
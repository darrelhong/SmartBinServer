from gpiozero import Button, LED, PWMLED
from picamera import PiCamera
from time import sleep
import argparse

from lobe import ImageModel

#Create input, output, and camera objects
button = Button(2)

blue_led = LED(17) #recyclable
green_led = LED(27) #general
white_led = PWMLED(24) #Status light and retake photo

camera = PiCamera()

parser = argparse.ArgumentParser(description='Waste classifier')
parser.add_argument('--model', help='Path to model folder', type=str, default='model')
args = parser.parse_args()

# Load Lobe TF model
model = ImageModel.load(args.model)

# Take Photo
def take_photo():
    # Quickly blink status light
    white_led.blink(0.1,0.1)
    sleep(2)
    print("Pressed")
    white_led.on()
    # Start the camera preview
    camera.start_preview(fullscreen=False,window=(50,0,900,1200))
    # wait 2s or more for light adjustment
    sleep(3) 
    # Optional image rotation for camera
    # --> Change or comment out as needed
    # camera.rotation = 270
    #Input image file path here
    # --> Change image path as needed
    camera.capture('/home/pi/Desktop/image.jpg')
    #Stop camera
    camera.stop_preview()
    white_led.off()
    sleep(1)

# Identify prediction and turn on appropriate LED
def led_select(label):
    print(label)
    if label == "general":
        print("general trash")
        green_led.on()
        sleep(5)
    if label == "recyclable":
        print("recyclable")
        blue_led.on()
        sleep(5)
    if label == "noitem":
        print("No item detected!")
        sleep(5)
    else:
        print("None")
        blue_led.off()
        green_led.off()
        white_led.off()

# Main Function
while True:
    if button.is_pressed:
        take_photo()
        # Run photo through Lobe TF model
        print("predicting")
        result = model.predict_from_file('/home/pi/Desktop/image.jpg')
        
        # Print all classes
        for label, confidence in result.labels:
            print(f"{label}: {confidence*100}%")

        led_select(result.prediction)
    else:
        # Pulse status light
        white_led.pulse(2,1)
    sleep(1)
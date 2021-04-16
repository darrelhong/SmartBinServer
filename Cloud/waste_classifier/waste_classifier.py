from time import sleep
from gpiozero import LED, PWMLED
from picamera import PiCamera

from lobe import ImageModel

blue_led = LED(17)  # recyclable
green_led = LED(27)  # general
white_led = PWMLED(24)  # Status light and retake photo

camera = PiCamera()

class WasteClassifier:
    def __init__(self, modelPath) -> None:
        pass
        self.model = ImageModel.load(modelPath)
    def led_select(label):
        print(label)
        if label == "general":
            print("General trash detected")
            green_led.on()
            sleep(5)
        if label == "recyclable":
            print("Recyclable item detected")
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
    def classify(self) -> None:
        # take picture
        # Quickly blink status light
        white_led.blink(0.1, 0.1)
        sleep(2)
        white_led.on()
        # Start the camera preview
        camera.start_preview(fullscreen=False, window=(50, 0, 900, 1200))
        # wait 2s or more for light adjustment
        sleep(3)
        # Optional image rotation for camera
        # --> Change or comment out as needed
        # camera.rotation = 270
        # Input image file path here
        # --> Change image path as needed
        camera.capture("/home/pi/Desktop/image.jpg")
        # Stop camera
        camera.stop_preview()
        white_led.off()
        sleep(1)

        # predict
        result = self.model.predict_from_file("/home/pi/Desktop/image.jpg")

        # Print all classes
        for label, confidence in result.labels:
            print(f"{label}: {confidence*100}%")

        self.led_select(result.prediction)

import RPi.GPIO as GPIO


class FlameSensor:

    def __init__(self, pin, callback) -> None:
        self.pin = pin
        GPIO.setup(pin, GPIO.IN)
        GPIO.add_event_detect(pin, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
        GPIO.add_event_callback(pin, callback)
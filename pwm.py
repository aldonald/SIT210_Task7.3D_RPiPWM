import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24
BUZZ = 17
LED= 18

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(BUZZ, GPIO.OUT)
GPIO.setup(LED, GPIO.OUT)

buzzer = GPIO.PWM(BUZZ, 100)
led = GPIO.PWM(LED, 100)

buzzer.start(0)
led.start(0)

counter = 0 
try:
    while True:
        counter += 1
        GPIO.output(TRIG, False)
        time.sleep(1)  # To allow clean signal on trigger
        
        GPIO.output(TRIG, True)
        time.sleep(0.00001)  # minimum for sensor to trigger.
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()

        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        # speed of sound = 34300 cm/s but travels to object and back, so 17150.
        distance = round(pulse_duration * 17150, 2)  
        buzzer_level = 100 - distance/2 if distance < 100 else 0
        led_level = 100 - distance/2 if distance < 100 else 0

        buzzer.ChangeDutyCycle(int(buzzer_level))
        led.ChangeDutyCycle(int(led_level))

        if (counter % 20 == 0):
            print(f"Distance: {distance}cm")

except KeyboardInterrupt:
    print("\nInterupted")
    GPIO.cleanup()

import RPi.GPIO as GPIO
import time
import pyglet

GPIO.setmode(GPIO.BCM)

TRIG = 4
ECHO = 3
PIR = 2

print "Distance Measurement In Progress"

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(PIR,GPIO.IN)

GPIO.output(TRIG, False)
print "Waiting For Sensor To Settle"

sound2 = pyglet.media.load('sound2.mp3', streaming=False)
sound2.play()


while True:

    print(GPIO.input(PIR))
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
        pulse_start = time.time()

    while GPIO.input(ECHO)==1:
        pulse_end = time.time()

    
    pulse_duration = pulse_end - pulse_start
    
    distance = pulse_duration * 17150
    
    distance = round(distance, 2)
    
    print "Distance:",distance,"cm"
    
    time.sleep(2)

GPIO.cleanup()

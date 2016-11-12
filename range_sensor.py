import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

TRIG = 4
ECHO = 3
PIR = 2

print "Distance Measurement In Progress"

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(PIR,GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(TRIG, False)
print "Waiting For Sensor To Settle"

GPIO.wait_for_edge(PIR, GPIO.RISING, callback=detected_people)

detected = False

while True:

    if detected :
        read_distance()
        print "Detected OK"
        detected = False

    time.sleep(2)
    

GPIO.cleanup()

def detected_people(PIR):
    detected = True


def read_distance():
    
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

    return distance


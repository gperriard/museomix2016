import RPi.GPIO as GPIO
import time
import sys
import subprocess

GPIO.setmode(GPIO.BCM)

TRIG = 4
ECHO = 3
PIR = 2

step_1_process = None
step_2_process = None

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(PIR, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(TRIG, False)


def read_distance():
    """
    Read the distance between the visitor and the captor.
    Due to the captor can detect something at 1.5 meter max.
    """

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    pulse_start = 0
    pulse_end = 0

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance


def player(file):
    return subprocess.Popen(['aplay', file])


def step_1(PIR):
    global step_1_process
    global step_2_process

    # Run sound1 only if sound1 or sound2 is not already playing
    if (step_2_process is None or (step_2_process is not None and step_2_process.poll() == 0)) and (step_1_process is None or step_1_process.poll() == 0):
        step_1_process = player('sound1.wav')


GPIO.add_event_detect(PIR, GPIO.RISING, callback=step_1)

while True:
    if read_distance() < 500:
        if step_1_process is not None and step_1_process.poll() is None:
            step_1_process.kill()
            step_1_process = None

        # Run step 2 only if it hasn't running yet (or just finished)
        if step_2_process is None or step_2_process.poll() == 0:
            step_2_process = player('sound2.wav')

GPIO.cleanup()


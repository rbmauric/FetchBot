# EGCP 470: FetchBot
# Ryan Mauricio
# 12/5/20
# Servo Controller

# Initialization
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
servo = GPIO.PWM(11, 50)
duty = 7
right = True


# Initialization
def ServoInit():
    servo.start(0)
    time.sleep(2)


# Rotation Function
def SetAngle(angle):
    duty = int((angle / 18) + 2)
    servo.ChangeDutyCycle(duty)
    time.sleep(0.1)
    servo.ChangeDutyCycle(0)
    time.sleep(0.1)


# Sweep Function
def SweepRight():
    global duty
    if duty <= 12:
        duty = duty + 1
        servo.ChangeDutyCycle(duty)
        time.sleep(0.1)
        servo.ChangeDutyCycle(0)
        time.sleep(0.1)


def SweepLeft():
    global duty
    if duty >= 2:
        duty = duty - 1
        servo.ChangeDutyCycle(duty)
        time.sleep(0.1)
        servo.ChangeDutyCycle(0)
        time.sleep(0.)


def Sweep():
    global right
    global duty

    if duty >= 12:
        right = False
    else:
        right = True

    if right == True:
        SweepRight()
    else:
        SweepLeft()


# Cleanup
def CleanUp():
    servo.ChangeDutyCycle(7)
    time.sleep(1)
    servo.stop()
    GPIO.cleanup()
    # exit()

# Testing
# while(1):
#    print("Sweeping. Duty =", duty)
#    Sweep()
#      ang = int(input("Angle:\n"))
#      print("Rotating", ang, "degrees\n")
#      SetAngle(ang)
#
#      fin = str(input("Finished? y/n\n"))
#      if fin in ['y', 'Y']:
#          CleanUp()
#

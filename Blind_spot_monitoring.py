import GPIO #GPIO of any micro-controller
import time
import _thread
from threading import Thread

#set up the GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#Pin
TRIG = 1
ECHO = 2
TRIGR = 3
ECHOR = 4
RIGHTLED = 5
LEFTLED = 6
FAULTLED=7

#pinconfiguration
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(TRIGR, GPIO.OUT)
GPIO.setup(ECHOR, GPIO.IN)
GPIO.setup(RIGHTLED, GPIO.OUT)
GPIO.setup(LEFTLED, GPIO.OUT)
GPIO.setup(FAULTLED, GPIO.OUT)


def checksystem_off():
    while True:
        bsm_state,engine_state=vehiclestatus()
        if(bsm_state==True and engine_state == True): #check if bsm is on and engine is on 
            standbythread= Thread(target= standby_t)
            standbythread.start()
            



def standby():
    while True:
        speed,gear=speed_gear()
        bsm_state,engine_state=vehiclestatus()
        if(speed>=20 and speed<=130 and (gear!='P' and gear != 'R') and bsm_state == True):
            avaiablethread= Thread(target= available_t)
            avaiablethread.start()
            _thread.exit()
        elif(bsm_state == False):
            checksystem_off()
            
            

def in_blindspot_left(): 
    GPIO.output(LEFTLED, GPIO.HIGH)
    time.sleep (0.5)
    GPIO.output(LEFTLED, GPIO.LOW)
        
def in_blindspot_right(): 
    GPIO.output(RIGHTLED, GPIO.HIGH)
    time.sleep (0.5)
    GPIO.output(RIGHTLED, GPIO.LOW)



def blink_left():
    while True:
        threat = False
        time.sleep(0.4)
        obj,rspeed=check_left()
        if(rspeed>0 and rspeed<48 and obj==True): #relative speed should be between 0 and 48
            threatl(True)
        
def blink_right():
    while True:
        threat = False
        time.sleep(0.4)
        obj,rspeed=check_right()
        if(rspeed>0 and rspeed<48 and obj==True):
            threatr(True)
        



def available():
    while True:
        threat=threat_status()
        bsm_state,engine_state=vehiclestatus()
        speed,gear=speed_gear()
        if(threat== False and bsm_state== True):
            try:
                _thread.start_new_thread( blink_left, ())
                _thread.start_new_thread( blink_right, ())
            except:
                fault()
        if(threat == True and bsm_state== False):
            alert=Thread(target = alert_t)
            alert.start()
            _thread.exit()
        if(speed<20 or (gear=='P' or  gear == 'R') and bsm_state == True):
            standby()
        elif(bsm_state == False):
            checksystem_off()
        
def alert():
    while True:
        threat=threat_status()
        bsm_state,engine_state=vehiclestatus()
        speed,gear=speed_gear()
        if(threatl == True and bsm_state== True):
            try:
                _thread.start_new_thread(in_blindspot_left, ())
            except:
                fault()
        if(threatr == True and bsm_state== True):
            try:
                _thread.start_new_thread(in_blindspot_right, ())
            except:
                fault()
        if(threat == False and bsm_state== True):
            available()
            
        if(speed<20 or (gear=='P' or  gear == 'R') and bsm_state == True):
            standby()
        elif(bsm_state == False):
            checksystem_off()
        



def standby_t():
    try:
        _thread.start_new_thread( standby , ())
       
    except:
        fault()

def available_t():
    try:
        _thread.start_new_thread( available , ())
       
    except:
       fault()

def alert_t():
    try:
        _thread.start_new_thread( alert , ())
       
    except:
        fault()


def fault():
    while True:
        bsm_state,engine_state=vehiclestatus()
        if(bsm_state==False or engine_state==False):
            checksystem_off()
        GPIO.output(FAULTLED, GPIO.HIGH)
        time.sleep (0.5)
        GPIO.output(FAULTLED, GPIO.LOW)
        
   
def main():
    try:
        _thread.start_new_thread( checksystem_off ,())
    except:
        fault()

if __name__ == "__main__":
    main()
       







def vehiclestatus():
    i= True
    j= True
    return i,j

def speed_gear():
    speed=25
    gear=1
    return speed,gear

def threatl(x):
    return x
def threatr(x):
    return x

def threat_status():
    status=threatl() or threatr()
    return status

def check_left():
    return True,20

def check_right():
    return True,20

import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt
import numpy as np
#from matplotlib.animation import FuncAnimation

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# doing this first, since we're using a while True.
#GPIO.cleanup()
#declaring pins for motor
plt.style.use('fivethirtyeight')
#plt.style.use('ggplot')

#Declaring counters for appending logic

c=0
d=0
g=0

# Declaring Empty arrays
#for plotting

a=[]
b=[]


plt.ion()
fig = plt.figure()
plt.title('Real time plotting')
plt.xlabel('left tyre')
plt.ylabel('Right tyre')
ax = fig.add_subplot(1,1,1)
plt.axis([-20,35,-20,35])


#secondcontrol_pins = [12,16,20,21]
secondcontrol_pins = [21,20,16,12]
control_pins = [6,13,19,26]
for pin in control_pins:
		GPIO.setup(pin, GPIO.OUT)
		GPIO.output(pin, 0)
		halfstep_seq = [
  [1,0,0,0],
  [1,1,0,0],
  [0,1,0,0],
  [0,1,1,0],
  [0,0,1,0],
  [0,0,1,1],
  [0,0,0,1],
  [1,0,0,1]
]


for pin in secondcontrol_pins:
		GPIO.setup(pin, GPIO.OUT)
		GPIO.output(pin, 0)
		halfstep_seq = [
  [1,0,0,0],
  [1,1,0,0],
  [0,1,0,0], 
  [0,1,1,0],
  [0,0,1,0],
  [0,0,1,1],
  [0,0,0,1],
  [1,0,0,1]
]


		
# declaring pins for distance sensor
TRIG = 4
ECHO = 18


GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

#function for distance acquisition
def get_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    
    while GPIO.input(ECHO) == False:
     start = time.time()
    while GPIO.input(ECHO) == True:
     end = time.time()
 
    sig_time = end - start

 #CM:
    distance = sig_time / 0.000058

    #inches:
    #distance = sig_time / 0.000148
    #print('Distance: {} centimeters'.format(distance))
    return distance

def mov():
 if d == 0 and c == 0 and (g%2==0) and g<1:
  count1=0
  count2=0
 elif c > 0:
  count1=a[-1]
  count2=b[-1]  
 elif c==0 and d==0 and (g%2!=0): 
  count1=a[-1]
  count2=b[-1]
 elif c==0 and d==0 and (g%2==0) and g>=1: 
  count1=a[-1]
  count2=b[-1]
 distance = get_distance()
  #plt.show()	
 while distance > 45:
   distance = get_distance()
   if d==0 and c==0 and (g%2==0):
    count1 = count1 + 1
    a.append(count1)
    #count2 = count2 + 1
    b.append(count2)
   elif c==0 and d==0 and (g%2!=0):
    #count1=count1-0.50
    a.append(count1)
    count2=count2-0.75
    b.append(count2)
   elif c == 1 and d == 1 and (g%2==0):
    count1=count1-0.5
    a.append(count1)
    count2 = count2 -1
    b.append(count2)
   elif c == 1 and d ==1 and (g%2!=0):
    count1=count1-0.40
    a.append(count1)
    count2 = count2 -0.75
    b.append(count2) 
   elif c == 2 and d ==2 and (g%2==0):
    count1=count1-0.10
    a.append(count1)
    count2=count2+1
    b.append(count2)
   elif c == 2 and d ==2 and (g%2!=0):
    count1=count1-0.60
    a.append(count1)
    count2=count2+0.55
    b.append(count2)
   elif c==3 and d ==3 and (g%2==0):
    count1=count1+0.95
    a.append(count1)
    #count2 = count2 + 1
    b.append(count2)
   elif c==3 and d ==3 and (g%2!=0):
    count1=count1+0.20
    a.append(count1)
    count2 = count2 + 0.70
    b.append(count2)
   
   
  
   print("left array ", a)	
   print(" Right array ", b)
   
   line1, = ax.plot(a, b, '-r')
   line1.set_data(a,b)
   fig.canvas.draw()
   fig.canvas.flush_events()
   for i in range(512):
    for halfstep in range(8):
     for pin in range(4):
       GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
       GPIO.output(secondcontrol_pins[pin], halfstep_seq[halfstep][pin])
     time.sleep(0.001)


def right():
 if c == 0 and d == 0 and (g%2==0):
  co=0
  co2=0
 elif d > 0:
  co=a[-1]
  co2=b[-1]
 elif c==0 and d==0 and (g%2!=0):
  co=a[-1]
  co2=b[-1]
 distance = get_distance()	
 while distance < 45:	 
   distance = get_distance()
   if c==0 and d == 1 and (g%2==0):
    co=co-0.4
    a.append(co)
    co2=co2-1
    b.append(co2)
    print("right array", a)
    print("left array ", b)
    line1, = ax.plot(a, b,'-r')
    line1.set_data(a,b)
    fig.canvas.draw()
    fig.canvas.flush_events()
    for i in range(512):
      for halfstep in range(8):
       for pin in range(4):
        GPIO.output(secondcontrol_pins[pin], halfstep_seq[halfstep][pin])
       time.sleep(0.001)
   elif c==0 and d == 1 and (g%2!=0):
    co=co-0.40
    a.append(co)
    co2=co2-0.75
    b.append(co2)
    print("right array", a)
    print("left array ", b)
    line1, = ax.plot(a, b,'-r')
    line1.set_data(a,b)
    fig.canvas.draw()
    fig.canvas.flush_events()
    for i in range(160):
     for halfstep in range(8):
      for pin in range(4):
       GPIO.output(secondcontrol_pins[pin], halfstep_seq[halfstep][pin])
      time.sleep(0.001)
   elif c == 1 and d == 2 and (g%2==0):
    co=co-0.10
    a.append(co)
    co2=co2+1
    b.append(co2)
    print("right array", a)
    print("left array ", b)
    line1, = ax.plot(a, b,'-r')
    line1.set_data(a,b)
    fig.canvas.draw()
    fig.canvas.flush_events()
    for i in range(705):
     for halfstep in range(8):
      for pin in range(4):
       GPIO.output(secondcontrol_pins[pin], halfstep_seq[halfstep][pin])
      time.sleep(0.001)
   elif c == 1 and d == 2 and (g%2!=0):
    co = co-0.60
    a.append(co)
    co2=co2+0.55
    b.append(co2)
    print("right array", a)
    print("left array ", b)
    line1, = ax.plot(a, b,'-r')
    line1.set_data(a,b)
    fig.canvas.draw()
    fig.canvas.flush_events()
    for i in range(410):
     for halfstep in range(8):
      for pin in range(4):
       GPIO.output(secondcontrol_pins[pin], halfstep_seq[halfstep][pin])
      time.sleep(0.001)
   elif c == 2 and d ==3 and (g%2==0):
    co=co+0.95
    a.append(co)
    #co2=co2+1
    b.append(co2)
    print("right array", a)
    print("left array ", b)
    line1, = ax.plot(a, b,'-r')
    line1.set_data(a,b)
    fig.canvas.draw()
    fig.canvas.flush_events()
    for i in range(474):
     for halfstep in range(8):
      for pin in range(4):
       GPIO.output(secondcontrol_pins[pin], halfstep_seq[halfstep][pin])
       #GPIO.output(secondcontrol_pins[pin], halfstep_seq[halfstep][pin])
      time.sleep(0.001)
   elif c == 2 and d ==3 and (g%2!=0):
    co=co+0.20
    a.append(co)
    co2=co2+0.70
    b.append(co2)
    print("right array", a)
    print("left array ", b)
    line1, = ax.plot(a, b,'-r')
    line1.set_data(a,b)
    fig.canvas.draw()
    fig.canvas.flush_events()
    for i in range(384):
     for halfstep in range(8):
      for pin in range(4):
       GPIO.output(secondcontrol_pins[pin], halfstep_seq[halfstep][pin])
      time.sleep(0.001)
   elif c == 3 and d == 4 and (g%2==0):
    #co=co-0.50
    a.append(co)
    co2=co2-0.75
    b.append(co2)
    print("right array", a)
    print("left array ", b)
    line1, = ax.plot(a, b,'-r')
    line1.set_data(a,b)
    fig.canvas.draw()
    fig.canvas.flush_events()
    for i in range(415):
      for halfstep in range(8):
       for pin in range(4):
        GPIO.output(secondcontrol_pins[pin], halfstep_seq[halfstep][pin])
       time.sleep(0.001) 
   elif c ==3 and d== 4 and (g%2!=0):
    co=co+1
    a.append(co)
    #co2=co2+0.78
    b.append(co2)
    print("right array", a)
    print("left array ", b)
    line1, = ax.plot(a, b,'-r')
    line1.set_data(a,b)
    fig.canvas.draw()
    fig.canvas.flush_events()
    for i in range(200):
      for halfstep in range(8):
       for pin in range(4):
        GPIO.output(secondcontrol_pins[pin], halfstep_seq[halfstep][pin])
       time.sleep(0.001) 
   
     

def stop():
 GPIO.setup(pin, GPIO.LOW)
 GPIO.setup([6,13,19,26], GPIO.LOW) 
 '''line3, = ax.plot(a, b, '-r', marker = '*')
 line3.set_data(a,b)
 fig.canvas.draw()
 fig.canvas.flush_events()'''

def new():
  global c 
  c= 0
  global d
  d=0
  global g
  g=g+1
  del a[:-12]
  del b[:-12]
  print ("hogi")
  print(c)
  print(d)
  #print(a)
  return(c,d)
   

while True:
    distance = get_distance()
    time.sleep(0.005)
    print("checking")
    print(distance)
    
    if c == 4:
        new()
    elif distance < 45:
        stop()
        time.sleep(1)
        print("obstacle")
        #line1, = ax.plot(a, b, marker = '*')
        right()
        c=c+1
    elif distance > 45:
        print("clear")
        mov()
        d=d+1
    '''if d == 4:
        c == 0
        d == 0
        a[i]=0
        b[i]=0'''
GPIO.cleanup()



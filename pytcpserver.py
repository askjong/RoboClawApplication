import socket
import re
import sys
import time
from threading import Thread
from roboclaw import Roboclaw

##################################################
#Declaring functions 
##################################################

def connect_to_server():
    sock.connect(server_address)
    Thread(target=handle_server, args=(sock,)).start()


# Handle information sendt from server
def handle_server(server):
    print 'Connected'

    while True:

        data = server.recv(4096) #4096
        try:

            #print("from connected user: " + data)

            array = data.lower().split(",")
            for i in array:
                #print(str(i))

                if str(i) == "getencoderdata":
                        encoderposition()
                        payloadUnencoded = "enc1:" + str(enc1Payload[0])+':' + "enc2:" + str(enc2Payload[0])
                        #print payloadUnencoded
                        payload =  str(payloadUnencoded) + '\n'.encode('UTF-8')
                        server.send(payload)


                if str(i) == 'getmotorspeed':
                    #print 'Motorspeed'
                    getMotorSpeed()
                    payload  = str(speed1Payload) + '\n'.encode('UTF-8')
                    server.send(payload)

                if "setspeedmotorone" in str(i):
                    #print 'Setting Motor speed'
                    matches = re.findall('-?\d+', i)
                    m1 = int(matches[0])
                    if m1> 0 :setM1ForwardSpeed(m1)
                    if m1 <= 0: setM1BackwardSpeed(abs(m1))
                    # payloadUnformated = "Motor 1f speed set"
                    # payload  = str(payloadUnformated) + '\n'.encode('UTF-8')
                    # server.send(payload)

                if "setspeedmotortwo" in str(i):
                    #print 'Setting Motor speed'
                    matches = re.findall('-?\d+', i)
                    m2 = int(matches[0])
                    if m2>0 :setM2ForwardSpeed(m2)
                    if m2<= 0: setM2BackwardSpeed(abs(m2))
                    # payloadUnformated = "Motor 2f speed set"
                    # payload  = str(payloadUnformated) + '\n'.encode('UTF-8')
                    # server.send(payload)

                if "stop" in str(i):
                    print 'Stop 2'
                    Stop()

        except Exception as e:
            print 'Exception in Server Thread. Stopping vehicle'
            print e
            Stop()
            server.close()



def getMotorSpeed():
    speed1 = rc.ReadSpeedM1(address)
    speed2 = rc.ReadSpeedM2(address)
    global speed1PayloadPrev
    global speed2PayloadPrev
    if(speed1[0]):
        global speed1Payload
        speed1Payload = speed1[1]
        speed1PayloadPrev = speed1Payload
    else:
        print 'Reading Speed failed. Previous value for speed returned.'
        speed1Payload = speed1PayloadPrev
    if(speed2[0]):
        global speed2Payload
        speed2Payload = speed2[1]
        speed2PayloadPrev = speed2Payload
    else:
        print 'Reading Speed failed. Previous value for speed returned.'
        speed2Payload = speed2PayloadPrev


def setM1ForwardSpeed(M1):
    rc.ForwardM1(address,M1)

def setM2ForwardSpeed(M2):
    rc.ForwardM2(address,M2)

def setM1BackwardSpeed(M1):
    rc.BackwardM1(address,M1)

def setM2BackwardSpeed(M2):
    rc.BackwardM2(address,M2)

def Stop():
    rc.BackwardM2(address,0)
    rc.BackwardM1(address,0)
    rc.ForwardM2(address,0)
    rc.ForwardM1(address,0)

def encoderposition():
    enc1 = rc.ReadEncM1(address)
    enc2 = rc.ReadEncM2(address)
    global enc1PayloadPrev
    global enc2PayloadPrev
    if(enc1[0]==1):
        global enc1Payload
        enc1Payload = enc1[1],
        enc2PayloadPrev = enc1Payload
    else:
        print 'Reading encoder 1 failed. Returning previous value'
        enc1Payload = enc2PayloadPrev,
    if(enc2[0]==1):
        global enc2Payload
        enc2Payload = enc2[1],
        enc2PayloadPrev = enc1Payload
    else:
        print 'Reading encoder 2 failed. Returning previous value'
        enc2Payload = enc2PayloadPrev




##################################################
#Initialzing server
##################################################


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('127.0.0.1', 8000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
# sock.connect(server_address)

#Initialize Roboclaw Library
rc = Roboclaw("/dev/ttyACM0",115200)
rc.Open()
address = 0x80
version = rc.ReadVersion(address)
enc1Payload = None;	
m1 = 0;
m2 = 0;
if version[0]==False:
    print "GETVERSION Failed"
else:
    print repr(version[1])

##################################################
#Running server
##################################################

if __name__ == "__main__":
    try:
        print 'Waiting for a connection'
        connect_to_server()
    except Exception as e:
        print 'Exception in main.'
        print e







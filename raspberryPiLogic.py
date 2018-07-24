import serial
arduinoSerialData = serial.Serial('/dev/ttyACM0', 9600)
while 1:
    if(arduinoSerialData.inWaiting()>0):
        myData = arduinoSerialData.readline()
        #if myData.find(b'btn1') != -1:
         #   arduinoSerialData.write('13'.encode())
          #  print('Lighting 13')
        #else:
        print(myData)

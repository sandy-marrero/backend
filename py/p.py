import serial

serial = serial.Serial("COM3", 9600, timeout=1)

while True:
    x = str(serial.readline().strip())[2:-1]
    if x:
        # x = x.split(",")
        num = x[0]
        speed = x[1]
        altitude = x[2]
        print(x)
        print()

#!/usr/bin/python3
import os
import sys
import time
import serial #python3.7 -m pip install pyserial
from ymodem import YModem


def readLine(serial_io, blocking):
    if blocking:
        print("[CNQ Board]: " + serial_io.readline().decode("ascii"), end='')

    while serial_io.inWaiting() > 0:
        print("[CNQ Board]: " + serial_io.readline().decode("ascii"), end='')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3.7 usartUpload.py flashfile.bin [serialDevice] [baudrate] [password]")
        exit(1)

    binaryFile = sys.argv[1]
    serialDevice = "/dev/ttyS1"
    bdRate = 500000 # CANIQUE devices run USART @ 500 kbps
    password = ""

    doReset = True

    if len(sys.argv) > 2:
        serialDevice = sys.argv[2]

    if len(sys.argv) > 3:
        bdRate = int(sys.argv[3])

    if len(sys.argv) > 4:
        password = sys.argv[4] #must not be longer than 16 chars


    print("Using serial device {} @ speed {} bps".format(serialDevice, bdRate))


    try:
        serial_io = serial.Serial()
        serial_io.port = serialDevice
        serial_io.baudrate = bdRate
        serial_io.timeout = 0.1

        #serial_io.parity = "N"
        #serial_io.bytesize = 8
        #serial_io.stopbits = 1
        #serial_io.timeout = 2

        print(serial_io)
        serial_io.open()

        #reset procedure
        if doReset:
            print("Resetting Canique board via reset pin...")
            serial_io.dtr = True #pull down

            time.sleep(0.1)
            serial_io.dtr = False #pull up again
    except Exception:
        print("Could not open serial port on {}".format(serialDevice))
        exit(1)

    def sender_getc(size):
        return serial_io.read(size) or None

    def sender_putc(data, timeout=15):
        return serial_io.write(data)

    print("Connected.\n")

    #read multiple lines: wait for press key prompt
    #readLine(serial_io, True)

    print("Waiting for msg from bootloader...")

    while True:
        if serial_io.inWaiting() > 0:
            line = serial_io.readline().decode("ascii")
            print("[CNQ Board]: " + line, end='')
            if "Press" in line:
                break

    readLine(serial_io, False)

    sender = YModem.YModem(sender_getc, sender_putc, data_pad=b'\xFF')
    os.chdir(sys.path[0])

    print("Sending command 'd' for firmware upload to Canique device...")
    serial_io.write('d'.encode()) # start download - specific command to CANIQUE devices

    #print("[CNQ Board]: " + serial_io.readline().decode("ascii"))
    # wait for password prompt / or "Transferring"
    prompt = serial_io.readline().decode("ascii")
    print("[CNQ Board]: " + prompt)

    if "Enter PW" in prompt:
        readLine(serial_io, False)
        print("Sending pw...")
        pwEnc = password.encode()

        print("[CNQ Board]: ", end="")

        for i in range(len(pwEnc)):
            serial_io.write(pwEnc[i:(i+1)])
            serial_io.flush()
            c = serial_io.read(1).decode("ascii")
            print(c, end="")

        serial_io.write("\n".encode())
        serial_io.flush()
        c = serial_io.read(1).decode("ascii")
        print(c, end="")
        #serial_io.flush()
        #pwEcho = serial_io.readline().decode("ascii") #read echo from password
        #print("[CNQ Board]: " + pwEcho)
        #while True:
    #        if serial_io.inWaiting() > 0:
    #            c = serial_io.read(1).decode("ascii")
#                print("[CNQ Board]: " + c)

        serial_io.timeout = 2.0 #pw check takes its time
        while True:
            if serial_io.inWaiting() > 5:
                line = serial_io.readline().decode("ascii")
                print("[CNQ Board]: " + line, end="")
                if "Transferring" in line:
                    break
                elif "Wrong" in line:
                    exit(1)
        serial_io.timeout = 0.5

    readLine(serial_io, False)


    file_path = os.path.abspath(binaryFile)
    sent = sender.send_file(file_path)

    if sent >= 0:
        print("Sent {} bytes".format(sent))

    readLine(serial_io, False)

    if sent == os.path.getsize(file_path):
        print("Sending command 'r' to run firmware...")
        serial_io.write('r'.encode()) # run firmware - specific command to CANIQUE devices

        serial_io.timeout = 9.5
        readLine(serial_io, True)

    serial_io.close()

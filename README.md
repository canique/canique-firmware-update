# canique-firmware-update
Code to update firmware on canique sensor devices

# Installation
```
git clone https://github.com/canique/canique-firmware-update.git
cd canique-firmware-update
python3 -m venv cnq-fw-update-venv
source cnq-fw-update-venv/bin/activate
pip install pyserial
deactivate
```

# Usage
Follow the instructions to establish an USART connection in the device manual. Usually this includes: removing the battery, connecting wires to VCC (3.3V), GND, RX, TX pins, and using a USB to serial converter to connect the wires to a computer USB port.  
Download the encrypted firmware image from the official canique website.  
Request the bootloader password from Canique.  

Then run:  

`cnq-fw-update-venv/bin/python3 usartUpload.py encrypted-flash-file.bin /dev/ttyUSB0 500000 bootloader-password`  
Replace `encrypted-flash-file.bin` by the name of your encrypted firmware binary.  
Replace `/dev/ttyUSB0` by your serial port.  
Replace `bootloader-password` by the bootloader password of the specific device (this is different for every single device)  

**Important: After running the FW Update, do not immediately cut off power. The device will reboot and decrypt the firmware image and store it in its internal memory. This can take around 20 seconds.**

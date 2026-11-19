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
`cnq-fw-update-venv/bin/python3 usartUpload.py encrypted-flash-file.bin /dev/ttyUSB0 500000 bootloader-password`
Replace `encrypted-flash-file.bin` by the name of your encrypted firmware binary.  
Replace `/dev/ttyUSB0` by your serial port.  
Replace `bootloader-password` by the bootloader password of the specific device (this is different for every single device)  

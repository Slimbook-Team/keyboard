# keyboard
... under construction


**Install RGB**

Dependencies:

standard compile stuff (c compiler, make, etc)

linux-headers

Open a terminal and:

git clone https://github.com/slimbook/keyboard.git

cd keyboard/backlight/essential/rgb-module/module/

sudo apt install gcc make build-essential

make && sudo make install

sudo insmod clevo-xsm-wmi.ko

sudo install -m644 clevo-xsm-wmi.ko /lib/modules/$(uname -r)/extra

sudo depmod

sudo tee /etc/modules-load.d/clevo-xsm-wmi.conf <<< clevo-xsm-wmi

sudo update-initramfs -uk all

sudo tee /etc/modprobe.d/clevo-xsm-wmi.conf <<< 'options clevo-xsm-wmi kb_color=white,white,white, kb_brightness=10'

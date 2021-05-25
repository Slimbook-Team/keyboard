# keyboard
... under construction


**Install Slimbook RGB Keyboard on Ubuntu (debian distros)**


      sudo add-apt-repository ppa:slimbook/slimbook

      sudo apt-get install slimbookrgbkeyboard


**Install Slimbook RGB Keyboard on other Linux distros**
(no GUI Interface)

Dependencies:

- standard compile stuff (c compiler, make, etc)
- linux-headers 

      · Ubuntu: sudo apt install git linux-headers-$(uname -r)

      · Fedora: yum -y install git kernel-devel kernel-headers
      

      Open a terminal and:

      wget https://raw.githubusercontent.com/slimbook/keyboard/main/install_rgb.sh

      sudo bash ./install_rgb.sh

      reboot

Thanks

More information of GUI here:
https://slimbook.es/en/tutoriales/aplicaciones-slimbook/501-en-slimbook-rgb-keyboard-3-0

**Information:**
We have a private repo for Slimbook RGB Keyboard because we find that the software is not mature enough yet. If you want to help with development you can ask for access at dev@slimbook.es

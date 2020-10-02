#include <stdio.h>

void main (){
    FILE* f = fopen("/sys/devices/platform/clevo_xsm_wmi/kb_brightness", "w");
    if (f == NULL) {
        fprintf(stderr, "Unable to open path for writing\n");
        return 1;
    }

    fprintf(f, "1\n");
    fclose(f);
    return 0;
}

echo 1 > /sys/devices/platform/clevo_xsm_wmi/kb_brightness


sudo chmod -R 777 /sys/devices/platform/clevo_xsm_wmi/kb_brightness
echo 1 > /sys/devices/platform/clevo_xsm_wmi/kb_brightness
sudo chmod -R 777 /sys/devices/platform/clevo_xsm_wmi/kb_color
echo "green green green" > /sys/devices/platform/clevo_xsm_wmi/kb_color



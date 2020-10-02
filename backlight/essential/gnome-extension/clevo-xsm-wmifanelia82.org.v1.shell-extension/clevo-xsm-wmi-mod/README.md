# clevo-xsm-wmi

Kernel module for keyboard backlighting of Clevo SM series notebooks.
(And several EM/ZM/DM series models)

Based upon tuxedo-wmi, created by TUXEDO Computers GmbH.
http://www.linux-onlineshop.de/forum/index.php?page=Thread&threadID=26

### Additions over tuxedo-wmi
* Non root Sysfs interface to control the brightness, mode, colour,
  on/off state after the module has loaded.
  In the original code you can only set these before the module loads.
* Small Gnome Extension application to visually control the keyboard lighting using the sysfs interface.
* Eliminated the part that control the fan


### Supported Devices

| Produkt Name         | Clevo Name             | TUXEDO Name            |
|----------------------|------------------------|------------------------|
| P15SM                | Clevo P15SM            | ???                    |
| P15SM1-A             | Clevo P15SM1-A         | ???                    |
| P15SM-A              | Clevo P15SM-A          | ???                    |
| P150EM               | Clevo P150EM           | TUXEDO XC1501          |
| P15xEMx              | Clevo P150EM           | TUXEDO XC1503          |
| P17SM-A              | Clevo P17SM-A          | ???                    |
| P17SM                | Clevo P17SM            | ???                    |
| P370SM-A             | Clevo P370SM-A         | ???                    |
| P65_67RSRP           | Clevo P65_67RSRP       | ???                    |
| P65xRP               | Clevo P65xRP           | TUXEDO XC1507          |
| P65xHP               | Clevo P65xHP           | TUXEDO XC1507v2        |
| Deimos/Phobos 1x15S  | Clevo P7xxDM(-G)       | TUXEDO XUX506 / XUX706 |
| P7xxDM(-G)           | Clevo P7xxDM(-G)       | TUXEDO XUX506 / XUX706 |
| P7xxDM2(-G)          | Clevo P7xxDM2(-G)      | TUXEDO XUX507 / XUX707 |
| P750ZM               | Clevo P750ZM           | ???                    |
| P5 Pro SE            | Clevo P750ZM           | ???                    |
| P5 Pro               | Clevo P750ZM           | ???                    |
| P775DM3(-G)          | Clevo P775DM3(-G)      | TUXEDO XUX707          |
| N85_N87              | Clevo N850HJ           | TUXEDO DX1507 / DX1707 |
| P870DM               | Clevo P870DM           | ???                    |
| N85_N87,HJ,HJ1,HK1   | Clevo N870HK           | ???                    |
| P95_HP,HR,HQ         | Clevo P950HP6          | ???                    |
| P65_67HSHP           | Clevo P65_67HSHP       | ???                    |

### Building

Dependencies:

* standard compile stuff (c compiler, make, etc)
* linux-headers

Building:
```bash
# For the module
$ cd module && make && sudo make install

# For the shell extension
See instruction under clevoxsmwmi@fanelia82.org/README.md
```

### License
This program is free software;  you can redistribute it and/or modify
it under the terms of the  GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or (at
your option) any later version.

This program is  distributed in the hope that it  will be useful, but
WITHOUT  ANY   WARRANTY;  without   even  the  implied   warranty  of
MERCHANTABILITY  or FITNESS FOR  A PARTICULAR  PURPOSE.  See  the GNU
General Public License for more details.

You should  have received  a copy of  the GNU General  Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

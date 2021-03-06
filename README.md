# Open-Gardener

A Modular End-to-End vegan/free-range/bio/fair-trade... Gardening solution from
scratch.

<img width=80% src=/images/dashboard.png ></img>

## List of Parts:

* [Raspberry Pi](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/)
* [Chinese Motor HAT](https://www.aliexpress.com/item/NEW-Stepper-Motor-B-Robot-Expansion-Board-Servo-HAT-for-Raspberry-Pi-3-PI-2-Mini/32857529077.html?spm=2114.search0204.3.36.272279d0nXKoS3&ws_ab_test=searchweb0_0,searchweb201602_1_10320_10152_10151_10065_10321_10344_10068_10342_10547_10343_10322_10340_10548_10341_10696_10084_10083_10618_10304_10307_10820_10821_10302_10843_10059_100031_10319_10103_10624_10623_10622_10621_10620-10152,searchweb201603_6,ppcSwitch_4_ppcChannel&algo_expid=79dfc765-b29e-4e5f-9ddc-ca0a054ac1de-5&algo_pvid=79dfc765-b29e-4e5f-9ddc-ca0a054ac1de&priceBeautifyAB=0) (Aliexpress
  link)
* [Arduino clone](https://www.aliexpress.com/item/Nano-CH340-ATmega328P-MicroUSB-Compatible-for-Arduino-Nano-V3-0/32740641316.html?spm=2114.search0204.3.1.32f52b20tGXJRD&s=p&ws_ab_test=searchweb0_0,searchweb201602_1_10320_10152_10151_10065_10321_10344_10068_10342_10547_10343_10322_10340_10548_10341_10696_10084_10083_10618_10304_10307_10820_10821_10302_10843_10059_100031_10319_10103_10624_10623_10622_10621_10620,searchweb201603_6,ppcSwitch_4_ppcChannel&priceBeautifyAB=0) (Aliexpress
  link)
* [Humidity Sensor](https://www.aliexpress.com/item/Nano-CH340-ATmega328P-MicroUSB-Compatible-for-Arduino-Nano-V3-0/32740641316.html?spm=2114.search0204.3.1.32f52b20tGXJRD&s=p&ws_ab_test=searchweb0_0,searchweb201602_1_10320_10152_10151_10065_10321_10344_10068_10342_10547_10343_10322_10340_10548_10341_10696_10084_10083_10618_10304_10307_10820_10821_10302_10843_10059_100031_10319_10103_10624_10623_10622_10621_10620,searchweb201603_6,ppcSwitch_4_ppcChannel&priceBeautifyAB=0) (Hygrometer)
  Aliexpress link
* [12v Water Pump](https://www.amazon.de/TSSS-Wasserpumpe-Submersible-Gartenteich-Unterhaltung/dp/B01I9BN3CI/ref=sr_1_3?ie=UTF8&qid=1533215283&sr=8-3&keywords=12v+water+pump) (Amazon.de link)

## Custom Parts:

* Water Multiplexer: 3D Printed.

<img width=80% src=/images/water-splitter-v2.png ></img>


## Software

* SQLite: Using WAL mode for storing moisture values
* Python: For everything else
* Arduino: Code for reading moisture values and other sensor.

## Installation

TBD

## DEMOs

### Water-Multiplexer in Action:

[![Alt text](https://img.youtube.com/vi/m-ae1GWE0tQ/0.jpg)](https://www.youtube.com/watch?v=m-ae1GWE0tQ)

## TODOs

### Missing Features
- [ ] Other Sensors
- [ ] Configuration Mapping between plants/sensors/hoses
- [ ] CRUD for sensors/hoses

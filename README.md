# [WIP] Open-Gardener

A Modular End-to-End free-range/bio/free-trade... Gardening solution from scratch.

<img width=100% src=/images/dashboard.png ></img>

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

<img width=100% src=/images/water-multiplexer.png ></img>


## Software

* SQLite: Using WAL mode for storing moisture values
* Python: For everything else
* Arduino: Code for reading moisture values and other sensor.

## Installation

TBD

## DEMOs

### Water-Multiplexer in Action:

<blockquote class="instagram-media" data-instgrm-captioned data-instgrm-permalink="https://www.instagram.com/p/Bf59qRFH2Rw/?utm_source=ig_embed" data-instgrm-version="9" style=" background:#FFF; border:0; border-radius:3px; box-shadow:0 0 1px 0 rgba(0,0,0,0.5),0 1px 10px 0 rgba(0,0,0,0.15); margin: 1px; max-width:540px; min-width:326px; padding:0; width:99.375%; width:-webkit-calc(100% - 2px); width:calc(100% - 2px);"><div style="padding:8px;"> <div style=" background:#F8F8F8; line-height:0; margin-top:40px; padding:50.0% 0; text-align:center; width:100%;"> <div style=" background:url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACwAAAAsCAMAAAApWqozAAAABGdBTUEAALGPC/xhBQAAAAFzUkdCAK7OHOkAAAAMUExURczMzPf399fX1+bm5mzY9AMAAADiSURBVDjLvZXbEsMgCES5/P8/t9FuRVCRmU73JWlzosgSIIZURCjo/ad+EQJJB4Hv8BFt+IDpQoCx1wjOSBFhh2XssxEIYn3ulI/6MNReE07UIWJEv8UEOWDS88LY97kqyTliJKKtuYBbruAyVh5wOHiXmpi5we58Ek028czwyuQdLKPG1Bkb4NnM+VeAnfHqn1k4+GPT6uGQcvu2h2OVuIf/gWUFyy8OWEpdyZSa3aVCqpVoVvzZZ2VTnn2wU8qzVjDDetO90GSy9mVLqtgYSy231MxrY6I2gGqjrTY0L8fxCxfCBbhWrsYYAAAAAElFTkSuQmCC); display:block; height:44px; margin:0 auto -44px; position:relative; top:-22px; width:44px;"></div></div> <p style=" margin:8px 0 0 0; padding:0 4px;"> <a href="https://www.instagram.com/p/Bf59qRFH2Rw/?utm_source=ig_embed" style=" color:#000; font-family:Arial,sans-serif; font-size:14px; font-style:normal; font-weight:normal; line-height:17px; text-decoration:none; word-wrap:break-word;" target="_blank">Test run for the irrigation system. My plants shall not die!</a></p> <p style=" color:#c9c8cd; font-family:Arial,sans-serif; font-size:14px; line-height:17px; margin-bottom:0; margin-top:8px; overflow:hidden; padding:8px 0 7px; text-align:center; text-overflow:ellipsis; white-space:nowrap;">A post shared by <a href="https://www.instagram.com/diegoeche/?utm_source=ig_embed" style=" color:#c9c8cd; font-family:Arial,sans-serif; font-size:14px; font-style:normal; font-weight:normal; line-height:17px;" target="_blank"> Diego</a> (@diegoeche) on <time style=" font-family:Arial,sans-serif; font-size:14px; line-height:17px;" datetime="2018-03-04T15:05:38+00:00">Mar 4, 2018 at 7:05am PST</time></p></div></blockquote>


## TODOs

TBD

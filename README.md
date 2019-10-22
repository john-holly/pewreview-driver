# pewreview-driver

This is a driver for the [Dream Cheeky USB Missile Launcher](https://www.alibaba.com/product-detail/Dream-Cheeky-8A1C2B-USB-Missile-Launcher_119093330.html).
I'm not going to lie, I just really want to shoot my boss when I open a pull request. If he becomes too quick I'm giving this puppy vision.

## Requirements

* Python 3
* PIP
* [Dream Cheeky USB Missile Launcher](https://www.alibaba.com/product-detail/Dream-Cheeky-8A1C2B-USB-Missile-Launcher_119093330.html)

![Dream Cheeky USB Missile Launcher](https://sc02.alicdn.com/kf/HTB1BuKvKVXXXXcwXVXXq6xXFXXXg/Dream-Cheeky-8A1C2B-USB-Missile-Launcher.jpg)

## Setup

Install the requirements via `pip`.

```bash
pip install -r requirements.txt
```

## Running

### Driver Demo

```bash
python launcher.py
```

### Server

TODO - create udev rules to run without root privileges.

```bash
sudo python server.py --port 31337
```

### Client

```bash
python client.py --port 31337 LEFT,2 RIGHT,3 FIRE FIRE FIRE
```


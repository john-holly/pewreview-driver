# pewreview-driver

This is a driver for the [Dream Cheeky USB Missile Launcher](https://www.alibaba.com/product-detail/Dream-Cheeky-8A1C2B-USB-Missile-Launcher_119093330.html).
I just really want to shoot my boss when I open a pull request. If he becomes too quick I'm giving this puppy vision.

## Requirements

* OS supporting `hidapi`
* Python 3
* PIP
* [Dream Cheeky USB Missile Launcher](https://www.alibaba.com/product-detail/Dream-Cheeky-8A1C2B-USB-Missile-Launcher_119093330.html)

![Dream Cheeky USB Missile Launcher](https://sc02.alicdn.com/kf/HTB1BuKvKVXXXXcwXVXXq6xXFXXXg/Dream-Cheeky-8A1C2B-USB-Missile-Launcher.jpg)

## Setup

Install the requirements via `pip`.

```bash
pip install -r requirements.txt
```

## Usage

### Driver Demo

This would only be to show off what the launcher can do. This is the core driver that has a main function to demo.

```bash
python launcher.py
```

### Server

```bash
sudo python server.py --port 31337
```

### Client

Each token of a command line is formatted as follows `<command> [,<sleep in nanoseconds/number of missiles>]`. The number is optional for `FIRE` and `RESET`

#### Commands

* `FIRE [,<number of missiles]`
* `UP`, `DOWN`, `LEFT`, `RIGHT`
* `RESET` - Reset hardware state (stop whatever command is running)

```bash
python client.py --port 31337 CMD[,<sleep in nanoseconds/number of missiles>]
```

## All Together

1. Plug in launcher and ensure the computer sees it. 
2. Start your server `python server.py --port 31337`.
3. Send a command stream to the launcher via client `python client.py --port 31337 UP,2000 LEFT,1000 FIRE,3`.
4. Assert geek dominance and profit.

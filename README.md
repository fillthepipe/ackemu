# ackemu
Ackemu is a UDP-based tool that sends large segments as data packets and returns small segments as ACK packets.

## Configure & Run
Experimental enviroment here is two server with both wireless and physical network cards and one router.
To run the test here:
1.Set configurations in config.py
2.```python ackemu.py```

You can custom your experiments as follow:
|--ackemu.py: Run ACK emulation experiments,you can mode test schedule here
|--config.py: Set experiments configuration based on your enviroment
|--utils.py: Add some utils


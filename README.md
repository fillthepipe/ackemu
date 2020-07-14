# ackemu
Ackemu is a UDP-based tool that sends large segments as data packets and returns small segments as ACK packets.

## Configure & Run
Experimental enviroment here is two server with both wireless and physical network cards and one router.

Before you run the test please configure config.py

After that, run ```python ackemu.py```

You can customize your experiments as follow:

+-- ackemu.py: Run ACK emulation experiments,you can mode test schedule here    
+-- config.py: Set experiments configuration based on your enviroment           
+-- utils.py: Add some utils


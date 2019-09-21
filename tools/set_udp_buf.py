import os
import argparse



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--size',type=int,default=1472)    #--size KB
    args = parser.parse_args()
    print args.size
    buf_size = args.size*1024
    os.system("sudo sysctl -w net.ipv4.udp_mem=\"%d %d %d\""%(98304,buf_size,buf_size))
    os.system("sudo sysctl -w net.core.rmem_default=%d"%(buf_size))
    os.system("sudo sysctl -w net.core.wmem_default=%d"%(buf_size))
    os.system("sudo sysctl -w net.core.rmem_max=%d"%(buf_size))
    os.system("sudo sysctl -w net.core.wmem_max=%d"%(buf_size))
    os.system("sudo sysctl -w net.ipv4.udp_rmem_min=%d"%(buf_size))
    os.system("sudo sysctl -w net.ipv4.udp_wmem_min=%d"%(buf_size))


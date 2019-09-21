import os
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--a', type=str, default='tcpbbr')  # --a algorithm
    algorithm = parser.parse_args()

    print 'Congestion Algorithm available:'
    os.system('cat /proc/sys/net/ipv4/tcp_available_congestion_control')

    os.system('sudo sysctl -w net.ipv4.tcp_congestion_control=%s'%(algorithm))
    print 'Setted Congestion Algorithm:'
    os.system('cat /proc/sys/net/ipv4/tcp_congestion_control')

    # ./ demo - s - p - g 1 - T - Q - t | tee xx
    # ./ demo - c - p - g 1 - T - Q - t
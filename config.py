"""
If the environment is not pure,
we can select the channel with less interference

AP setting(up to network confition):
11b/11g/11n,20/40HZ,h1-13
selected:40HZ,h5
11ac,20/40/80HZ auto,h36,40...
selected:80HZ,h40

We can Config the experiments as follow:
"""
#two server set the same
username = "test2"
passwd = "test12#$"

#data packet size and ack packet size
#data UDP pkt:1472,ACK UDP pkt:52
pkt_size = 1472
ack_size = 52

#IP config
"""
sudo ifconfig eth0 xxx/23 up
sudo ifconfig eth0:1 xxx/23 up

To prevent the link interference(eg:ssh),
we use two ips make the experements keep in a pure link
"""
#data & ack send link
sender_data_ip = "192.168.3.101"
receiver_data_ip = "192.168.3.102"
#ssh link
sender_ssh_ip = "192.168.3.104"
receiver_ssh_ip = "192.168.3.103"

#wifi_mode 802.  11b/11g/11n/11ac
wifi_mode = "11n"
#test time length each time
test_time = 30
#rerun test times
test_times = 100

#udp baseline
"""
UDP baseline of the bottleneck of our link,
in our test enviroment the bottleneck is the wnic of one PC

To test the wnic(PC) limit throughput
iperf test the bw of two PC
iperf3 -s /iperf3 -c 192.168.3.102  
iperf -u -s /iperf -c 192.168.3.102 -t 60 -i 1 -b 300M   

Rerun this test many times to get udp_baselines: 
11ac limit link bw: 590Mbps
11n limit link bw : 210Mbps
11g limit link bw : 26Mbps
11b limit link bw : 7Mbps
"""
wifi_mode_max_rate_dict = {'11b': 7 * 1024, '11g': 26 * 1024, '11n': 210 * 1024, '11ac': 590 * 1024}

#RTT condition to emulate
to_test_RTT = [10,80,200]

#log back up path
local_log_path = "~/ack_test_log/test_0916/te_ac_2"
remote_log_path = "~/log"

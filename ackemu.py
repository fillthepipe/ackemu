#-*- coding:utf-8 -*-
import time
import config
import os
from utils import ssh_conn,ssh_exec_cmd,ssh_conn_close,cal_ack_rate,cal_pack_rate,log_bak
from tqdm import tqdm


def get_ssh_conn():
    """
    get receiver ssh connect
    :return:recever ssh conn
    """
    receiver_ssh_ip = config.receiver_ssh_ip
    # sender_ssh_ip = config.sender_ssh_ip
    user_name = config.username
    passwd = config.passwd
    # sender = ssh_conn(sender_ssh_ip,user_name,passwd)
    receiver = ssh_conn(receiver_ssh_ip,user_name,passwd)
    return receiver

def get_test_cmd(send_rate,ack_rate,test_time,wifi_mode,test_mode):
    """
    :param send_rate:
    :param ack_rate:
    :param test_time:
    :param wifi_mode:
    :return: test command
    """
    sender_data_ip = config.sender_data_ip
    receiver_data_ip = config.receiver_data_ip
    file_name_tail = wifi_mode + '_' + test_mode + '_' + \
                     time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time())) + '.txt'
    data_recv_log = 'data_receiver_' + file_name_tail
    data_send_log = 'data_sender_' + file_name_tail
    ack_recv_log = 'ack_receiver_' + file_name_tail
    ack_send_log = 'ack_sender_' + file_name_tail

    # print data_recv_log
    cmd_dict = {}
    # cmd_dict['data_receiver_cmd'] = "nohup iperf3 -s -i 1 -d > %s 2>&1 &" % (data_recv_log)
    # cmd_dict['data_sender_cmd'] = "nohup iperf3 -c %s -i 1 -b %sK -l 1472 -u -t %s -d > %s 2>&1 &" % \
    #                   (receiver_data_ip, send_rate, test_time, data_send_log)
    # cmd_dict['ack_reveiver_cmd'] = 'nohup iperf3 -s -i 1 -d > %s 2>&1 &' % (ack_recv_log)
    # cmd_dict['ack_sender_cmd'] = 'nohup iperf3 -c %s -i 1 -b %sK -l 52 -u -t %s -d > %s  2>&1 &' % \
    #                  (sender_data_ip, ack_rate, test_time, ack_send_log)
    cmd_dict['data_receiver_cmd'] = "iperf3 -s -i 1 -d -1 > %s &" % (data_recv_log)
    cmd_dict['data_sender_cmd'] = "iperf3 -c %s -i 1 -b %sK -l 1472 -u -t %s -d > %s &" % \
                      (receiver_data_ip, send_rate, test_time, data_send_log)
    cmd_dict['ack_reveiver_cmd'] = 'iperf3 -s -i 1 -d -1> %s &' % (ack_recv_log)
    cmd_dict['ack_sender_cmd'] = 'iperf3 -c %s -i 1 -b %sK -l 52 -u -t %s -d > %s &' % \
                     (sender_data_ip, ack_rate, test_time, ack_send_log)
    cmd_dict['kill_iperf3'] = 'pkill -9 iperf3'
    print "%s test command dict" % test_mode
    print cmd_dict
    return cmd_dict

def run_test(receiver_ssh,cmd_dict):
    """
    test schedule of single test
    :return: one pack or ack test done
    """
    #kill iperf if iperf running  before testing
    receiver_ssh.exec_command(cmd_dict["kill_iperf3"])
    os.system(cmd_dict["kill_iperf3"])

    # receiver exec iperf cmd as iperf server to receive data
    print "==========iperf recv data!==========="
    ssh_exec_cmd(receiver_ssh,"cd log &&"+cmd_dict['data_receiver_cmd'])
    # time.sleep(2)
    print "==========iperf recv data server open!==========="

    #sender exec iperf cmd as iperf server to receive ack
    print "==========iperf recv ack!==========="
    os.system("cd log &&"+cmd_dict['ack_reveiver_cmd'])
    time.sleep(2)
    print "==========iperf recv ack sver open!==========="

    #sender exec iperf cmd as iperf client to send data
    print "==========iperf send data!==========="
    os.system("cd log &&"+cmd_dict['data_sender_cmd'])
    print "==========iperf send data done!==========="

    #receiver exec iperf cmd as sender to send ack
    print "==========iperf send ack!==========="
    ssh_exec_cmd(receiver_ssh,"cd log &&"+cmd_dict['ack_sender_cmd'])
    print "==========iperf send ack done!==========="

    time.sleep(test_time+5)

def rerun_test(pack_data_send_rate, pack_send_rate,ack_data_send_rate, ack_send_rate, test_time, wifi_mode,test_times):
    """
    run test test_times(setted in config.py)
    :return: test done
    """
    print time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
    #get ssh
    receiver_ssh = get_ssh_conn()
    # re run PACK emu test
    print "rerun test %d times!!!" %test_times
    for i in tqdm(range(test_times)):
        for k in range(len(pack_send_rate)):
            print "==========No:%d-%d PACK Test Start!==========" % ((i+1),(k+1))
            cmd_dict = get_test_cmd(pack_data_send_rate[k], pack_send_rate[k], test_time, wifi_mode, "PACK%d"%(k+1))
            run_test(receiver_ssh, cmd_dict)
            time.sleep(5)
            print "==========No:%d-%d PACK Test Done!==========" % ((i+1),(k+1))
        # run ACK emu test
        for j in range(len(ack_send_rate)):
            print "==========No:%d-%d ACK Test Start!==========" %((i+1),(j+1))
            cmd_dict = get_test_cmd(ack_data_send_rate[j],ack_send_rate[j],test_time,wifi_mode,"ACK_%d"%(1 if j==0 else 2**j))
            run_test(receiver_ssh,cmd_dict)
            time.sleep(5)
            print "==========No:%d-%d ACK Test Done!==========" %((i+1),(j+1))
    #log backup
    log_bak(receiver_ssh,wifi_mode,test_times)
    ssh_conn_close(receiver_ssh)

    print time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
    print "GAME OVER!!!"


if __name__ == '__main__':
    #load config
    wifi_mode = config.wifi_mode
    test_time = config.test_time
    test_times = config.test_times
    wifi_mode_bw_dict = config.wifi_mode_max_rate_dict
    max_rate = wifi_mode_bw_dict[wifi_mode]
    RTT = config.to_test_RTT

    #testing
    pack_send_rate = []
    pack_data_send_rate = []
    for rtt in RTT:
        ack_send,data_send = cal_pack_rate(max_rate,rtt,wifi_mode)
        pack_send_rate.append(ack_send)
        pack_data_send_rate.append(data_send)
    ack_send_rate, ack_data_send_rate = cal_ack_rate(max_rate)
    print pack_send_rate, pack_data_send_rate,ack_send_rate,ack_data_send_rate

    #run test test_times
    rerun_test(pack_data_send_rate, pack_send_rate,ack_data_send_rate, ack_send_rate, test_time, wifi_mode,test_times)

import paramiko
import datetime
import config
import time
import os
# logging.raiseExceptions=False

def ssh_conn(ip,username,passwd):
    """
    connect server by paramiko
    """
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(ip,22,username,passwd)
        paramiko.util.log_to_file("paramiko.log")
        print "ssh to %s created at %s!" %(ip,datetime.datetime.now())
        return ssh
    except:
        print "ssh to %s Failed!!" %ip


def ssh_exec_cmd(ssh,cmd):
    """
    Exec command on ssh conn
    """
    try:
        # out = []
        # stdin,stdout,stderr = ssh.exec_command(cmd)
        # tmp = stdout.readlines()
        # out.append(tmp)
        transport = ssh.get_transport()
        channel = transport.open_session()
        channel.exec_command(cmd)   #this exec method not blocking
        print 'ssh cmd exec success!'
    except:
        print "ssh cmd exec error!!!"

def ssh_conn_close(ssh):
    """
    close ssh conn
    """
    try:
        ssh.exec_command('pkill -9 iperf3')
        time.sleep(1)
        ssh.close()
        print "ssh conn closed & iperf3 pkilled!"
    except:
        print 'ssh close Error!!'

def cal_pack_rate(max_rate,RTT,wifi_mode):
    """
    :param max_rate:
    :return: rate Kbps
    """
    if wifi_mode == 'b' and RTT == 10:
        pack_cnt = (max_rate * 1024) / ((1472 + 52) * 8)

    else:
        pack_cnt = 1*1000*4 / RTT
    pack_data_cnt = int(float((max_rate * 1024 - pack_cnt * 52 * 8) / (1472 * 8)))
    pack_data_send_rate = 1472 * pack_data_cnt * 8 / 1024
    pack_send_rate = 52 * pack_cnt * 8 / 1024
    # print pack_cnt,pack_data_cnt,pack_data_send_rate,pack_send_rate
    print pack_cnt

    return pack_send_rate,pack_data_send_rate

def cal_ack_rate(max_rate):
    """
    :param max_rate:
    :return: rate Kbps
    """
    k = [1, 2, 4, 8, 16]
    ack_cnt = [(max_rate * 1024) / ((1472 * n + 52) * 8) for n in k]
    ack_data_cnt = [(max_rate * 1024) * n / ((1474 * n + 52) * 8) for n in k]
    ack_send_rate = [52 * m * 8 / 1024 for m in ack_cnt]
    ack_data_send_rate = [1472 * m * 8 / 1024 for m in ack_data_cnt]
    # print ack_cnt,ack_data_cnt,ack_send_rate,ack_data_send_rate
    print ack_cnt
    return ack_send_rate,ack_data_send_rate

def log_bak(receiver_ssh,wifi_mode,test_times):
    """
    backup remote and local log
    """
    compress_file_name_local = 'log_%s_%s_%s_%d.tar.gz'% \
                         ('local',time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time())),
                          wifi_mode,test_times)
    ##set ssh-key before this
    remote_scp_to_local = 'scp * %s@%s:%s'%\
                          (config.username,config.sender_ssh_ip,config.local_log_path)
    compress_file_name_remote = 'log_%s_%s_%s_%d.tar.gz' % \
                               ('remote',time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time())),
                                wifi_mode,test_times)
    remote_log_bak_cmd = 'cd %s && tar -czf %s *.txt && %s && mv * ../log_bak'%\
                     (config.remote_log_path, compress_file_name_remote,remote_scp_to_local)
    local_log_bak_cmd = "cd log && tar -czf %s *.txt && mv * %s" %\
                        (compress_file_name_local,config.local_log_path)
    code_bak = "cp *.py *.log %s" %\
               (config.local_log_path)

    print "log bak cmd",remote_log_bak_cmd,local_log_bak_cmd
    receiver_ssh.exec_command(remote_log_bak_cmd)
    os.system(local_log_bak_cmd)
    os.system(code_bak)

    print "log bak success!"

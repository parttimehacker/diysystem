#!/usr/bin/python3
''' Diyhas raspberry pi system status class '''

import datetime
import time
import socket

import psutil

class SystemUtility():
    ''' Check and publish process status information '''

    def __init__(self, client):
        ''' server system status monitor thread with MQTT reporting '''
        self.client = client
        self.host = socket.gethostname()
        self.boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        self.running_since = self.boot_time.strftime("%d. %B %Y")

    def get_cpu(self,):
        ''' publish cpu use as a percentage '''
        topic = "diyhas/"+self.host+"/cpu"
        value = psutil.cpu_percent(interval=1)
        info = "{0:.1f}".format(value)
        self.client.publish(topic, str(info), 0, True)

    def get_memory(self,):
        ''' publish memory use as a percentage '''
        topic = "diyhas/"+self.host+"/memory"
        value = psutil.virtual_memory()[2]
        info = "{0:.1f}".format(value)
        self.client.publish(topic, str(info), 0, True)

    def get_disk(self,):
        ''' publish disk space used as a percentage '''
        topic = "diyhas/"+self.host+"/disk"
        value = psutil.disk_usage('/')[3]
        info = "{0:.1f}".format(value)
        self.client.publish(topic, str(info), 0, True)

    def get_up_time(self,):
        ''' publish up time in days, hours, minutes and seconds '''
        topic = "diyhas/"+self.host+"/uptime"
        seconds = int(time.time()) - int(psutil.boot_time())
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        up_time = [days, hours, minutes, seconds]
        up_time_info = ":".join(str(v) for v in up_time)
        self.client.publish(topic, up_time_info, 0, True)

    def check_system_status(self,):
        ''' collect and publish four system status values '''
        self.get_cpu()
        self.get_memory()
        self.get_disk()
        self.get_up_time()

if __name__ == '__main__':
    exit()

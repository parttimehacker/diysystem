#!/usr/bin/python3
''' Diyhas raspberry pi system status class '''

import datetime
import time
import socket

import psutil

from gpiozero import CPUTemperature

class SystemUtility():
    ''' Check and publish process status information '''

    def __init__(self, client):
        ''' server system status monitor thread with MQTT reporting '''
        self.client = client
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #connect to any target website
        sock.connect(('google.com', 0))
        self.host = socket.gethostname()
        self.ip_address = sock.getsockname()[0]
        sock.close()
        self.cpu = "0.0"
        self.memory = "0.0"
        self.available = "0.0"
        self.free = "0.0"
        self.disk = "0.0"
        self.celsius = "0.0"
        self.boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        self.running_since = self.boot_time.strftime("%d. %B %Y")

    def get_cpu(self,):
        ''' publish cpu use as a percentage '''
        topic = "diyhas/"+self.host+"/cpu"
        value = psutil.cpu_percent(interval=1)
        info = "{0:.1f}".format(value)
        self.client.publish(topic, str(info), 0, True)
        self.cpu = info

    def get_cpu_temperature(self,):
        ''' publish cpu temperature in celsius '''
        topic = "diyhas/"+self.host+"/cpucelsius"
        cpu = CPUTemperature()
        info = "{0:.1f}".format(cpu.temperature)
        self.client.publish(topic, str(info), 0, True)
        self.celsius = info

    def get_memory(self,):
        ''' publish memory use as a percentage '''
        topic = "diyhas/"+self.host+"/memory"
        mem = psutil.virtual_memory()
        # Divide from Bytes -> KB -> MB
        self.available = str(round(mem.available/1024.0/1024.0,1))
        self.memory = str(round(mem.total/1024.0/1024.0,1))
        #info = "{0:.1f}".format(self.available)
        self.client.publish(topic, self.memory, 0, True)

    def get_disk(self,):
        ''' publish disk space used as a percentage '''
        topic = "diyhas/"+self.host+"/disk"
        disk = psutil.disk_usage('/')
        # Divide from Bytes -> KB -> MB -> GB
        self.free = str(round(disk.free/1024.0/1024.0/1024.0,1))
        self.disk = str(round(disk.total/1024.0/1024.0/1024.0,1))
        #info = "{0:.1f}".format(self.free)
        self.client.publish(topic, self.free, 0, True)

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
        self.get_cpu_temperature()
        self.get_memory()
        self.get_disk()
        self.get_up_time()

if __name__ == '__main__':
    exit()

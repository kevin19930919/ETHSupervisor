import subprocess
from subprocess import check_output
import os
import sys

from mailModule import MailHandler

class ETHMinerHandler():

    minerModulePath = '/data2/kevin7552/ETHMinner/nanominer-linux-3.3.13'
    minerScript = 'nanominer'


    @staticmethod
    def execute_command_by_subprocess_popen(command):
        pop = subprocess.Popen(command, shell=True, executable='/bin/bash', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout,stderr = pop.communicate()
        return stdout.decode('utf-8'), stderr.decode('utf-8')
    
    @staticmethod
    def check_number_of_users():
        command = f"last|grep logged"
        pop = subprocess.Popen(command, shell=True, executable='/bin/bash', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        numerUser = 0
        while True:
            line = pop.stdout.readline()
            if not line:
                break
            numerUser+=1
        return numerUser
    
    @classmethod
    def get_ethminer_pid(cls):
        name = f'./{cls.minerScript}'
        subprocess.check_output(["pidof","-s",name])
        pidList = list(map(lambda x: int(x), check_output(["pidof",name]).split()))
        return pidList
    
    @classmethod    
    def kill_miner(cls, pids):
        [cls.execute_command_by_subprocess_popen(f'kill -9 {pid}') for pid in pids]
    
    @classmethod
    def start_ethminer(cls):
        command = f"cd {cls.minerModulePath} ; ./{cls.minerScript} &> /dev/null &"
        stdout, stderr = cls.execute_command_by_subprocess_popen(command)

    @staticmethod
    def is_anyone_connect_or_disconnect(usersRightNow, usersBeforeProcess):
        return usersRightNow != usersBeforeProcess

        


if __name__ == "__main__":
    #execute ETH miner service
    ETHMinerHandler.start_ethminer()
    #get number of users connect to this server when you start mining
    usersBeforeProcess = ETHMinerHandler.check_number_of_users()
    
    while True:
        #get number of users connect to server right now
        usersRightNow = ETHMinerHandler.check_number_of_users()
        
        #check if there anyone connect or disconnect to server
        isAnyActivityOnHost = ETHMinerHandler.is_anyone_connect_or_disconnect(usersRightNow, usersBeforeProcess)
        if isAnyActivityOnHost:
            try:
                pidList = ETHMinerHandler.get_ethminer_pid()
                #kill all miner service
                ETHMinerHandler.kill_miner(pidList)
                MailHandler.send_mail(f"detect an user log in server,stop mining")
            except:
                #exit self
                sys.exit()    
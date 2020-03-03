#!/usr/bin/env python3
#This file contains system level stuff
import socket
import os

def ip_of_machine():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname('Tims-iMac')
    return IPAddr



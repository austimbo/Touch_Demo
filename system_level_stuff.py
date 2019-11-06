#!/usr/bin/env python3
#This file contains system level stuff
import socket

def ip_of_machine():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    return IPAddr

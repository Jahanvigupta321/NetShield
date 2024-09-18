#!/usr/bin/python
#
#
# Events.py
#
from .core import is_windows, is_posix
import sys
#dont know if needed but no issues for now
if is_posix():
        sys.exit(1)
#changed to only import on windows
if is_windows():
    import win32api, win32con, win32evtlog, win32evtlogutil, win32security
    def HoneyPotEvent():
        #lets try and write an event log
        process = win32api.GetCurrentProcess()
        token = win32security.OpenProcessToken(process, win32con.TOKEN_READ)
        my_sid = win32security.GetTokenInformation(token, win32security.TokenUser)[0]
        AppName = "NetShield"
        eventID = 1
        category =5
        myType = win32evtlog.EVENTLOG_WARNING_TYPE
        descr =["NetShield Detected access to a honeypot port", "The offending ip has been blocked and added to the local routing table",]
        data = "Application\0Data".encode("ascii")
        win32evtlogutil.ReportEvent(AppName, eventID, eventCategory=category, eventType=myType, strings=descr, data=data, sid=my_sid)


    def NetShieldStartEvent():
        process = win32api.GetCurrentProcess()
        token = win32security.OpenProcessToken(process, win32con.TOKEN_READ)
        my_sid = win32security.GetTokenInformation(token, win32security.TokenUser)[0]
        AppName = "NetShield"
        eventID = 1
        category =5
        myType = win32evtlog.EVENTLOG_INFORMATION_TYPE
        descr =["NetShield has started and begun monitoring the selected ports ",]
        data = "Application\0Data".encode("ascii")
        win32evtlogutil.ReportEvent(AppName, eventID, eventCategory=category, eventType=myType, strings=descr, data=data, sid=my_sid)



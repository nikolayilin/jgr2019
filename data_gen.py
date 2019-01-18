#!/usr/bin/env python3
import subprocess   
import os 
from datetime import datetime, timedelta

startday = datetime(2015,12,31,0)
endday = datetime(2016,12,30,12)
day = startday
day_number = 2*(endday - startday).days    

print(day_number)
thread_number = 24  
for i_block in range(day_number // thread_number +1):
    threads = []
    for i in range(thread_number):
        threads.append(subprocess.Popen(['./thread.py', day.strftime('%Y'), day.strftime('%m'), day.strftime('%d'), day.strftime('%H')]))    
        day += timedelta(hours=12)
    for i in range(thread_number):
        threads[i].wait()

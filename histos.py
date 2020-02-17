import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import fileinput
import csv
import datetime
from taTools import *

#set filename
#execute %matplotlib qt on spyder before running
filename = input("What data do you want to view? ")
filename = filename + ".dat"
#filename = "0514.dat"

min_size = 11
max_size = 50

anispeed = 250

fcount = 144

#init
tasdnum,tasdx,tasdy,tasdz =[],[],[],[]
tasdxyz(tasdnum,tasdx,tasdy,tasdz)

tasdlat,tasdlon,tasdalt = [],[],[]
tasdgps(tasdlat,tasdlon,tasdalt)

YYMMDD = []
hhmmss = []
Hitdetnum = []
lv0rate = []
lv1rate = []
warn = []
dontuse = []
quality = []

detector = []
dlv0rate = []

#YYMMDD = datetime.datetime.strptime(YYMMDD, "%Y-%B-%d")
#timestamp = pd.to_datetime(T[0:])
#timestamp = timestamp.strftime("%Y-%m-%d")
#timestamp = pd.to_datetime(T[0:]).strftime("%Y-%m-%d")
#YYMMDD = timestamp
#converted_dates = list(map(datetime.datetime.strptime, YYMMDD, len(YYMMDD)*['%Y-%m-%d']))
#formatter = YYMMDD.DateFormatter('%Y-%m-%d')

#open file
file = open(filename,'r')

for line in file:
    columns = line.split()

    YYMMDD.append(int(columns[0]))
    hhmmss.append(int(columns[1]))
    Hitdetnum.append(int(columns[2]))
    lv0rate.append(float(columns[3]))
    lv1rate.append(float(columns[4]))
    dontuse.append(int(columns[5]))
    warn.append(int(columns[6]))
    quality.append(int(columns[7]))
    
    
#specifying detector
#look into passing as strings
int_detector = int(input("What detector would you like to view? "))
for i in range(len(Hitdetnum)):
    if (int_detector == Hitdetnum[i]):
        detector.append(Hitdetnum[i])
        
        for j in range(len(detector)):
            dlv0rate.append(lv0rate[j])


#get each unique time in order
times = [hhmmss[0]]

for i in range(len(hhmmss) - 1):
    if (hhmmss[i] != hhmmss[i + 1] and hhmmss[i] > 000000):
        times.append(hhmmss[i + 1])
        
        
#min and max values
WorkingNTASD=len(YYMMDD)  
Rnglv0rate = []      
   
for i in range(0,WorkingNTASD):
    for j in range(len(tasdnum[0])):          
        if(Hitdetnum[i]==tasdnum[0][j] and dontuse[j]==0 and warn[j]==0 and quality[j]==0):
            Rnglv0rate.append(lv0rate[j])
            minrate = min(Rnglv0rate)
            maxrate = max(Rnglv0rate)


#for defining the size in relation of the quality
minqual = min(quality)
maxqual = max(quality)
        
#plot and animation setup

x = []
y = []

#with open(filename,'r') as csvfile:
    #plots = csv.reader(csvfile, delimiter=' ')
    #for columns in plots:
        #x.append(int(columns[1]))
        #y.append(float(columns[3]))

fig, ax = plt.subplots()
line, = ax.plot(hhmmss, dlv0rate, 'o', color='k')

#animation
def animate(i):
    
    x = hhmmss[0][0,i]
    y = dlv0rate[0][0,i]
    

        
    line.set_data(x[:i], y[:i])
    #line.axes.axis([hhmmss[000000], hhmmss[245000], minrate, maxrate])
    return line,

ani = animation.FuncAnimation(fig, animate, len(x), fargs=[x, y, line],
                              interval=25, blit=True)
plt.show()
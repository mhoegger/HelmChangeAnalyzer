import json
import matplotlib.pylab as plt
import numpy as np
import datetime
from matplotlib.patches import Rectangle
import sys
import datetime
import matplotlib.cbook as cbook
from matplotlib.dates import bytespdate2num, num2date
from matplotlib.ticker import Formatter
import matplotlib.dates as mdates
import os
from pathlib import Path
import calendar

def analyze1(pathJson, pathOut):

    try:
        os.mkdir(pathOut + "/histogram")
    except:
        print("exists already")

    with open(pathJson, 'r') as f:
        dict = json.load(f)

    keys=["version","appVersion","description","engine","email","name","maintainers","sources","icon","home","apiVersion"]
    for key in keys:

        addition =[]
        changes =[]
        deletions =[]
        modul = []

        #print(len(dict['files']))

        for files in dict['files']:
            print(files)
            addition.append(files[key]["addition"])
            changes.append(files[key]["change"])
            deletions.append(files[key]["deletion"])
            modul.append(files["ModulName"])

        fig, ax = plt.subplots()
        bins=np.linspace(0,70,71)
        plt.hist([addition, deletions, changes], range=(0,75),bins=bins,alpha=0.5, label=["addition","deletions","changes"])
        plt.legend(loc='best')
        plt.yscale("log")
        plt.title(key)
        #plt.show()
        plt.savefig(pathOut+"/histogram/histogram_"+key+".png")
        plt.clf()

def analyze2(pathJson, pathOut):
    try:
        os.mkdir(pathOut + "/datecurve")
    except:
        print("exists already")

    with open(pathJson, 'r') as f:
        dict = json.load(f)


    keys=["version","appVersion","description","engine","email","name","maintainers","sources","icon","home","apiVersion"]
    for key in keys:
        addition ={}
        changes ={}
        deletions ={}
        for files in dict['files']:
            for d in files[key]["additionDates"]:
                #readable = datetime.datetime.utcfromtimestamp(float(d)).strftime('%Y-%m-%d')
                readable = datetime.datetime.utcfromtimestamp(float(d))
                if not readable in addition:
                    addition[readable]=1
                else:
                    addition[readable] = 1+addition[readable]
            for d in files[key]["changeDates"]:
                #readable = datetime.datetime.utcfromtimestamp(float(d)).strftime('%Y-%m-%d')
                readable = datetime.datetime.utcfromtimestamp(float(d))
                if not readable in changes:
                    changes[readable] = 1
                else:
                    changes[readable] = 1+changes[readable]
            for d in files[key]["deletionDates"]:
                #readable = datetime.datetime.utcfromtimestamp(float(d)).strftime('%Y-%m-%d')
                readable = datetime.datetime.utcfromtimestamp(float(d))
                if not readable in deletions:
                    deletions[readable] = 1
                else:
                    deletions[readable] = 1+deletions[readable]
        print(changes)
        fig = plt.figure(figsize=(10,10))
        ax = fig.add_subplot(111, label="1")
        ax2 = fig.add_subplot(111, label="2", frame_on=False)
        ax3 = fig.add_subplot(111, label="3", frame_on=False)


        base = datetime.datetime.strptime('2018-05-01','%Y-%m-%d')
        date_list = [(base + datetime.timedelta(days=x)) for x in range(0, 129)]
        print(date_list)



        if len(addition) != 0:
            print(sorted(addition.items()))
            listsa = sorted(addition.items())  # sorted by key, return a list of tuples
            xa, ya = zip(*listsa)  # unpack a list of pairs into two tuples
            ax.plot_date(xa, ya,'o-',label="addition", color="C0", markersize=3)
            ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_xlim(xmin=date_list[0], xmax=date_list[-1])

        else:
            ax.set_xticks([])
            ax.set_yticks([])


        if len(deletions) != 0:
            listsd = sorted(deletions.items())  # sorted by key, return a list of tuples
            xd, yd = zip(*listsd)  # unpack a list of pairs into two tuples
            ax3.plot_date(xd, yd,'o-',label="deletions", color="C1",markersize=3)
            ax3.format_xdata = mdates.DateFormatter('%Y-%m-%d')
            ax3.set_xlim(xmin=date_list[0], xmax=date_list[-1])

        if len(changes) != 0:
            listsc = sorted(changes.items())  # sorted by key, return a list of tuples
            xc, yc = zip(*listsc)  # unpack a list of pairs into two tuples
            ax2.plot_date(xc, yc,'o-',label="changes", color="C2",markersize=3)
            ax2.format_xdata = mdates.DateFormatter('%Y-%m-%d')


            ax3.set_xticks([])
            ax3.set_yticks([])

            ax2.set_xticks(date_list)
            ax2.set_xticklabels(date_list , rotation=90)
            ax2.set_xlim(xmin=date_list[0], xmax=date_list[-1])
            ax2.set_ylim(0, 25)

            ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            every_nth = 7
            for n, label in enumerate(ax2.xaxis.get_ticklabels()):
                if n % every_nth != 0:
                   label.set_visible(False)
        else:
            ax3.set_xticks(date_list)

            ax2.set_xticks([])
            ax2.set_yticks([])
            ax3.set_xticklabels(date_list,rotation=90)
            ax3.set_xlim((date_list[0], date_list[-1]))
            ax3.set_ylim(0, 25)
            ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            every_nth = 7
            for n, label in enumerate(ax3.xaxis.get_ticklabels()):
                if n % every_nth != 0:
                   label.set_visible(False)

        plt.title(key)
        fig.legend(loc='best')
        plt.savefig(pathOut+"/datecurve/datecurve_"+key+".png")
        plt.clf()

def analyze3(pathJson, pathOut):
    try:
        os.mkdir(pathOut+"/VersionUpdateHistograms")
    except:
        print("exists already")

    with open(pathJson, 'r') as f:
        dict = json.load(f)

    #VERSION-HISTOGRAM
    versiontypes =["version","appVersion","apiVersion"]

    for k in versiontypes:

        Service=[]
        Minor=[]
        Major=[]
        for files in dict['files']:
            for d in files[k]["VersionUpdates"]:
                if d["type"]=="Service":
                    Service.append(d["increment"])
                elif d["type"]=="Minor":
                    Minor.append(d["increment"])
                elif d["type"] == "Major":
                    Major.append(d["increment"])

        fig, ax = plt.subplots()
        bins=np.linspace(-8,8,16)
        plt.hist([Major, Minor, Service], range=(-8,8),bins=bins,alpha=0.5, label=["Major","Minor","Service"])
        plt.legend(loc='best')
        #plt.yscale("log")
        plt.title("VersionType")
        #plt.show()
        plt.savefig(pathOut+"/VersionUpdateHistograms/histogram_"+k+"Updates.png")
        plt.clf()

def analyze5(pathJson, pathOut):

    with open(pathJson, 'r') as f:
        dict = json.load(f)

    my_file = Path(pathOut+"/CountPerKey.txt")
    if my_file.is_file():
        os.remove((pathOut+"/CountPerKey.txt"))
    fw = open(pathOut+"/CountPerKey.txt","x")

    keys=["version","appVersion","description","engine","email","name","maintainers","sources","icon","home","apiVersion"]

    for key in keys:
        addition = 0
        change = 0
        deletion = 0
        for files in dict['files']:
            addition += files[key]["addition"]
            change += files[key]["change"]
            deletion += files[key]["deletion"]

        fw.write(key+": "+str(addition)+"|"+str(change)+"|"+str(deletion)+"\n")
    fw.close()


def analyze6(pathJson, pathOut):

    with open(pathJson, 'r') as f:
        dict = json.load(f)

    my_file = Path(pathOut+"/CountPerModul.txt")
    if my_file.is_file():
        os.remove((pathOut+"/CountPerModul.txt"))
    fw = open(pathOut+"/CountPerModul.txt","x")

    keys=["version","appVersion","description","engine","email","name","maintainers","sources","icon","home","apiVersion"]
    for files in dict['files']:
        addition = 0
        change = 0
        deletion = 0
        for key in keys:
            addition += files[key]["addition"]
            change += files[key]["change"]
            deletion += files[key]["deletion"]

        fw.write(files["ModulName"]+": "+str(addition)+"|"+str(change)+"|"+str(deletion)+"\n")
    fw.close()

def analyze(pathJson, pathOut):
    with open(pathJson, 'r') as f:
        dict = json.load(f)

    base = datetime.datetime.strptime('2018-05-01','%Y-%m-%d')
    date_list = [(base + datetime.timedelta(days=x)) for x in range(0, 129)]

    dateDict = {}
    for d in date_list:
        dateDict[d.strftime('%Y-%m-%d')]={}
        dateDict[d.strftime('%Y-%m-%d')]["addition"]=0
        dateDict[d.strftime('%Y-%m-%d')]["deletion"]=0
        dateDict[d.strftime('%Y-%m-%d')]["change"]=0

    keys=["version","appVersion","description","engine","email","name","maintainers","sources","icon","home","apiVersion"]
    additiondays=[]
    deletondays=[]
    changendays=[]

    for key in keys:
        for files in dict['files']:
            for d in files[key]["additionDates"]:
                readable = datetime.datetime.utcfromtimestamp(float(d)).strftime('%Y-%m-%d')
                additiondays.append(calendar.day_name[datetime.datetime.utcfromtimestamp(float(d)).weekday()])
                dateDict[readable]["addition"] += 1
            for d in files[key]["changeDates"]:
                readable = datetime.datetime.utcfromtimestamp(float(d)).strftime('%Y-%m-%d')
                changendays.append(calendar.day_name[datetime.datetime.utcfromtimestamp(float(d)).weekday()])
                dateDict[readable]["change"] += 1
            for d in files[key]["deletionDates"]:
                readable = datetime.datetime.utcfromtimestamp(float(d)).strftime('%Y-%m-%d')
                deletondays.append(calendar.day_name[datetime.datetime.utcfromtimestamp(float(d)).weekday()])
                dateDict[readable]["deletion"] += 1

    print(sorted(dateDict, key=lambda x: -dateDict[x]['addition']))
    print(sorted(dateDict, key=lambda x: -dateDict[x]['deletion']))
    print(sorted(dateDict, key=lambda x: -dateDict[x]['change']))

    fig, ax = plt.subplots()
    bins = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    plt.hist([additiondays, deletondays, changendays], alpha=0.5, align="left",
             label=["addition", "deletions", "changes"])
    plt.legend(loc='best')
    plt.title("Weekdays")
    plt.xticks(range(len(bins)), bins)
    plt.savefig(pathOut + "/histogram_weekdays.png")
    plt.clf()

    addline=[]
    delline=[]
    chaline=[]
    dateline=[]

    fig, ax = plt.subplots()

    for d in dateDict:
        dateline.append(d)
        addline.append(dateDict[d]["addition"])
        delline.append(dateDict[d]["deletion"])
        chaline.append(dateDict[d]["change"])


    listsa = sorted(dateDict.items())  # sorted by key, return a list of tuples
    xa, ya = zip(*listsa)  # unpack a list of pairs into two tuples
    ax.plot(dateline, addline, '-', label="addition", color="C0", markersize=3)
    ax.plot(dateline, delline, '-', label="deletion", color="C1", markersize=3)
    ax.plot(dateline, chaline, '-', label="change", color="C2", markersize=3)
    plt.title("Timeseries")
    plt.legend(loc='best')
    every_nth = 7
    for n, label in enumerate(ax.xaxis.get_ticklabels()):
        if n % every_nth != 0:
            label.set_visible(False)
    plt.xticks(rotation='vertical')
    plt.savefig(pathOut + "/Timeseries.png")
    plt.clf()


if __name__ == "__main__":
    analyze(sys.argv[1],sys.argv[2])
    analyze1(sys.argv[1],sys.argv[2])
    analyze2(sys.argv[1],sys.argv[2])
    analyze3(sys.argv[1],sys.argv[2])
    analyze5(sys.argv[1],sys.argv[2])
    analyze6(sys.argv[1],sys.argv[2])

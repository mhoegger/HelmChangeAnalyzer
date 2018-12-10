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

def analyze1(pathJson, pathOut):

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
        plt.savefig(pathOut+"/histogram_"+key+".png")
        plt.clf()

def analyze(pathJson, pathOut):
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
            #ax.set_xticks(date_list)
            #ax.set_xticklabels(date_list,rotation=90)
            #ax.set_yticks([])
            #ax.set_xlim((date_list[0], date_list[-1]))
            #every_nth = 7
            #for n, label in enumerate(ax.xaxis.get_ticklabels()):
            #    if n % every_nth != 0:
            #        label.set_visible(False)
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

            #ax3.set_xticks(date_list)
            #ax3.set_xticklabels(date_list,rotation=90)
            #ax3.set_yticks([])
            #ax3.set_xlim((date_list[0], date_list[-1]))
            #every_nth = 7
            #for n, label in enumerate(ax3.xaxis.get_ticklabels()):
            #    if n % every_nth != 0:
            #        label.set_visible(False)



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
        print(date_list[0])
        print(date_list[-1])








        fig.legend(loc='best')


        plt.savefig(pathOut+"/datecurve_"+key+".png")
        plt.clf()
    """
    versionCount = []
    sourcesCount = []
    for files in dict:
        if files["Versions"][0] == "":
            versionCount.append(0)
        else:
            versionCount.append(len(files["Versions"]))
        try:
            sourcesCount.append(len(files["AllSources"]))
        except:
            sourcesCount.append(0)

    print(versionCount)

    creations = {}
    updates = {}
    deletions = {}
    versionUpdates = {}

    for files in dict:
        for changes in files["Changes"]:
            date = changes["Date"]
            if changes["NewVersion"] == True:
                if not date in versionUpdates:
                    versionUpdates[date]=1
                else:
                    versionUpdates[date] = 1+versionUpdates[date]
            if changes["Type"] == "File-Creation":
                if not date in creations:
                    creations[date]=1
                else:
                    creations[date] = 1+creations[date]
            elif changes["Type"] == "File-Update":
                if not date in updates:
                    updates[date]=1
                else:
                    updates[date] = 1+updates[date]
            elif changes["Type"] == "File-Removal":
                if not date in deletions:
                    deletions[date]=1
                else:
                    deletions[date] = 1+deletions[date]

    print(creations)
    print(updates)
    print(deletions)


    lists = sorted(creations.items()) # sorted by key, return a list of tuples

    x, y = zip(*lists) # unpack a list of pairs into two tuples
    fig, ax = plt.subplots()
    plt.plot(x, y)
    plt.xticks(rotation='vertical')
    plt.title("creations")
    every_nth = 4
    for n, label in enumerate(ax.xaxis.get_ticklabels()):
        if n % every_nth != 0:
            label.set_visible(False)
    plt.savefig("creations.png")
    plt.clf()

    #----

    lists = sorted(updates.items()) # sorted by key, return a list of tuples

    x, y = zip(*lists) # unpack a list of pairs into two tuples
    fig, ax = plt.subplots()
    plt.plot(x, y)
    plt.xticks(rotation='vertical')
    plt.title("updates")

    every_nth = 4
    for n, label in enumerate(ax.xaxis.get_ticklabels()):
        if n % every_nth != 0:
            label.set_visible(False)
    plt.savefig("updates.png")
    p lt.clf()

    #----

    lists = sorted(deletions.items()) # sorted by key, return a list of tuples

    x, y = zip(*lists) # unpack a list of pairs into two tuples
    fig, ax = plt.subplots()
    plt.plot(x, y)
    plt.xticks(rotation='vertical')
    plt.title("deletions")

    every_nth = 4
    for n, label in enumerate(ax.xaxis.get_ticklabels()):
        if n % every_nth != 0:
            label.set_visible(False)
    plt.savefig("deletions.png")
    plt.clf()


    #----

    lists = sorted(versionUpdates.items()) # sorted by key, return a list of tuples

    x1, y1 = zip(*lists) # unpack a list of pairs into two tuples
    x = x1[3:]
    y = y1[3:]
    fig, ax = plt.subplots()

    plt.plot(x, y)
    plt.xticks(rotation='vertical')
    plt.title("versionUpdates")
    monday = 0
    dienstag = 0
    mittwuch = 0
    donnerstag = 0
    freitag = 0
    samstag = 0
    sonntag = 0
    for i in range(0,len(x)):
        date_t = x[i]
        now = datetime.date(*(int(s) for s in date_t.split('-')))
        if now.weekday()== 0:
            monday+=y[i]
        elif now.weekday()== 1:
            dienstag += y[i]
            a=plt.axvline(date_t,color='r')
            #plt.axvline(date_t,color='y')
        elif now.weekday()== 2:
            mittwuch += y[i]
            #plt.axvline(date_t,color='g')
        elif now.weekday()== 3:
            #plt.axvline(date_t,color='m')
            donnerstag += y[i]
        elif now.weekday()== 4:
            #plt.axvline(date_t,color='c')
            freitag += y[i]
        elif now.weekday()== 5:
            samstag += y[i]
            #plt.axvline(date_t,color='k')
        elif now.weekday()== 6:
            sonntag += y[i]
           #plt.axvline(date_t, color='b')
           #draw vertical line
    every_nth = 4
    for n, label in enumerate(ax.xaxis.get_ticklabels()):
        if n % every_nth != 0:
           label.set_visible(False)
    extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)

    plt.legend([extra, a, extra, extra, extra, extra, extra], ("Monday: "+str(monday), "Thuesday: "+str(dienstag),
                            "Wednessday: "+str(mittwuch),"Thursday: "+str(donnerstag),
                            "Friday: "+str(freitag), "Saturday: "+str(samstag), "Sunday: "+str(sonntag)))
    #plt.show()
    plt.savefig("versionUpdates.png")
    plt.clf()


    #----
    print(len(list(filter(lambda x: x==1, versionCount))))
    print(len(list(filter(lambda x: x==2, versionCount))))
    print(len(list(filter(lambda x: x==3, versionCount))))
    print(len(list(filter(lambda x: x==4, versionCount))))
    print(len(list(filter(lambda x: x==5, versionCount))))

    fig, ax = plt.subplots()
    bins=np.linspace(0,30,31)
    print(bins)
    plt.hist(versionCount, bins=bins, facecolor='blue', edgecolor='gray', rwidth=1, align='mid')
    #plt.show()
    plt.title("versions")

    plt.savefig("versions.png")
    plt.clf()

    #----
    print(len(list(filter(lambda x: x==1, versionCount))))
    print(len(list(filter(lambda x: x==2, versionCount))))
    print(len(list(filter(lambda x: x==3, versionCount))))
    print(len(list(filter(lambda x: x==4, versionCount))))
    print(len(list(filter(lambda x: x==5, versionCount))))

    fig, ax = plt.subplots()
    bins=np.linspace(0,max(sourcesCount),max(sourcesCount)+1)
    print(bins)
    plt.hist(sourcesCount, bins=bins, facecolor='blue', edgecolor='gray', rwidth=1, align='mid')
    #plt.show()
    plt.title("Sources per descriptor")

    plt.savefig("Sources _per_descriptor.png")
    plt.clf()
    """


if __name__ == "__main__":
    analyze(sys.argv[1],sys.argv[2])

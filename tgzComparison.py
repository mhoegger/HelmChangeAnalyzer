import subprocess
import os
import sys
import datetime
import operator
import pandas as pd
import glob
import json
import re
import shutil

class FileChanges:
    def __init__(self, trackingdir, tempStoragePath, filename=None):
        self.trackingdir = trackingdir
        self.tempStoragePath = tempStoragePath
        self.filename = filename
        self.fileHistory = []
        self.keywordDict = {}
        self.keywordDict["ModulName"] = filename

        self.keywordDict["version"] = {}
        self.keywordDict["version"]["addition"] = 0
        self.keywordDict["version"]["change"] = 0
        self.keywordDict["version"]["deletion"] = 0
        self.keywordDict["version"]["additionDates"] = []
        self.keywordDict["version"]["changeDates"] = []
        self.keywordDict["version"]["deletionDates"] = []

        self.keywordDict["appVersion"] = {}
        self.keywordDict["appVersion"]["addition"] = 0
        self.keywordDict["appVersion"]["change"] = 0
        self.keywordDict["appVersion"]["deletion"] = 0
        self.keywordDict["appVersion"]["additionDates"] = []
        self.keywordDict["appVersion"]["changeDates"] = []
        self.keywordDict["appVersion"]["deletionDates"] = []

        self.keywordDict["description"] = {}
        self.keywordDict["description"]["addition"] = 0
        self.keywordDict["description"]["change"] = 0
        self.keywordDict["description"]["deletion"] = 0
        self.keywordDict["description"]["additionDates"] = []
        self.keywordDict["description"]["changeDates"] = []
        self.keywordDict["description"]["deletionDates"] = []

        self.keywordDict["engine"] = {}
        self.keywordDict["engine"]["addition"] = 0
        self.keywordDict["engine"]["change"] = 0
        self.keywordDict["engine"]["deletion"] = 0
        self.keywordDict["engine"]["additionDates"] = []
        self.keywordDict["engine"]["changeDates"] = []
        self.keywordDict["engine"]["deletionDates"] = []

        self.keywordDict["email"] = {}
        self.keywordDict["email"]["addition"] = 0
        self.keywordDict["email"]["change"] = 0
        self.keywordDict["email"]["deletion"] = 0
        self.keywordDict["email"]["additionDates"] = []
        self.keywordDict["email"]["changeDates"] = []
        self.keywordDict["email"]["deletionDates"] = []

        self.keywordDict["name"] = {}
        self.keywordDict["name"]["addition"] = 0
        self.keywordDict["name"]["change"] = 0
        self.keywordDict["name"]["deletion"] = 0
        self.keywordDict["name"]["additionDates"] = []
        self.keywordDict["name"]["changeDates"] = []
        self.keywordDict["name"]["deletionDates"] = []

        self.keywordDict["maintainers"] = {}
        self.keywordDict["maintainers"]["addition"] = 0
        self.keywordDict["maintainers"]["change"] = 0
        self.keywordDict["maintainers"]["deletion"] = 0
        self.keywordDict["maintainers"]["additionDates"] = []
        self.keywordDict["maintainers"]["changeDates"] = []
        self.keywordDict["maintainers"]["deletionDates"] = []

        self.keywordDict["sources"] = {}
        self.keywordDict["sources"]["addition"] = 0
        self.keywordDict["sources"]["change"] = 0
        self.keywordDict["sources"]["deletion"] = 0
        self.keywordDict["sources"]["additionDates"] = []
        self.keywordDict["sources"]["changeDates"] = []
        self.keywordDict["sources"]["deletionDates"] = []

        self.keywordDict["icon"] = {}
        self.keywordDict["icon"]["addition"] = 0
        self.keywordDict["icon"]["change"] = 0
        self.keywordDict["icon"]["deletion"] = 0
        self.keywordDict["icon"]["additionDates"] = []
        self.keywordDict["icon"]["changeDates"] = []
        self.keywordDict["icon"]["deletionDates"] = []

        self.keywordDict["home"] = {}
        self.keywordDict["home"]["addition"] = 0
        self.keywordDict["home"]["change"] = 0
        self.keywordDict["home"]["deletion"] = 0
        self.keywordDict["home"]["additionDates"] = []
        self.keywordDict["home"]["changeDates"] = []
        self.keywordDict["home"]["deletionDates"] = []

        self.keywordDict["apiVersion"] = {}
        self.keywordDict["apiVersion"]["addition"] = 0
        self.keywordDict["apiVersion"]["change"] = 0
        self.keywordDict["apiVersion"]["deletion"] = 0
        self.keywordDict["apiVersion"]["additionDates"] = []
        self.keywordDict["apiVersion"]["changeDates"] = []
        self.keywordDict["apiVersion"]["deletionDates"] = []

        self.keywordDict["otherAddition"] = []
        self.keywordDict["otherDeletions"] = []
        self.dateOfChange = ""



    def unique_getlog(self):
        """
        Gets the whole git log history of repository denoted in the "trackingdir"
        Will return the log in chronological order. so oldest commit first.

        :return: log as a string
        """

        origdir = os.getcwd()
        os.chdir(self.trackingdir)

        cmd = "COLUMNS=200 git log --stat"

        r = subprocess.run(f"{cmd} --reverse", shell=True, stdout=subprocess.PIPE)

        log = r.stdout.decode("utf-8")
        os.chdir(origdir)
        return str(log)


    def checkout(self,id1, file1, id2, file2):
        origdir = os.getcwd()
        os.chdir(self.trackingdir)
        shutil.rmtree(self.tempStoragePath+"a/")
        try:
            os.mkdir(self.tempStoragePath+"a/")
        except:
            print("Dir exists")
        cmd = "COLUMNS=200 git --work-tree="+self.tempStoragePath+"a checkout "+id1+ " -- "+file1
        #print(cmd)
        r = subprocess.run(f"{cmd}", shell=True, stdout=subprocess.PIPE)
        cmd2= "tar -xvzf "+self.tempStoragePath+"a/"+file1+" -C "+self.tempStoragePath+"a"
        r = subprocess.run(f"{cmd2}", shell=True, stdout=subprocess.PIPE)

        shutil.rmtree(self.tempStoragePath+"b/")

        try:
            os.mkdir(self.tempStoragePath+"b/")
        except:
            print("Dir exists")


        cmd = "COLUMNS=200 git --work-tree="+self.tempStoragePath+"b checkout "+id2+ " -- "+file2
        #print(cmd)
        r = subprocess.run(f"{cmd}", shell=True, stdout=subprocess.PIPE)
        cmd2= "tar -xvzf "+self.tempStoragePath+"b/"+file2+" -C "+self.tempStoragePath+"b"
        r = subprocess.run(f"{cmd2}", shell=True, stdout=subprocess.PIPE)
        self.runDiff()


    def runDiff(self):
        origdir = os.getcwd()
        os.chdir(self.trackingdir)

        findACmd = "find "+self.tempStoragePath+"a/ -name Chart.yaml"
        pathToA = str(subprocess.run(f"{findACmd}", shell=True, stdout=subprocess.PIPE).stdout.decode("utf-8")).split("\n")[0]
        #print(str(pathToA))
        findBCmd = "find "+self.tempStoragePath+"b/ -name Chart.yaml"
        pathToB = str(subprocess.run(f"{findBCmd}", shell=True, stdout=subprocess.PIPE).stdout.decode("utf-8")).split("\n")[0]
        #print(pathToB)

        cmd = "diff "+str(pathToA)+" "+str(pathToB)
        #print(cmd)
        response = subprocess.run(f"{cmd}", shell=True, stdout=subprocess.PIPE).stdout.decode("utf-8")
        print(str(response))
        self.checkForKeywords(str(response))

    def checkForKeywords(self, changes):
        # temparary variable to save whether addition, deletion or change
        temp = {}
        for key in self.keywordDict:
            temp[key]="null"

        for line in changes.split("\n"):
            nonkey = True
            for key in self.keywordDict:
                if key in line:
                    nonkey = False
                    if line.startswith("<"):
                        temp[key] = "deletion"
                    if line.startswith(">") and temp[key] == "deletion":
                        temp[key] = "change"
                    if line.startswith(">") and temp[key] == "null":
                        temp[key] = "addition"
            if nonkey:
                if line.startswith("<"):
                    self.keywordDict["otherAddition"].append(line)
                elif line.startswith(">"):
                    self.keywordDict["otherDeletions"].append(line)
        print(temp["maintainers"])
        for key in self.keywordDict:
            if temp[key] == "addition":
                self.keywordDict[key]["addition"]=self.keywordDict[key]["addition"]+1
                self.keywordDict[key]["additionDates"].append(self.dateOfChange)

            elif temp[key] == "change":
                self.keywordDict[key]["change"] = self.keywordDict[key]["change"] + 1
                self.keywordDict[key]["changeDates"].append(self.dateOfChange)

            elif temp[key] == "deletion":
                self.keywordDict[key]["deletion"] = self.keywordDict[key]["deletion"] + 1
                self.keywordDict[key]["deletionDates"].append(self.dateOfChange)



    def extractHistory(self):
        date = None
        commitline = -5
        dateline = -5
        correctcommit = False
        commit = None
        log = self.unique_getlog()
        for idx, logline in enumerate(log.split("\n")):

            if logline.startswith("commit"):
                commitline = idx
                commit = logline.split("commit ")[-1]

            elif idx == commitline+2:
                dateline = idx
                datestr = ":".join(logline.split(":")[1:]).strip()
                d = datetime.datetime.strptime(datestr, "%a %b %d %H:%M:%S %Y %z").date()
                t = datetime.datetime.strptime(datestr, "%a %b %d %H:%M:%S %Y %z").time()
                s= datetime.datetime.strptime(datestr, "%a %b %d %H:%M:%S %Y %z").timestamp()
                time = str(t)
                date = str(d)
                timestamp = str(s)

                correctcommit = False

            elif idx == dateline + 2:
                comment = logline.strip()
                if comment == "daily helm tracking":
                    correctcommit = True

            elif correctcommit:
                if logline.startswith(" charts/"+self.filename):
                    print("charts/" + self.filename)

                    change = {}
                    change["CommitID"] = commit
                    change["Date"]=date
                    change["Time"]=time
                    change["TimeStamp"]=timestamp
                    change["filename"]=logline.split("charts/")[-1].split(".tgz")[0]+".tgz"

                    version = "No valid Versioning"
                    try:
                        # print(re.split(r"(\d+\.)(\d+\.)(\d)",post.split("/")[-1]))
                        pre, major, minor, build, post = re.split(r"(\d+\.)(\d+\.)(\d)", logline)
                        version = major+minor+build
                    except:
                        version = logline.split("/chats")[-1].split(".tgz")[0]
                        print(version)
                        print(" No Version NUmber")
                    change["Version"] = version
                    preBytes = logline.split("Bin ")[-1].split(" -> ")[0]
                    postBytes = logline.split("Bin ")[-1].split(" -> ")[-1].split(" bytes")[0]
                    change["preBytes"] = preBytes
                    change["postBytes"] = postBytes
                    if postBytes != "0":
                        self.fileHistory.append(change)

        print(self.fileHistory)

    def checkDiff(self):
        self.extractHistory()
        print(self.fileHistory)
        commits = []
        files = []
        timestamps = []
        for changes in sorted(self.fileHistory, key= lambda k: k["TimeStamp"]):
            commitID = changes["CommitID"]
            print(commitID)
            commits.append(commitID)
            timestamps.append(changes["TimeStamp"])
            files.append("charts/"+changes["filename"])
        print(commits)
        for i in range(len(commits)-1):
            self.dateOfChange = timestamps[i+1]
            self.checkout(commits[i], files[i],commits[i+1],files[i+1])
        print(self.keywordDict)
        return self.keywordDict
        #TODO: print to file


    def getTGZs(self):
        print(self.trackingdir)
        allfiles = [f for f in os.listdir(self.trackingdir) if os.path.isfile(os.path.join(self.trackingdir, f))]
        filesToTrack = []
        jsondict = {}
        jsondict["files"]=[]
        for filename in allfiles:
            filemodule = re.split(r"(\-)(\d+\.)(\d+\.)(\d)", filename)[0]
            if (filename.endswith("tgz") and filemodule not in filesToTrack):
                filesToTrack.append(filemodule)
                print(filemodule)
                fc = FileChanges(self.trackingdir, self.tempStoragePath, filemodule)
                resdic= fc.checkDiff()
                jsondict["files"].append(resdic)

        print(jsondict)
        with open(os.path.join(sys.path[0],"resultjson.json"),"w") as jf:
            print("pre")
            json.dump(jsondict,jf)
            print("post")



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Syntax: {} <command> [<command-args>...]".format(sys.argv[0]), file=sys.stderr)
        print("Commands: command1", file=sys.stderr)
        # Todo: Add more command Options
        sys.exit(1)
    command = sys.argv[1]

    if command == "commit":
        if len(sys.argv) != 4:
            print("Syntax: {} tgz <tempStoragePath> <commitId1> <commitId2>".format(sys.argv[0]), file=sys.stderr)
            sys.exit(1)
        else:
            tempStoragePath = sys.argv[1]
            commitId1 = sys.argv[2]
            commitId2 = sys.argv[3]
            print("running tgz with "+tempStoragePath+", "+trackingdir+", "+commitId+".")

    if command == "file":
        print(len(sys.argv))
        if len(sys.argv) != 5:
            print("Syntax: {} file <trackingdir> <tempStoragePath> <filename>".format(sys.argv[0]), file=sys.stderr)
            sys.exit(1)
        else:
            trackingdir = sys.argv[2]
            tempStoragePath = sys.argv[3]
            filename = sys.argv[4]
            print("running 'file' with "+trackingdir+", "+tempStoragePath+", "+filename+".")
            fc = FileChanges(trackingdir,tempStoragePath, filename)
            fc.checkDiff()

    if command == "repo":
        print(len(sys.argv))
        if len(sys.argv) != 4:
            print("Syntax: {} repo <trackingdir> <tempStoragePath>".format(sys.argv[0]), file=sys.stderr)
            sys.exit(1)
        else:
            trackingdir = sys.argv[2]
            tempStoragePath = sys.argv[3]
            print("running 'file' with "+trackingdir+", "+tempStoragePath+".")
            fc = FileChanges(trackingdir,tempStoragePath)
            fc.getTGZs()
    else:
        print("Unknown command.", file=sys.stderr)
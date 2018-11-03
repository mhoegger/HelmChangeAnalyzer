import subprocess
import os
import sys
import datetime
import operator
import pandas as pd
import glob
import json
import re

class FileChanges:
    def __init__(self, trackingdir, tempStoragePath, filename=None):
        self.trackingdir = trackingdir
        self.tempStoragePath = tempStoragePath
        self.filename = filename
        self.fileHistory = []

    def unique_getlog(self):
        origdir = os.getcwd()
        os.chdir(self.trackingdir)

        cmd = "COLUMNS=200 git log --stat"

        r = subprocess.run(f"{cmd} --reverse", shell=True, stdout=subprocess.PIPE)

        log = r.stdout.decode("utf-8")
        print("-----LOG END-----")
        os.chdir(origdir)
        return str(log)


    def checkout(self,id1, file1, id2, file2):
        origdir = os.getcwd()
        os.chdir(self.trackingdir)
        try:
            os.mkdir(self.tempStoragePath+"a/")
        except:
            print("Dir exists")
        cmd = "COLUMNS=200 git --work-tree="+self.tempStoragePath+"a checkout "+id1+ " -- "+file1
        print(cmd)
        r = subprocess.run(f"{cmd}", shell=True, stdout=subprocess.PIPE)
        cmd2= "tar -xvzf "+self.tempStoragePath+"a/"+file1+" -C "+self.tempStoragePath+"a"
        r = subprocess.run(f"{cmd2}", shell=True, stdout=subprocess.PIPE)

        try:
            os.mkdir(self.tempStoragePath+"b/")
        except:
            print("Dir exists")


        cmd = "COLUMNS=200 git --work-tree="+self.tempStoragePath+"b checkout "+id2+ " -- "+file2
        print(cmd)
        r = subprocess.run(f"{cmd}", shell=True, stdout=subprocess.PIPE)
        cmd2= "tar -xvzf "+self.tempStoragePath+"b/"+file2+" -C "+self.tempStoragePath+"b"
        r = subprocess.run(f"{cmd2}", shell=True, stdout=subprocess.PIPE)
        self.runDiff()


    def runDiff(self):
        origdir = os.getcwd()
        os.chdir(self.trackingdir)

        findACmd = "find "+self.tempStoragePath+"a/ -name Chart.yaml"
        pathToA = str(subprocess.run(f"{findACmd}", shell=True, stdout=subprocess.PIPE).stdout.decode("utf-8")).split("\n")[0]
        print(str(pathToA))
        findBCmd = "find "+self.tempStoragePath+"b/ -name Chart.yaml"
        pathToB = str(subprocess.run(f"{findBCmd}", shell=True, stdout=subprocess.PIPE).stdout.decode("utf-8")).split("\n")[0]
        print(pathToB)

        cmd = "diff "+str(pathToA)+" "+str(pathToB)
        print(cmd)
        response = subprocess.run(f"{cmd}", shell=True, stdout=subprocess.PIPE).stdout.decode("utf-8")
        print(str(response))

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
                date = str(d)
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
                    version = "No valid Versioning"
                    try:
                        # print(re.split(r"(\d+\.)(\d+\.)(\d)",post.split("/")[-1]))
                        pre, major, minor, build, post = re.split(r"(\d+\.)(\d+\.)(\d)", logline)
                        version = major+minor+build
                    except:
                        print("No Version NUmber")
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
        for changes in self.fileHistory:
            commitID = changes["CommitID"]
            print(commitID)
            commits.append(commitID)
            files.append("charts/"+self.filename+"-"+changes["Version"]+".tgz")

        self.checkout(commits[0], files[0],commits[-1],files[-1])






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


    else:
        print("Unknown command.", file=sys.stderr)
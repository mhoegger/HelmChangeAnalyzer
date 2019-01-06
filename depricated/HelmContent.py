import subprocess
import os
import sys
import datetime
import operator
import pandas as pd
import glob
import json
import re

class Changelogs:
    def __init__(self, trackingdir=None, startingpoint=None):
        self.trackingdir = trackingdir
        self.startingpoint = startingpoint

    def assign_type_Of_change(self, logline, type, filedict, files,date,sources):
        if filedict:
            files.append(filedict)
        filedict = {}  # reset
        post = logline.split("+++ b/")[-1]
        # filedict["filePath"] = post
        try:
            # print(re.split(r"(\d+\.)(\d+\.)(\d)",post.split("/")[-1]))
            name, n1, n2, n3, end = re.split(r"(\d+\.)(\d+\.)(\d)", post.split("/")[-1])
        except:
            name = post.split("/")[-1]
            n1, n2, n3 = "","",""
            print("No Version NUmber")
            # print(files)
        version = n1 + n2 + n3

        if (len(list(filter(lambda file: file["fileName"] == name, files[0:]))) > 0):
            # file already in dict
            foundFile = list(filter(lambda file: file["fileName"] == name, files[0:]))[0]
            change = {}
            if not version in foundFile["Versions"]:
                # Version Change
                change["Type"] = "File-"+type
                change["NewVersion"] = True
                try:
                    foundFile["Versions"].append(n1 + n2 + n3)
                except:
                    print("No Version NUmber")
            else:
                change["Type"] = "File-"+type
                change["NewVersion"] = False

            change["Version"] = version
            change["Path"]= post
            change["Date"] = date
            change["Sources"] = sources
            foundFile["Changes"].append(change)
            for source in sources:
                if not source in foundFile["AllSources"]:
                    foundFile["AllSources"].append(source)
                if change["Type"] == "File-Remove":
                    if source in foundFile["AllSources"]:
                        foundFile["AllSources"].remove(source)




        else:
            filedict["fileName"] = name
            filedict["Changes"] = []
            filedict["Versions"] = []
            filedict["AllSources"] = sources
            change = {}
            change["Date"] = date
            change["Type"] = "File-Creation"
            change["Version"] = version
            change["Path"]= post
            change["Sources"] = sources
            change["NewVersion"] = True

            filedict["Changes"].append(change)
            try:
                filedict["Versions"].append(n1 + n2 + n3)
            except:
                print("No Version NUmber")

        # filedict["fileType"] = post.split(".")[-1]
        return filedict, files
        # filedict[name]["changes"] = date
    def parse_fileSources(self, log):
        print(">>>>>in parse")
        files = []
        filedict={}
        date = None
        comment = None
        dateline = -5
        changes = {}
        sources = []
        correctcommit = False
        predate = None
        newfileline = 0
        postline = 0
        counter = 0
        start = False
        deflogline = 0
        typeString = ""

        for idx, logline in enumerate(log.split("\n")):
            if logline.startswith("Date:"):
                dateline = idx
                datestr = ":".join(logline.split(":")[1:]).strip()
                d = datetime.datetime.strptime(datestr, "%a %b %d %H:%M:%S %Y %z").date()
                date = str(d)
                correctcommit = False
                predate = d - datetime.timedelta(days=1)

            elif idx == dateline + 2:
                comment = logline.strip()
                if comment == "daily helm tracking":
                    correctcommit = True


            elif correctcommit:
                if logline.startswith("--- /dev/null"):
                    # new filecreated
                    newfileline = idx # line below adds file
                elif (logline.startswith("+++ b/") and idx==newfileline+1):
                    # new file created since line above contained /dev/nul
                    deflogline = logline
                    typeString = "Creation"
                    sources = []
                elif logline.startswith("+++ b/"):
                    # file changed
                    deflogline = logline
                    typeString = "Update"
                elif logline.startswith("--- a/"):
                    # file remove if line bolw contains /dev/null
                    prevlogline = logline
                    postline = idx
                elif (idx == postline+1 and logline.startswith("+++ /dev/null")):
                    #delete file
                    deflogline = prevlogline
                    typeString = "Removal"
                elif logline.startswith("+# Source: "):
                    start = True
                    sources.append(logline.split("+# Source: ")[-1])
                elif logline.startswith("-# Source: "):
                    start = True
                    sources.append(logline.split("-# Source: ")[-1])
                elif logline.startswith("+") or logline.startswith("-"):
                    if not logline.startswith("+++") or logline.startswith("---"):
                        start = True
                elif logline.startswith("diff") and start:
                    #newdiff recognized
                    filedict, files = self.assign_type_Of_change(deflogline, typeString, filedict, files, date, sources)
                    typeString = ""
                    start = False
                    deflogline = 1
                    sources=[]
                else:
                    newfile = False
                    #filedict[""]
                    #sources = []
        # first close source list of previous file
        #filedict["fileSources"] = sources
        sources = []  # reset
        # first save previous file in filelist
        #files.append(filedict)
        print("------->"+str(counter))
        return files

    def unique_getlog(self):
        origdir = os.getcwd()
        os.chdir(self.trackingdir)

        cmd = "COLUMNS=200 git log -p"

        #if self.startingpoint:
         #   cmd = f"{cmd} {self.startingpoint}..HEAD"

        r = subprocess.run(f"{cmd} --reverse", shell=True, stdout=subprocess.PIPE)

        log = r.stdout.decode("utf-8")
        print("-----LOG END-----")
        os.chdir(origdir)
        return str(log)

    def findMetrics(self):
        filename = "foundMetrics.json"
        with open(filename, "w") as f:
            print(">>>>>in file")
            dict = {}
            log = self.unique_getlog()
            print(log)

            print(str(log))
            files = self.parse_fileSources(log)
            dict["FileSource"] = files
            print(">>>>>after file")

            print(dict)
            json.dump(files, f)




if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Syntax: {} <command> [<command-args>...]".format(sys.argv[0]), file=sys.stderr)
        print("Commands: command1", file=sys.stderr)
        # Todo: Add more command Options
        sys.exit(1)
    command = sys.argv[1]

    if command == "command1":
        if len(sys.argv) not in (3, 4):
            print("Syntax: {} tracking <trackingdir> [<startingpoint>]".format(sys.argv[0]), file=sys.stderr)
            sys.exit(1)
        startingpoint = None
        if len(sys.argv) == 4:
            startingpoint = sys.argv[3]
        cr = Changelogs(sys.argv[2], startingpoint)
        cr.findMetrics()

    else:
        print("Unknown command.", file=sys.stderr)
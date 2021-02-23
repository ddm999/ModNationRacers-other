#!/usr/bin/env python3
import argparse, shutil, re, os
headercomment = """
    Python script that copies MNR UCC.

    Provide a list of content names as they are shown in-game, and this script will copy those from one directory to another.
    At the end a list of warnings are provided for any files with matching names, you'll have to figure these out yourself.
"""
# let the script run with no args (disabled by default to prevent running while trying to access help)
ALLOW_EMPTY_RUN = False

# default values, changed by args
DEV = False
TEST = 0
folder_src = "ALL_VEHICLES"
folder_dest = "VEHICLE"
filename = "VEHICLE.txt"

# argparse
parser = argparse.ArgumentParser(description=headercomment)
parser.add_argument('-s','--src',default=folder_src,help="source folder (ie ALL_VEHICLES)")
parser.add_argument('-d','--dest',default=folder_dest,help="destination folder (ie VEHICLE)")
if ALLOW_EMPTY_RUN:
    parser.add_argument('-f','--file',default=filename,help="file containing item names, one per line (ie VEHICLE.txt)")
else:
    parser.add_argument('-f','--file',required=True,help="file containing item names, one per line (ie VEHICLE.txt)")
parser.add_argument('--dev',action='store_true',help="run in developer mode: ie. print useless information")
parser.add_argument('--test',choices=[0,1,2],type=int,help="test mode: set to 1 to print instead of moving an item / set to 2 to print instead of moving each file")

# helper func to move a file (or pretend to with TEST)
def move(f: str):
    if TEST >= 2:
        print("TEST move '"+folder_src+"/"+f+"' to '"+folder_dest+"/"+f+"'")
    else:
        shutil.move(folder_src+"/"+f,folder_dest+"/"+f)

def __main__():
    global DEV, TEST, folder_src, folder_dest, filename
    # global state lol

    warnings = []

    inputs = vars(parser.parse_args())
    DEV = inputs["dev"] or DEV
    TEST = inputs["test"] or TEST
    folder_src = inputs["src"] or folder_src
    folder_dest = inputs["dest"] or folder_dest
    filename = inputs["file"] or filename

    if DEV:
        print("source folder: "+folder_src)
        print("destination folder: "+folder_dest)
        print("file: "+filename)

    listing = []
    with open(filename, "r") as f:
        listing = f.readlines()

    sourcefiles = os.listdir(folder_src)
    sourcefiles_mini = []
    for f in sourcefiles:
        if f.endswith(".CMD"):
            sourcefiles_mini.append(f)

    count=0
    foundnames = []
    for f in listing:
        if f == "\n":
            # skip over blank lines
            continue
        wantedfile = "_"+re.sub('[^A-Za-z0-9_]', '', f.strip("\n ")).upper()+".CMD"
        if DEV:
            print("DEV  wantedfile: "+wantedfile)

        found = False
        eol = False
        i=0
        sourcefile=""
        while not eol:
            sourcefile = sourcefiles_mini[i]
            if sourcefile.find(wantedfile) != -1:
                if DEV:
                    print("DEV  match: "+sourcefile)
                if found == True:
                    if DEV:
                        print("DEV  multiple match: "+wantedfile)
                    warnings.append("Another item matches the input '"+f.strip("\n ")+"'.")
                else:
                    found = True
                foundnames.append(sourcefile)
            i+=1
            if i>=len(sourcefiles_mini):
                eol = True

    for file in foundnames:
        count+=1
        if TEST == 1:
            print("TEST move '"+file[:-4]+"'")
        else:
            move(file)
            move(file[:-4]+".PNG")
            move(file[:-4]+".SAV")
            move(file[:-4]+"_SMALL.PNG")

    print("\nNOTE wanted:",len(listing),"/ found:",count)
    if len(warnings) > 0:
        print("\n======== WARNINGS ========")
    for w in warnings:
        print(" "+w)

__main__()
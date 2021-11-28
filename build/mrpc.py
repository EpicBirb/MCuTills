'''
EpicBirb/mrpc Repository is licensed under:

                    GNU GENERAL PUBLIC LICENSE
                       Version 2, June 1991

 Copyright (C) 1989, 1991 Free Software Foundation, Inc.,
 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

Permissions
 - Commercial Use
 - Modification
 - Distrbution
 - Private Use

Conditions:
 - License and copyright notice
 - State changes
 - Disclose Source
 - Same license
'''

#import classes
import os,time,json,shutil,atexit,webbrowser
import zipfile as zp
from collections import Counter
import pathlib as pl

#tries to do all of these line, go to bottom of the script to find the except: exception
try:
  #var
  temp_c = 0 #temp var
  pack = [] #pack logging
  checks = [] #logs files from ./<packname>/assets/minecraft/models/items/
  debugc = "" #var to check if debug.txt is valid

  #debug checker
  try:
    debug1 = open("debug.txt")
    debug = debug1.read() 
    debug1.close()
    if debug.lower() == "true":
      debugc = 1
      if os.path.exists("log.txt"):
        zpn = zp.ZipFile("log.zip", "w", zp.ZIP_DEFLATED)
        zpn.write("log.txt")
        zpn.close()
        f = open("log.txt", "w")
        f.write("-----------[Debug Log]-----------\n")
        f.write("\\\\\ What errors can I find today?\n \n")
        f.close()
      else:
        f = open("log.txt", "a")
        f.write("-----------[Debug Log]-----------\n")
        f.write("\\\\\ What errors can I find today?\n \n")
        f.close()
    else:
      pass
  except FileNotFoundError:
    pass

  #function
  def exit_handler():
    global debugc
    if debugc == 1:
      f = open("log.txt", "a")
      f.write("\n-----------[End of log]-----------")
      f.close()
    else:
      pass
  
  #exit funciton
  def exitp():
    print("Exiting...")
    debuglog("[OK]", "complete, exiting")
    time.sleep(2)
    exit(1)

  #logs
  def debuglog(typeoferror, append):
    global debugc
    if debugc == 1 and os.path.exists("log.txt") and str(append) == "":
      f = open("log.txt", "a")
      f.write("\n")
      f.write("[ERROR] error not specified (debuglog function)")
    else:
      f = open("log.txt", "a")
      f.write("\n")
      f.write(str(typeoferror) + " " + str(append))
      f.close()
  
  #clear console
  def clearconsole():
    print("\n" * 100)

  #introduction
  def intro():
    print("==================================================")
    print("-[MRPC]-")
    print("A python program to combine resource packs that")
    print("have conflicts with each other in Minecraft.")
    print("Most commonly, resource packs for data packs.")
    print("==================================================")

  #pack.mcmeta writer
  def packmc(ver, pathtowrite):
    packmcmeta = open(pathtowrite, "w+")
    jsonwrite = {"pack": {"pack_format": int(ver),"description": "MRPC: github.com/EpicBirb/mrpc"}}
    packmcmeta.write(json.dumps(jsonwrite, indent=2, sort_keys=True))
    packmcmeta.close()

  def mainask():
    print("Select an option:")
    print("   [1] Start Combining")
    print("   [2] View Repository on GitHub")
    print("   [3] Quit")

  #atexit handler
  atexit.register(exit_handler)

  while True:
    #intro
    intro()
    print()

    #ask to do
    mainask()
    confirm5 = input("> ")
    while True:
      if confirm5 == "1":
        break
      elif confirm5 == "2":
        webbrowser.open("https://github.com/EpicBirb/mrpc")
        clearconsole()
        intro()
      elif confirm5 == "3":
        print("Thanks for using this program!")
        time.sleep(2)
        exit(1)
      else:
        clearconsole()
        mainask()
        confirm5 = input("Invalid Option, type it again > ")

    #warn
    print()
    print("Before we begin, you must have the resource packs in the same directory as this program (The resource packs must not be in zip files)")
    print()

    #check for resource packs
    print()
    for i in os.listdir("."):
      try:
        for o in os.listdir("./" + i):
          if o.lower() == "pack.mcmeta":
            pack.append(i)
            temp_c = temp_c + 1
            debuglog("[OK]", "folder " + i + " is a recource pack (pack.mcmeta)")
          else:
            pass
      except NotADirectoryError:
        pass

    #list all resource packs in current durectory, if not, it will exit
    if temp_c >= 2:
      print("List of resource packs in current directory:")
      for p in pack:
        print("   " + p)
    elif temp_c == 1:
      print("There is only 1 resource pack in the current directory. (The program scans for pack.mcmeta in the folders)")
      print()
      print("Exiting..")
      debuglog("[ERROR]", "there are only 1 resource pack in the current folder")
      time.sleep(3)
      exit(1)
    else:
      print("There are no resource packs in the current folder, are you trying to test me?")
      debuglog("[ERROR]", "there are no resource packs in the current folder")
      time.sleep(3)
      exit(1)
    print()

    #asks if these are the packs to be merged
    print()
    confirm = input("Are these the resource packs you need to be merged (Yes or No)? ")
    while True:
      if confirm.lower() == "yes":
        break
      elif confirm.lower() == "no":
        print()
        print("Ok, run the program again when you only see the folders you need!")
        time.sleep(5)
        exit(1)
      else:
        print()
        confirm = input("Yes or No? ")

    #list all files in /assets/minecraft/models/item/ cuz it records the json files inside of it
    for i in pack:
      for j in os.listdir("./" + i + "/assets/minecraft/models/item/"):
        checks.append(j)
        debuglog("[OK]", "logging file " + j)

    #check for duplicate files
    checkfordups = [key for key in Counter(checks).keys() if Counter(checks)[key]>1]
      
    #makes the temp folder, if exist, print error
    try:
      os.mkdir("./temp/")
      debuglog("[OK]", "temp folder created")
    except FileExistsError:
      print("The program is trying to make a folder in the current folder, but can't do so. This may be cuase by already having the folder \"temp\" in the directory or becuase the program forgot to clear it up. If you are seeing this, please delete the folder.")
      debuglog("[ERROR]", "folder \"temp\" is already in the currnet folder")
      time.sleep(15)
      exit(1)

    #warn
    print()
    print()
    confirm3 = input("Before we continue, the folder you need to be merged with must be edited by the program, if ths pack is new and hasn't been backed up, I advise you to do it. Don't blame me if this happens. DO YOU WISH TO CONTINUE? (Yes or No): ")

    #input checker
    while True:
      if confirm3.lower() == "yes":
        break
      elif confirm3.lower() == "no":
        print("Canceling Operation")
        try:
          shutil.rmtree("./temp")
          debuglog("[WARN]", "removing \"temp\" folder (shutil.rmtree)")
          time.sleep(5)
          exit(1)
        except KeyboardInterrupt:
          print("Alright wise guy, Ill close")
          debuglog("[WARN]", "force exit (crl + c)")
          time.sleep(1)
          exit(1)
      else:
        print()
        confirm3 = input("Yes or No? ")

    #make temp strorage
    os.mkdir("./temp/json/")
    os.mkdir("./temp/splash/")
    os.mkdir("./temp/temp/")
    os.mkdir("./temp/temp/temp")
    debuglog("[OK]", "created folder \"temp/temp/\", \"temp\", \"json\", \"splash\", in \"temp\"")

    #clear temp_c
    temp_c = 0

    #check for splash
    try:
      for i in pack:
        for o in os.listdir("./" + i + "/assets/minecraft/texts/"):
          temp_c = temp_c + 1
          debuglog("[OK]", "counting " + o + " as a splash file")
    except FileNotFoundError:
      pass

    #splash merge
    try:
      if temp_c >= 2:
        for i in pack:
          for o in os.listdir("./" + i + "/assets/minecraft/texts/"):
            for p in os.listdir("./temp/splash/"):
              if p == o:
                debuglog("[OK]", "opening " + o)
                f = open(os.path.join("./" + i + "/assets/minecraft/texts/" + o))

                f1 = open(os.path.join("./temp/splash/" + o))
                container2 = f1.read()
                  
                f.write("\n")
                f.write(container2)

                f.close()
                f1.close()
              else:
                shutil.copy("./" + i + "/assets/minecraft/texts/", "./temp/splash/")
                debuglog("[OK]", "copying " + o + " to " + "/temp/splash/")
      else:
        pass
    except:
      debuglog("[WARN]", "passing file " + p)

    #reset container2
    container2 = ""

    #merge model json
    for o in pack:
      for i, k in enumerate(checkfordups):
        for p in os.listdir("./" + o + "/assets/minecraft/models/item/"):
          if p == checkfordups[i]:
            debuglog("[OK]", "found dupe file " + p)
            for l in os.listdir("./temp/temp/"):
              debuglog("[OK]", "file in ./temp/json " + l)
              #checks if json file is in temp/json
              if l == p:
                #open json in temp, and assets. appens then clear
                with open("./temp/temp/" + p, "r") as f:
                  debuglog("[OK]", "opening " + p + " in temp")
                  container = json.load(f)
                  with open("./" + o + "/assets/minecraft/models/item/" + p, "r") as f1:
                    debuglog("[OK]", "opening " + p + " in pack folder")
                    container2 = json.load(f1)
                    debuglog("[OK]", "appending data...")
                    for q in container2["overrides"]:
                      container["overrides"].append(q)
                  with open(os.path.join("./temp/temp/" + p), "w+") as t:
                    t.write(json.dumps(container, indent=2, sort_keys=True))
                  os.remove("./" + o + "/assets/minecraft/models/item/" + p)
                debuglog("[OK]", "finished writing file " + p)
              #else: move file
              else:
                try:
                  shutil.move("./" + o + "/assets/minecraft/models/item/" + p, "./temp/temp/")
                  debuglog("[OK]", "copying " + p + " to /temp/temp/")
                except:
                  debuglog("[WARN]", "could not find file " + p + ", skipping")
          else:
            pass

    #removes file to prepare for transfer
    for i in pack:
      try:
        os.remove("./" + i + "/pack.mcmeta")
        os.remove("./" + i + "/pack.png")
        shutil.rmtree("./temp/temp/temp/")
        debuglog("[OK]", "removing \"pack.mcmeta\" and \"pack.png\" from " + i)
      except FileNotFoundError:
        pass

    #move files in /temp/temp/ to /tmp/json/
    for i in os.listdir("./temp/temp"):
      shutil.move("./temp/temp/" + i, "./temp/json/")
      debuglog("[OK]", "moved " + i + " from /temp/temp/ to /temp/json/")

    #make temp path for new pack  
    os.mkdir("./temp/pack/")
    debuglog("[OK]", "created folder /temp/pack/")

    #create dir and copy
    for i in pack:
      debuglog("[OK]", "in " + i)
      for s in os.listdir(i):
        debuglog("[OK]", "in " + s + " in " + i)
        for subdir, dirs, file in os.walk(os.fspath(pl.PurePath(os.path.join(i, s)))):
          debuglog("[OK]", "atttempting to create folder...")
          try:
            os.mkdir("./temp/pack" + subdir.replace(i, ""))
            debuglog("[OK]", "created folder " + subdir + " in ./temp/pack/")
          except FileExistsError:
            debuglog("[WARN]", "file/folder exists already, skipping: " + os.fspath(pl.PurePath(os.path.join("./temp/pack/", subdir))))
        for subdir, dirs, file in os.walk(os.fspath(pl.PurePath(os.path.join(i, s)))):
          for files in file:
            shutil.move(os.path.join(subdir, files), "./temp/pack" + subdir.replace(i, ""))

    #ask for pack version that user will be using the pack on
    print()
    print("What version are you planning to use the resource pack on?")
    print("   [1]  1.6.1 - 1.8.9")
    print("   [2]  1.9 - 1.10.2")
    print("   [3]  1.11 - 1.12.2")
    print("   [4]  1.13  - 1.14.4")
    print("   [5]  1.15 - 1.16.1")
    print("   [6]  1.16.2 - 1.16.5")
    print("   [7]  1.17.x")
    print("   [8]  1.18 snapshots")
    version = input("> ")
    while True:
      try:
        if int(version) <= 8 and int(version) != 0:
          packmc(int(version), "./temp/pack/pack.mcmeta")
          break
        else:
          version = input("Invalid option, type it again > ")
      except Exception as error:
        debuglog("[FATAL ERROR]", error)
        exit(1)

    #move json files to temp pack
    for i in os.listdir("./temp/json/"):
      shutil.move("./temp/json/" + i, "./temp/pack/assets/minecraft/models/item/")
      debuglog("[OK]", "moving " + i + " to pack in temp")

    #move pack to current folder and remove temp
    shutil.move("./temp/pack", ".")
    shutil.rmtree("./temp")
    debuglog("[OK]", "moved temp pack into main dir and removed temp folder")

    #done
    print()
    print("Merge Complete")
    print()

    #ask to go back to main screen
    while True:
      print()
      print("Want to go back to main screen (yes or no?)? ")
      confirm7 = input("> ")
      if confirm7.lower() == "yes":
        clearconsole()
        break
      elif confirm7.lower() == "no":
        print()
        exitp()
      else:
        print()
        confirm = input("Yes or No? ")

#logs error and kills the program
except Exception as error:
    debuglog("[FATAL ERROR]", error)
    exit(1)
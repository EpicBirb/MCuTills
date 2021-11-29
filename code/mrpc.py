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
        with zp.ZipFile("log.zip", "w", zp.ZIP_DEFLATED) as zpn:
          zpn.write("log.txt")
        with open("log.txt", "w") as f:
          f.write("-----------[Debug Log]-----------\n \\\\\ What errors can I find today?\n\n")
      else:
        with open("log.txt", "a") as f:
          f.write("-----------[Debug Log]-----------\n \\\\\ What errors can I find today?\n\n")
    else:
      pass
  except FileNotFoundError:
    pass

  #function
  def exit_handler():
    global debugc
    if debugc == 1:
      with open("log.txt", "a") as f:
        f.write("\n-----------[End of log]-----------")
  
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
      with open("log.txt", "a") as f:
        f.write("\n[ERROR] error not specified (debuglog function)")
    elif debugc == 1 and os.path.exists("log.txt"):
      with open("log.txt", "a") as f:
        f.write(f"\n{str(typeoferror)} {str(append)}")
  
  #clear console
  def clearconsole():
    print("\n" * 100)

  #introduction
  def intro():
    print("==================================================\n-[MRPC v1.0.0]-\nA python program to combine resource packs that\nhave conflicts with each other in Minecraft.\nMost commonly, resource packs for data packs.\n==================================================")

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
    for i in os.listdir("."):
      try:
        for o in os.listdir(f"./{i}"):
          if o.lower() == "pack.mcmeta":
            pack.append(i)
            temp_c = temp_c + 1
            debuglog("[OK]", f"folder {i} is a recource pack (pack.mcmeta)")
      except NotADirectoryError:
        pass

    #list all resource packs in current durectory, if not, it will exit
    if temp_c >= 2:
      print("List of resource packs in current directory:")
      for p in pack:
        print(f"   {p}")
    else:
      print("There is 1 or no resource pack in the current directory. (The program scans for pack.mcmeta in the folders)")
      print("Exiting..")
      debuglog("[ERROR]", "there are 1 or no resource pack in the current folder")
      time.sleep(3)
      exit(1)
    print()

    #asks if these are the packs to be merged
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
      for j in os.listdir(f"./{i}/assets/minecraft/models/item/"):
        checks.append(j)
        debuglog("[OK]", f"logging file {j}")

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
    confirm3 = input("Before we continue, the folder you need to be merged with must be edited by the program, if ths pack is new and hasn't been backed up, I advise you to do it. Don't blame me if this happens. DO YOU WISH TO CONTINUE? (Yes or No): ")

    #input checker
    while True:
      if confirm3.lower() == "yes":
        break
      elif confirm3.lower() == "no":
        print("Canceling Operation")
        try:
          shutil.rmtree("./temp")
          debuglog("[OK]", "removing \"temp\" folder (shutil.rmtree)")
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
        for o in os.listdir(f"./{i}/assets/minecraft/texts/"):
          temp_c = temp_c + 1
          debuglog("[OK]", f"counting {o} as a splash file")
    except FileNotFoundError:
      pass

    #splash merge
    try:
      if temp_c >= 2:
        for i in pack:
          for o in os.listdir(f"./{i}/assets/minecraft/texts/"):
            for p in os.listdir("./temp/splash/"):
              if o != p:
                shutil.copy(f"./{i}/assets/minecraft/texts/{o}")
              else:
                debuglog("[OK]", f"opening {o}")
                with open(os.path.join(f"./{i}/assets/minecraft/texts/{o}")) as f:
                  with open(os.path.join(f"./temp/splash/{o}")) as f1:
                    f.write(f"\n{f1.read()}")
                  os.remove(f"./{i}/assets/minecraft/texts/{o}")
    except:
      debuglog("[WARN]", f"passing file {p}")

    #merge model json
    for o in pack:
      for i, k in enumerate(checkfordups):
        for p in os.listdir(f"./{o}/assets/minecraft/models/item/"):
          if p == checkfordups[i]:
            debuglog("[OK]", f"found dupe file {p}")
            for l in os.listdir("./temp/temp/"):
              debuglog("[OK]", f"file in ./temp/json {l}")
              #checks if json file is in temp/json
              if l == p:
                #open json in temp, and assets. appens then clear
                with open(f"./temp/temp/{p}", "r") as f:
                  debuglog("[OK]", f"opening {p} in temp")
                  container = json.load(f)
                  with open(f"./{o}/assets/minecraft/models/item/{p}", "r") as f1:
                    debuglog("[OK]",f"opening {p} in pack folder")
                    container2 = json.load(f1)
                    debuglog("[OK]", "appending data...")
                    for q in container2["overrides"]:
                      container["overrides"].append(q)
                  with open(os.path.join(f"./temp/temp/{p}"), "w+") as t:
                    t.write(json.dumps(container, indent=2, sort_keys=True))
                  os.remove(f"./{o}/assets/minecraft/models/item/{p}")
                debuglog("[OK]", f"finished writing file {p}")
              #else: move file
              else:
                try:
                  shutil.move(f"./{o}/assets/minecraft/models/item/{p}", "./temp/temp/")
                  debuglog("[OK]", f"copying {p} to /temp/temp/")
                except:
                  debuglog("[WARN]", f"could not find file {p}, skipping")

    #removes file to prepare for transfer
    for i in pack:
      try:
        os.remove(f"./{i}/pack.mcmeta")
        os.remove(f"./{i}/pack.png")
        shutil.rmtree("./temp/temp/temp/")
        debuglog("[OK]", f"removing \"pack.mcmeta\" and \"pack.png\" from {i}")
      except FileNotFoundError:
        pass

    #move files in /temp/temp/ to /tmp/json/
    for i in os.listdir("./temp/temp"):
      shutil.move(f"./temp/temp/{i}", "./temp/json/")
      debuglog("[OK]", f"moved {i} from /temp/temp/ to /temp/json/")

    #make temp path for new pack  
    os.mkdir("./temp/pack/")
    debuglog("[OK]", "created folder /temp/pack/")

    #create dir and copy
    for i in pack:
      debuglog("[OK]", f"in {i}")
      for s in os.listdir(i):
        debuglog("[OK]", f"in {s} in {i}")
        for subdir, dirs, file in os.walk(os.fspath(pl.PurePath(os.path.join(i, s)))):
          debuglog("[OK]", "atttempting to create folder...")
          try:
            os.mkdir("./temp/pack" + subdir.replace(i, ""))
            debuglog("[OK]", f"created folder {subdir} in ./temp/pack/")
          except FileExistsError:
            debuglog("[WARN]", "file/folder exists already, skipping: ./temp/pack/" + subdir.replace(i, ""))
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
      if int(version) <= 8 and int(version) != 0:
        packmc(int(version), "./temp/pack/pack.mcmeta")
        break
      else:
        version = input("Invalid option, type it again > ")

    #move json files to temp pack
    for i in os.listdir("./temp/json/"):
      shutil.move(f"./temp/json/{i}", "./temp/pack/assets/minecraft/models/item/")
      debuglog("[OK]", f"moving {i} to pack in temp")

    #move pack to current folder and remove temp
    shutil.move("./temp/pack", ".")
    shutil.rmtree("./temp")
    debuglog("[OK]", "moved temp pack into main dir and removed temp folder")

    #remove pack orgin of pack
    try:
      for i in pack:
        shutil.rmtree(i)
        debuglog("[OK]", f"removed {i}")
    except:
      debuglog("[WARN]", "could not remove pack folder, skipping")

    #done
    print()
    print("Merge Complete")
    print()

    #ask to go back to main screen
    print("Want to go back to main screen (yes or no?)? ")
    confirm7 = input("> ")
    while True:
      if confirm7.lower() == "yes":
        clearconsole()
        break
      elif confirm7.lower() == "no":
        print()
        exitp()
      else:
        print()
        confirm7 = input("Yes or No? ")

#logs error and kills the program
except Exception as error:
    debuglog("[FATAL ERROR]", error)
    exit(1)
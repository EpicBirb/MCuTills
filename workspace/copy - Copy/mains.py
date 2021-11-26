import os,time,json,shutil,atexit
import zipfile as zp
from collections import Counter

try:
  #null
  confirm2 = ""
  confirm4 = ""

  #var
  temp_c = 0
  dirs = {}
  pack = []
  packup = []
  checks = []
  appendup = []
  jdit = []
  dup1 = ""
  container = ""
  container2 = ""
  copy = ""
  debugc = ""

  #debug checker
  try:
    debug1 = open("./debug.txt")
    debug = debug1.read()
    debug1.close()
    if debug.lower() == "true":
      debugc = 1
      if os.path.exists("./log.txt"):
        zpn = zp.ZipFile("log.zip", "w", zp.ZIP_DEFLATED)
        zpn.write("./log.txt")
        zpn.close()
        f = open("./log.txt", "w")
        f.close()
      else:
        f = open("./log.txt", "a")
        f.write("\n-----------[Debug Log]-----------\n")
        f.write("\\\\\ What errors can I find today?\n \n")
        f.close()
    else:
      pass
  except FileNotFoundError:
    pass

  #function
  def exit_handler():
    f = open("./log.txt", "a")
    f.write("\n-----------[End of log]-----------")
    f.close()

  def debuglog(typeoferror, append):
    global debugc
    if debugc == 1:
      if os.path.exists("./log.txt"):
        if str(append) == "":
          f = open("log.txt", "a")
          f.write("\n")
          f.write("[ERROR] error not specified (debuglog function)")
        else:
          f = open("log.txt", "a")
          f.write("\n")
          f.write(str(typeoferror) + " " + str(append))
      else:
        pass
    else:
      pass

  #atexit handler
  atexit.register(exit_handler)

  #intro
  print("==================================================")
  print("Welcome to JSONesource, a JSON combiner for minecraft \n resource packs that has a conflict with each other.")
  print("==================================================")

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
    if confirm.lower() == "yes" or confirm2.lower() == "yes":
      break
    elif confirm.lower() == "no" or confirm2.lower() == "no":
      print()
      print("Ok, run the program again when you only see the folders you need!")
      time.sleep(5)
      exit(1)
    else:
      print()
      confirm2 = input("Yes or No? ")

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
    if confirm3.lower() == "yes" or confirm4.lower() == "yes":
      break
    elif confirm3.lower() == "no" or confirm4.lower() == "no":
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
      confirm4 = input("Yes or No? ")

  #make temp strorage
  os.mkdir("./temp/json/")
  os.mkdir("./temp/splash/")
  os.mkdir("./temp/temp/")
  os.mkdir("./temp/temp/temp")
  debuglog("[OK]", "created folder \"temp/temp/\", \"temp\", \"json\", \"splash\", in \"temp\"")

  #temp_c reset
  temp_c = 0

  #splash merge
  try:
    for i in pack:
      for o in os.listdir("./" + i + "/assets/minecraft/texts/"):
        temp_c = temp_c + 1
        debuglog("[OK]", "counting " + o + " as a splash file")
  except FileNotFoundError:
    pass

  #checkfor more than 1 splash
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

  exit(1)

  #removes file to prepare for transfer
  for i in pack:
    try:
      os.remove("./" + i + "/pack.mcmeta")
      os.remove("./" + i + "/pack.png")
      shutil.rmtree("./temp/temp/temp/")
      debuglog("[OK]", "removing \"pack.mcmeta\" and \"pack.png\" from " + i)
    except FileNotFoundError:
      pass

  #make temp path for new pack  
  os.mkdir("./temp/pack/")
  debuglog("[OK]", "created folder /temp/pack/")

  #create dir and copy
  for i in pack:
    for o in os.listdir(i):
      for subdir, dirs, files in os.walk(o):
        os.mkdir(os.path.join("./temp/pack/", subdir))
        debuglog("[OK]", "creating directory " + os.path.join("/temp/pack/", subdir))
      for subdir, dirs, files in os.walk(o):
        for file in files:
          shutil.copy(os.path.join("./temp/pack/", subdir, file))
          debuglog("[OK]", "copying " + os.path.join(os.getcwd(), subdir, file) + " to pack")

  #move json files to temp pack
  for i in os.listdir("./temp/json/"):
    shutil.move("./temp/json/" + i, "./temp/pack/assets/minecraft/models/item/")
    debuglog("[OK]", "moving " + i + "to pack in temp")

  #move pack to current folder and remove temp
  shutil.move("./temp/pack", ".")
  shutil.rmtree("./temp")
  debuglog("[OK]", "moved temp pack into main dir and removed temp folder")

  #done
  print("Merge Complete")
  print("")
  print("Exiting...")
  debuglog("[OK]", "complete, exiting")
  time.sleep(2)
  exit(1)

except Exception as error:
    debuglog("[FATAL ERROR]", error)
    exit(1)
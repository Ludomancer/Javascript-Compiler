import sys
import argparse
import ConfigParser
import os
import fnmatch
import subprocess
import shutil
import zipfile


class confData:  
	username = ""
	password = ""
	domain = ""
	buildDir = None
	projectRoot = ""
	itemsToCopy = []
	debugItems = []
	debugInjectData = ""
	gameKey = None
	gameName = None
	injectDebug = None
	optimizeAssets = None
	isVerbose = None
	zipPath = None
	uploadSource = None
	uploadZip = None
	uploadOnly = None
	ftpTimeout = None
	extraWinScpCMds = None
	targetPath = ""
	updatingAssets = None
	releaseIndex = None

class bcolors:  
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def getTitle(text):
	return bcolors.HEADER + text + bcolors.ENDC
	
def getWarn(text):
	return bcolors.WARNING + text + bcolors.ENDC
	
def getSubTitle(text):
	return bcolors.BOLD + text + bcolors.ENDC
	
def getColorText(color, text):
	return color + text + bcolors.ENDC
	
def copyAllAssets(itemList, clear):
	print getTitle("Clearing: ") + confData.buildDir
	if(os.path.exists(confData.buildDir)):
		if clear == True:
			for root, dirs, files in os.walk(confData.buildDir):
				for f in files: os.unlink(os.path.join(root, f))
				for d in dirs: shutil.rmtree(os.path.join(root, d))
	else: os.mkdir(confData.buildDir)
	
	for item in itemList:
		itemData = item.split(":")
		sourceItem = os.path.join(os.getcwd(),confData.projectRoot, itemData[0])
	
		if(len(itemData) == 2): destItem = os.path.join(os.getcwd(),confData.buildDir, itemData[1])
		else: destItem = os.path.join(os.getcwd(),confData.buildDir, itemData[0])
	
		print getSubTitle("Copying: ") + sourceItem + getSubTitle(" -> ") + destItem
	
		if os.path.isdir(sourceItem): shutil.copytree(sourceItem, destItem)
		else: shutil.copyfile(sourceItem, destItem)
		
	print getColorText(bcolors.OKGREEN,"DONE!")
	return
	
def optimizeAssets():
	print getTitle("Optimizing Assets")
	compilerPath = os.path.join(os.getcwd(), "compiler.jar")
	pngOptPath = os.path.join(os.getcwd(), "pngquant.exe")
	jpgOptPat = os.path.join(os.getcwd(), "jpegtran.exe")
	DEVNULL = open(os.devnull, 'wb')
	for root, dirnames, filenames in os.walk(confData.buildDir):
		for extension in ['jpg', 'jpeg', 'png', 'js']:
			for filename in fnmatch.filter(filenames, '*.' + extension):
				print getSubTitle("Optimizing: ") + filename

				filename = os.path.join(os.getcwd(),root, filename)
				if (extension == 'jpg') or (extension == 'jpeg'):
					callString = "{1} -copy none -optimize -outfile {0} {0}".format(filename,jpgOptPat)
				if (extension == 'png'):
					callString = "{1} --force --verbose --ext .png --speed 1 --quality=45-85 {0}".format(filename,pngOptPath)
				if (extension == 'js'):
					callString = "java -jar {1} --js_output_file={0} {0}".format(filename,compilerPath)
				
				if confData.isVerbose: subprocess.call(callString)
				else: subprocess.call(callString, stdout=DEVNULL, stderr=subprocess.STDOUT)
	DEVNULL.close()
	print getColorText(bcolors.OKGREEN,"DONE!")
	return
	
def injectDebug(items,debugInjectData):
	print getTitle("Injecting Debug Files")
	
	for item in items:
		sourceItem = os.path.join(os.getcwd(),confData.projectRoot, item)
		destItem = os.path.join(os.getcwd(),confData.buildDir, item)
	
		print getSubTitle("Copying: ") + sourceItem + getSubTitle(" -> ") + destItem
	
		if os.path.isdir(sourceItem): shutil.copytree(sourceItem, destItem)
		else: shutil.copyfile(sourceItem, destItem)
	
	injectTo = os.path.join(os.getcwd(),confData.buildDir, debugInjectData[0])	
	
	print getSubTitle("Injecting: ") + injectTo	
	lines = []
	with open(injectTo) as infile:
		for line in infile:
			line = line.replace(debugInjectData[1], debugInjectData[2])
			lines.append(line)
			
	with open(injectTo, 'w') as outfile:
		for line in lines:
			outfile.write(line)
	
	print getColorText(bcolors.OKGREEN,"DONE!")
	return
	
def replaceTagInGame(fileName, tag,changeTo):
	print getTitle("Setting Game Name to: ") + changeTo	
	lines = []
	
	injectTo = os.path.join(os.getcwd(),confData.buildDir, fileName)	
	with open(injectTo) as infile:
		for line in infile:
			line = line.replace(tag, changeTo)
			lines.append(line)
			
	with open(injectTo, 'w') as outfile:
		for line in lines:
			outfile.write(line)
	
	print getColorText(bcolors.OKGREEN,"DONE!")
	return
	
def configSectionMap(config,section):
	dict1 = {}
	options = config.options(section)
	for option in options:
		try:
			dict1[option] = config.get(section, option)
			if dict1[option] == -1:
				DebugPrint("skip: %s" % option)
		except:
			print("exception on %s!" % option)
			dict1[option] = None
	return dict1	
	
def getKeyFromDict(dict, key):
	if key in dict: return dict[key]
	else : return None

def readConfiguration():
	try:
		parser = argparse.ArgumentParser()
		parser.add_argument("-o","--optimize",help="Optimizes assets on export.", default=None)
		parser.add_argument("-d","--debug",help="Add debug scripts to the game.", default=None)
		parser.add_argument("-gk","--gameKey",help="Game Key", default=None)
		parser.add_argument("-gn","--gameName",help="Game Name. Defaults to Game Key", default=None)
		parser.add_argument("-v","--verbose",help="Print log", default=None)
		parser.add_argument("-uo","--uploadOnly",help="Re-upload previous build", default=None)
		parser.add_argument("-uz","--uploadZip",help="Should we upload the zip file.", default=None)
		parser.add_argument("-us","--uploadSource",help="Should we upload the source files.", default=None)
		parser.add_argument("-bd","--buildDir",help="Where to copy the compiled files.", default=None)
		parser.add_argument("-t","--timeOut",help="FTP timeout.", default=None)
		parser.add_argument("-wsc","--winScpCmd",help="Extra WinSCP commands.", default=None)
		parser.add_argument("-cf","--configFile",help="Choose alternative config file.", default="config.ini")
		parser.add_argument("-af","--authFile",help="Choose alternative auth file.", default="auth.ini")
		parser.add_argument("-ui","--updatingAssets",help="Alternative index.html to be used while updating.", default=None)
		parser.add_argument("-ri","--releaseIndex",help="Alternative index.html to be used when upload is finished.", default=None)
		
		args = parser.parse_args()
		if args.optimize != None: confData.optimizeAssets = True if args.optimize == "1" else False
		if args.debug != None: confData.injectDebug = True if args.debug == "1" else False
		if args.gameName != None: confData.gameName = args.gameName
		if args.gameKey != None: confData.gameKey = args.gameKey
		if args.buildDir != None: confData.buildDir = args.buildDir
		if args.verbose != None: confData.isVerbose = True if args.verbose == "1" else False
		if args.uploadSource != None: confData.uploadSource = True if args.uploadSource == "1" else False
		if args.uploadZip != None: confData.uploadZip = True if args.uploadZip == "1" else False
		if args.uploadOnly != None: confData.uploadOnly = True if args.uploadOnly == "1" else False
		if args.timeOut != None: confData.ftpTimeout = args.timeOut
		if args.winScpCmd != None: confData.extraWinScpCMds = args.winScpCmd
		if args.updatingAssets != None: confData.updatingAssets = args.updatingAssets
		if args.releaseIndex != None: confData.releaseIndex = args.releaseIndex
		
		config = ConfigParser.ConfigParser()
		config.read(args.configFile)
		
		projectSection = configSectionMap(config,"Project")
		compilerSection = configSectionMap(config,"Compiler")
		uploaderSection = configSectionMap(config,"Uploader")
		
		confData.targetPath = getKeyFromDict(uploaderSection,"targetpath")
		if confData.targetPath == None: confData.targetPath = ""

		confData.projectRoot = os.path.abspath(os.path.normpath(getKeyFromDict(projectSection,"projectroot")))
		if confData.buildDir == None: buildDir = os.path.normpath(getKeyFromDict(projectSection,"builddir"))
		else: buildDir = os.path.normpath(confData.buildDir)

		confData.buildDir = os.path.abspath(os.path.join(confData.projectRoot, buildDir))
		
		confData.itemsToCopy = getKeyFromDict(projectSection,"items").split(",")
		confData.debugItems = getKeyFromDict(projectSection,"debugitems").split(",")
		confData.debugInjectData = getKeyFromDict(projectSection,"debuginjectdata").split(":")
		confData.zipPath = getKeyFromDict(compilerSection,"zippath")

		if confData.gameKey == None: confData.gameKey = getKeyFromDict(projectSection,"gamekey")
		if confData.gameName == None: confData.gameName = getKeyFromDict(projectSection,"gamename")
		if confData.optimizeAssets == None: confData.optimizeAssets = getKeyFromDict(compilerSection,"optimize")
		if confData.injectDebug == None: confData.injectDebug = getKeyFromDict(compilerSection,"debug")
		if confData.isVerbose == None: confData.isVerbose = getKeyFromDict(compilerSection,"verbose")	
		if confData.zipPath != None: confData.zipPath = confData.zipPath.replace(".zip","")

		if confData.uploadSource == None: confData.uploadSource = getKeyFromDict(uploaderSection,"uploadsource")
		if confData.uploadZip == None: confData.uploadZip = getKeyFromDict(uploaderSection,"uploadzip")
		if confData.ftpTimeout == None: confData.ftpTimeout = getKeyFromDict(uploaderSection,"timeout")
		if confData.extraWinScpCMds == None: confData.extraWinScpCMds = getKeyFromDict(uploaderSection,"extrawinscpcmds")
		if confData.updatingAssets == None: confData.updatingAssets = getKeyFromDict(uploaderSection,"updatingassets").split(",")
		if confData.releaseIndex == None: confData.releaseIndex = getKeyFromDict(uploaderSection,"releaseindex")
		
		if confData.ftpTimeout != None and confData.ftpTimeout.isdigit() == False: confData.ftpTimeout = 20
		else: confData.ftpTimeout = int(confData.ftpTimeout)

		config = ConfigParser.ConfigParser()
		config.read(args.authFile)
		
		ftpSection = configSectionMap(config,"FTP")

		confData.username = getKeyFromDict(ftpSection,"username")
		confData.password = getKeyFromDict(ftpSection,"password")
		confData.domain = getKeyFromDict(ftpSection,"domain")
	except:
		e = sys.exc_info()[0]
		print e
	return
	
def startUpload(path, newFileName):

	path = os.path.abspath(path)
	print getTitle("Uploading: ") + path + getSubTitle(" -> ") + confData.targetPath
	tempFile = "ftpCmd.dat"
	ftpDataFile = open(tempFile, "w")
	
	ftpDataFile.write("OPEN ftp://{0}:{1}@{2}\n".format(confData.username,confData.password,confData.domain))
	ftpDataFile.write("option batch continue\n")
	ftpDataFile.write("MKDIR {0}\n".format(confData.targetPath))
	
	if os.path.isdir(path):
		ftpDataFile.write("SYNCHRONIZE remote {0} {1}\n".format(path, confData.targetPath))
	else:
		if newFileName == None: fileName = os.path.basename(path)
		else: fileName = newFileName
		
		ftpDataFile.write("LCD {0}\n".format(confData.projectRoot))
		ftpDataFile.write("CD {0}\n".format(confData.targetPath))
		ftpDataFile.write("PUT -neweronly {0} {1}\n".format(path,fileName))
	ftpDataFile.write("option batch off\n")
	ftpDataFile.write("EXIT\n")
	
	ftpDataFile.close()
	
	DEVNULL = open(os.devnull, 'wb')
	
	callString = "WinSCP.com"
	if confData.ftpTimeout > 0 == True: callString += " /timeout={0}".format(confData.ftpTimeout)
	if confData.extraWinScpCMds != None: callString += confData.extraWinScpCMds
	callString += " /script={0}".format(tempFile)
	
	print callString
	
	if confData.isVerbose: subprocess.call(callString)
	else: subprocess.call(callString, stdout=DEVNULL, stderr=subprocess.STDOUT)
	DEVNULL.close()
	
	os.remove(tempFile)
	
	print getColorText(bcolors.OKGREEN,"DONE!")
	return
	
def createZipFile():
	print getTitle("Creating zip File: ") + confData.zipPath
	try:
		if os.path.exists(confData.zipPath):
			os.remove(confData.zipPath)
		
		shutil.make_archive(confData.zipPath, 'zip', confData.buildDir)
	except:
		e = sys.exc_info()[0]
		print e
	print getColorText(bcolors.OKGREEN,"DONE!")
	return
	
def prepareIndexFile():
	copyAllAssets([confData.releaseIndex+":index.html"], False)
	if confData.injectDebug: injectDebug(confData.debugItems,confData.debugInjectData)
	replaceTagInGame("index.html","<app-name>",confData.gameName);	
		
	if bumpVersionNumber() == False:
		print "Program Terminated.";
		sys.exit();
	else: return;

def bumpVersionNumber():
	print getTitle("Bumping Version Number")
	targetPath = os.path.join(os.getcwd(),confData.projectRoot, "gameVersion.ini")
	target = None;
	version = 0;
	if(os.path.exists(targetPath)):
		target = open(targetPath, 'r')
		try:
			version = int(target.readline()) + 1;
			target.close()
		except:
			target.close();
			print getWarn("Failed to bump version!")
			return False
			
	target = open(targetPath, 'w')
	target.write(str(version));
	target.close()
	
	replaceTagInGame("index.html","<app-version>",str(version));
	return True

try:	
	scriptDir = os.getcwd()
	readConfiguration()

	if confData.uploadOnly != True:
		copyAllAssets(confData.itemsToCopy, True)
		if confData.optimizeAssets: optimizeAssets()
		
	if confData.uploadSource:
		copyAllAssets(confData.updatingAssets, False)
		
		for asset in confData.updatingAssets:
			asset = asset.split(":");
			if len(asset) == 2: 
				tempPath = os.path.join(confData.buildDir, asset[1]);
				replaceTagInGame(asset[1],"<app-name>",confData.gameName);	
				startUpload(tempPath, asset[1])
			else: 
				tempPath = os.path.join(confData.buildDir, asset[0]);
				replaceTagInGame(asset[0],"<app-name>",confData.gameName);	
				startUpload(tempPath, asset[0])
			os.remove(tempPath)		
		
		startUpload(confData.buildDir, None)
		
		prepareIndexFile();
		
		tempPath = os.path.join(confData.buildDir, "index.html");
		startUpload(tempPath,"index.html" )
	else:
		prepareIndexFile();
			
	#Finalize Build
   
	if confData.zipPath: 
		createZipFile()
		if confData.uploadZip == True: startUpload(confData.zipPath + ".zip", None)
		raw_input("Press Enter to continue...")
except:
		e = sys.exc_info()[0]
		print e
		raw_input("Exception occured press Enter to continue...")
	
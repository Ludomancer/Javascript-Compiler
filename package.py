import argparse
import sys
import ConfigParser
import os
import fnmatch
import subprocess
import printer
import dictUtils
import fileUtils
import ftpHelper


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
    extraWinScpCmds = None
    targetPath = ""
    updatingAssets = None
    releaseIndex = None


def readConfiguration():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-o", "--optimize", help="Optimizes assets on export.", default=None)
        parser.add_argument("-d", "--debug", help="Add debug scripts to the game.", default=None)
        parser.add_argument("-gk","--gameKey", help="Game Key", default=None)
        parser.add_argument("-gn","--gameName", help="Game Name. Defaults to Game Key", default=None)
        parser.add_argument("-v","--verbose", help="Print log", default=None)
        parser.add_argument("-uo","--uploadOnly", help="Re-upload previous build", default=None)
        parser.add_argument("-uz","--uploadZip", help="Should we upload the zip file.", default=None)
        parser.add_argument("-us","--uploadSource", help="Should we upload the source files.", default=None)
        parser.add_argument("-bd","--buildDir", help="Where to copy the compiled files.", default=None)
        parser.add_argument("-t","--timeOut", help="FTP timeout.", default=None)
        parser.add_argument("-wsc","--winScpCmd", help="Extra WinSCP commands.", default=None)
        parser.add_argument("-cf","--configFile", help="Choose alternative config file.", default="config.ini")
        parser.add_argument("-af","--authFile", help="Choose alternative auth file.", default="auth.ini")
        parser.add_argument("-ui","--updatingAssets", help="Alternative index.html to be used while updating.", default=None)
        parser.add_argument("-ri","--releaseIndex", help="Alternative index.html to be used when upload is finished.", default=None)

        args = parser.parse_args()
        if args.optimize is not None:
            confData.optimizeAssets = True if args.optimize == "1" else False
        if args.debug is not None:
            confData.injectDebug = True if args.debug == "1" else False
        if args.gameName is not None:
            confData.gameName = args.gameName
        if args.gameKey is not None:
            confData.gameKey = args.gameKey
        if args.buildDir is not None:
            confData.buildDir = args.buildDir
        if args.verbose is not None:
            confData.isVerbose = True if args.verbose == "1" else False
        if args.uploadSource is not None:
            confData.uploadSource = True if args.uploadSource == "1" else False
        if args.uploadZip is not None:
            confData.uploadZip = True if args.uploadZip == "1" else False
        if args.uploadOnly is not None:
            confData.uploadOnly = True if args.uploadOnly == "1" else False
        if args.timeOut is not None:
            confData.ftpTimeout = args.timeOut
        if args.winScpCmd is not None:
            confData.extraWinScpCmds = args.winScpCmd
        if args.updatingAssets is not None:
            confData.updatingAssets = args.updatingAssets
        if args.releaseIndex is not None:
            confData.releaseIndex = args.releaseIndex

        config = ConfigParser.ConfigParser()
        config.read(args.configFile)

        projectSection = dictUtils.configSectionMap(config, "Project")
        compilerSection = dictUtils.configSectionMap(config, "Compiler")
        uploaderSection = dictUtils.configSectionMap(config, "Uploader")

        confData.targetPath = dictUtils.getKeyFromDict(uploaderSection, "targetpath")
        if confData.targetPath is None:
            confData.targetPath = ""

        confData.projectRoot = os.path.abspath(os.path.normpath(dictUtils.getKeyFromDict(projectSection, "projectroot")))
        if confData.buildDir is None:
            buildDir = os.path.normpath(dictUtils.getKeyFromDict(projectSection, "builddir"))
        else:
            buildDir = os.path.normpath(confData.buildDir)

        confData.buildDir = os.path.abspath(os.path.join(confData.projectRoot, buildDir))

        confData.itemsToCopy = dictUtils.getKeyFromDict(projectSection, "items").split(",")
        confData.debugItems = dictUtils.getKeyFromDict(projectSection, "debugitems").split(",")
        confData.debugInjectData = dictUtils.getKeyFromDict(projectSection, "debuginjectdata").split(":")
        confData.zipPath = dictUtils.getKeyFromDict(compilerSection, "zippath")

        if confData.gameKey is None:
            confData.gameKey = dictUtils.getKeyFromDict(projectSection, "gamekey")
        if confData.gameName is None:
            confData.gameName = dictUtils.getKeyFromDict(projectSection, "gamename")
        if confData.optimizeAssets is None:
            confData.optimizeAssets = dictUtils.getKeyFromDict(compilerSection, "optimize")
        if confData.injectDebug is None:
            confData.injectDebug = dictUtils.getKeyFromDict(compilerSection, "debug")
        if confData.isVerbose is None:
            confData.isVerbose = dictUtils.getKeyFromDict(compilerSection, "verbose")
        if confData.zipPath is not None:
            confData.zipPath = confData.zipPath.replace(".zip", "")

        if confData.uploadSource is None:
            confData.uploadSource = dictUtils.getKeyFromDict(uploaderSection, "uploadsource")
        if confData.uploadZip is None:
            confData.uploadZip = dictUtils.getKeyFromDict(uploaderSection, "uploadzip")
        if confData.ftpTimeout is None:
            confData.ftpTimeout = dictUtils.getKeyFromDict(uploaderSection, "timeout")
        if confData.extraWinScpCmds is None:
            confData.extraWinScpCmds = dictUtils.getKeyFromDict(uploaderSection, "extraWinScpCmds")
        if confData.updatingAssets is None:
            confData.updatingAssets = dictUtils.getKeyFromDict(uploaderSection, "updatingassets").split(",")
        if confData.releaseIndex is None:
            confData.releaseIndex = dictUtils.getKeyFromDict(uploaderSection, "releaseindex")

        if confData.ftpTimeout is not None and confData.ftpTimeout.isdigit() is False:
            confData.ftpTimeout = 20
        else:
            confData.ftpTimeout = int(confData.ftpTimeout)

        config = ConfigParser.ConfigParser()
        config.read(args.authFile)

        ftpSection = dictUtils.configSectionMap(config, "FTP")

        confData.username = dictUtils.getKeyFromDict(ftpSection, "username")
        confData.password = dictUtils.getKeyFromDict(ftpSection, "password")
        confData.domain = dictUtils.getKeyFromDict(ftpSection, "domain")

        ftpHelper.timeOut = confData.ftpTimeout
        ftpHelper.extraWinScpCmds = confData.extraWinScpCmds
        ftpHelper.isVerbose = confData.isVerbose
    except:
        e = sys.exc_info()[0]
        print e
    return


def copyAllAssets(itemList, clear):
    print printer.title("Clearing: ") + confData.buildDir
    if(os.path.exists(confData.buildDir)):
        if clear is True:
            fileUtils.deleteDirRecursive(confData.buildDir)
    else:
        os.mkdir(confData.buildDir)

    print printer.title("Copying Assets")

    for item in itemList:
        itemData = item.split(":")
        sourceItem = os.path.join(os.getcwd(),confData.projectRoot, itemData[0])

        if(len(itemData) == 2):
            destItem = os.path.join(os.getcwd(),confData.buildDir, itemData[1])
        else:
            destItem = os.path.join(os.getcwd(),confData.buildDir, itemData[0])

        print printer.subTitle("Copying: ") + sourceItem + printer.subTitle(" -> ") + destItem

        fileUtils.copyAllRecursive(sourceItem,destItem)
    print printer.okGreen("DONE!")
    return


def optimizeAssets():
    print printer.title("Optimizing Assets")
    compilerPath = os.path.join(os.getcwd(), "compiler.jar")
    pngOptPath = os.path.join(os.getcwd(), "pngquant.exe")
    jpgOptPat = os.path.join(os.getcwd(), "jpegtran.exe")
    DEVNULL = open(os.devnull, 'wb')
    for root, dirnames, filenames in os.walk(confData.buildDir):
        for extension in ['jpg', 'jpeg', 'png', 'js']:
            for filename in fnmatch.filter(filenames, '*.' + extension):
                filename = os.path.join(os.getcwd(),root, filename)
                print printer.subTitle("Optimizing: ") + filename
                if (extension == 'jpg') or (extension == 'jpeg'):
                    callString = '"{1}" -copy none -optimize -outfile "{0}" "{0}"'.format(filename,jpgOptPat)
                if (extension == 'png'):
                    callString = '"{1}" --force --verbose --ext .png --speed 1 --quality=45-85 "{0}"'.format(filename,pngOptPath)
                if (extension == 'js'):
                    callString = 'java -jar "{1}" --js_output_file="{0}" "{0}"'.format(filename,compilerPath)
                else:
                    continue
                if confData.isVerbose:
                    subprocess.call(callString)
                else:
                    subprocess.call(callString, stdout=DEVNULL, stderr=subprocess.STDOUT)
    DEVNULL.close()
    print printer.okGreen("DONE!")
    return


def prepareIndexFile():
    copyAllAssets([confData.releaseIndex + ":index.html"], False)
    if confData.injectDebug:
        injectDebug(confData.debugItems,confData.debugInjectData)
    injectTo = os.path.join(os.getcwd(),confData.buildDir, "index.html")
    fileUtils.replaceStringInFile(injectTo,"<app-name>",confData.gameName)

    if bumpVersionNumber() is False:
        print "Program Terminated."
        sys.exit()
    else:
        return


def injectDebug(items,debugInjectData):
    print printer.title("Injecting Debug Files")

    for item in items:
        sourceItem = os.path.join(os.getcwd(),confData.projectRoot, item)
        destItem = os.path.join(os.getcwd(),confData.buildDir, item)

        print printer.subTitle("Copying: ") + sourceItem + printer.subTitle(" -> ") + destItem

        fileUtils.copyAllRecursive(sourceItem,destItem)

    injectTo = os.path.join(os.getcwd(),confData.buildDir, debugInjectData[0])

    fileUtils.replaceStringInFile(injectTo,debugInjectData[1],debugInjectData[2])

    print printer.okGreen("DONE!")
    return


def bumpVersionNumber():
    print printer.title("Bumping version number")
    targetPath = os.path.join(os.getcwd(), confData.projectRoot, "gameVersion.ini")
    target = None
    version = 0
    if(os.path.exists(targetPath)):
        target = open(targetPath, 'r')
        try:
            version = int(target.readline()) + 1
            target.close()
        except:
            target.close()
            print printer.warn("Failed to bump version!")
            return False

    target = open(targetPath, 'w')
    target.write(str(version))
    target.close()
    tempPath = os.path.join(confData.buildDir, "index.html")
    injectTo = os.path.join(os.getcwd(),tempPath)
    fileUtils.replaceStringInFile(injectTo, "<app-version>", str(version))
    return True

try:
    scriptDir = os.getcwd()
    readConfiguration()

    if confData.uploadOnly is not True:
        copyAllAssets(confData.itemsToCopy, True)
        if confData.injectDebug is True:
            copyAllAssets(confData.debugItems, False)
        if confData.optimizeAssets is True:
            optimizeAssets()

    if confData.uploadSource:
        copyAllAssets(confData.updatingAssets, False)
        for asset in confData.updatingAssets:
            asset = asset.split(":")
            nameIndex = 0
            if len(asset) == 2:
                nameIndex = 1
            else:
                nameIndex = 0

            tempPath = os.path.join(confData.buildDir, asset[nameIndex])
            injectTo = os.path.join(os.getcwd(),tempPath)
            fileUtils.replaceStringInFile(injectTo,"<app-name>",confData.gameName)
            ftpHelper.startUpload(
                tempPath,
                confData.domain,
                confData.username,
                confData.password,
                confData.projectRoot,
                confData.targetPath,
                asset[nameIndex]
            )
            os.remove(tempPath)

        ftpHelper.startUpload(
            confData.buildDir,
            confData.domain,
            confData.username,
            confData.password,
            confData.projectRoot,
            confData.targetPath,
            None
        )

        prepareIndexFile()

        tempPath = os.path.join(confData.buildDir, "index.html")
        ftpHelper.startUpload(
            tempPath,
            confData.domain,
            confData.username,
            confData.password,
            confData.projectRoot,
            confData.targetPath,
            "index.html"
        )
    else:
        prepareIndexFile()

    if confData.zipPath:
        fileUtils.createZipFile(confData.buildDir, confData.zipPath)
        if confData.uploadZip is True:
            ftpHelper.startUpload(confData.zipPath + ".zip", None)
        raw_input("Press Enter to continue...")
except:
        e = sys.exc_info()[0]
        print e
        raw_input("Exception occured press Enter to continue...")

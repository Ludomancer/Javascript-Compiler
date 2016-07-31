# region Author
#
# ************************************************************************************************************
# Author: Ludomancer/Nidre (Erdin Kacan)
# Website: http://erdin.me/
# GitHub: https://github.com/Nidre
# Behance : https://www.behance.net/erdinkacan
# ************************************************************************************************************
#
# endregion
#
# region Copyright
#
# ************************************************************************************************************
# The MIT License (MIT)
# Copyright (c) 2015 Erdin
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ************************************************************************************************************
#
# endregion

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

defaultAppVersionTag = "<app-version>"
defaultAppNameTag = "<app-name>"


class confData:
    username = ""
    password = ""
    domain = ""
    buildDir = None
    projectRoot = ""
    itemsToCopy = None
    debugItems = None
    debugInjectData = None
    appKey = None
    appName = None
    injectDebug = None
    optimizeAssets = None
    isVerbose = None
    zipPath = None
    uploadSource = None
    uploadZip = None
    ftpTimeout = None
    extraWinScpCmds = None
    targetPath = ""
    updatingAssets = None
    releaseAssets = None
    injectData = None
    version = None
    appVersionTag = defaultAppVersionTag
    appNameTag = defaultAppNameTag


compilerDir = os.path.dirname(os.path.realpath(__file__))


def readConfiguration():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-i","--itemsToCopy", help="Items to copy.", default=None)
        parser.add_argument("-o", "--optimize", help="Optimizes assets on export.", default=None)
        parser.add_argument("-d", "--debug", help="Add debug scripts to the game.", default=None)
        parser.add_argument("-ak","--appKey", help="App Key", default=None)
        parser.add_argument("-an","--appName", help="App Name. Defaults to Game Key", default=None)
        parser.add_argument("-avt","--appVersionTag", help="App Key Tag", default=defaultAppVersionTag)
        parser.add_argument("-ant","--appNameTag", help="App Name Tag., default=defaultAppNameTag)
        parser.add_argument("-v","--verbose", help="Print log", default=None)
        parser.add_argument("-uz","--uploadZip", help="Should we upload the zip file.", default=None)
        parser.add_argument("-us","--uploadSource", help="Should we upload the source files.", default=None)
        parser.add_argument("-pr","--projectRoot", help="Root path of your JavaScript project.", default=None)
        parser.add_argument("-bd","--buildDir", help="Where to copy the compiled files.", default=None)
        parser.add_argument("-t","--timeOut", help="FTP timeout.", default=None)
        parser.add_argument("-wsc","--winScpCmd", help="Extra WinSCP commands.", default=None)
        parser.add_argument("-cf","--configFile", help="Choose alternative config file.", default="config.ini")
        parser.add_argument("-af","--authFile", help="Choose alternative auth file.", default="auth.ini")
        parser.add_argument("-ua","--updatingAssets", help="Alternative files to be used while updating.", default=None)
        parser.add_argument("-ra","--releaseAssets", help="Alternative files to be used when upload is finished.", default=None)
        parser.add_argument("-di","--debugItems", help="Items to be copied if debug is enabled", default=None)
        parser.add_argument("-dd","--debugInjectData", help="Debug Inject instructions.", default=None)
        parser.add_argument("-id","--injectData", help="Inject instructions.", default=None)
        parser.add_argument("-ver","--version", help="Version, it will be automatically created and bumped if not provided.", default=None)
        parser.add_argument("-zp","--zipPath", help="Where to export the zip file containing the project in the end.", default=None)
        parser.add_argument("-tp","--targetPath", help="Where to upload the project when the compilation is completed. This should be a directory name not the full path. Directory will be created if doesn't exists.", default="")

        args = parser.parse_args()
        if args.itemsToCopy is not None:
            confData.itemsToCopy = args.itemsToCopy
        if args.optimize is not None:
            confData.optimizeAssets = True if args.optimize == "1" else False
        if args.debug is not None:
            confData.injectDebug = True if args.debug == "1" else False
        if args.appName is not None:
            confData.appName = args.appName
        if args.appKey is not None:
            confData.appKey = args.appKey
        if args.projectRoot is not None:
            confData.projectRoot = args.projectRoot
        if args.buildDir is not None:
            confData.buildDir = args.buildDir
        if args.verbose is not None:
            confData.isVerbose = True if args.verbose == "1" else False
        if args.uploadSource is not None:
            confData.uploadSource = True if args.uploadSource == "1" else False
        if args.uploadZip is not None:
            confData.uploadZip = True if args.uploadZip == "1" else False
        if args.timeOut is not None:
            confData.ftpTimeout = args.timeOut
        if args.winScpCmd is not None:
            confData.extraWinScpCmds = args.winScpCmd
        if args.updatingAssets is not None:
            confData.updatingAssets = args.updatingAssets
        if args.releaseAssets is not None:
            confData.releaseAssets = args.releaseAssets
        if args.debugItems is not None:
            confData.debugItems = args.debugItems
        if args.debugInjectData is not None:
            confData.debugInjectData = args.debugInjectData
        if args.injectData is not None:
            confData.injectData = args.injectData
        if args.version is not None:
            confData.version = args.version
        if args.appNameTag is not defaultAppNameTag:
            confData.appNameTag = args.appNameTag
        if args.appVersionTag is not defaultAppVersionTag:
            confData.appVersionTag = args.appVersionTag
        if args.zipPath is not None:
            confData.zipPath = args.zipPath
        if args.targetPath is not None:
            confData.targetPath = args.targetPath

        config = ConfigParser.ConfigParser()
        config.read(args.configFile)

        projectSection = dictUtils.configSectionMap(config, "Project")
        compilerSection = dictUtils.configSectionMap(config, "Compiler")
        uploaderSection = dictUtils.configSectionMap(config, "Uploader")

        if confData.targetPath is None:
            confData.targetPath = dictUtils.getKeyFromDict(uploaderSection, "targetpath")
        if confData.targetPath is None:
            confData.targetPath = ""

        if confData.projectRoot is None:
            confData.projectRoot = os.path.abspath(os.path.normpath(dictUtils.getKeyFromDict(projectSection, "projectroot")))

        if confData.buildDir is None:
            buildDir = os.path.normpath(dictUtils.getKeyFromDict(projectSection, "builddir"))
        else:
            buildDir = os.path.normpath(confData.buildDir)

        confData.buildDir = os.path.abspath(os.path.join(confData.projectRoot, buildDir))

        if confData.itemsToCopy is None:
            items = dictUtils.getKeyFromDict(projectSection, "itemstocopy")
        else:
            items = confData.itemsToCopy

        if items:
            confData.itemsToCopy = items.split(",")
        if confData.debugItems is None:
            items = dictUtils.getKeyFromDict(projectSection, "debugitems")
        else:
            items = confData.debugItems
        if items:
            confData.debugItems = items.split(",")

        if confData.debugInjectData is None:
            items = dictUtils.getKeyFromDict(projectSection, "debuginjectdata")
        else:
            items = confData.debugInjectData
        if items:
            confData.debugInjectData = items.split(",")
            index = 0
            for data in confData.debugInjectData:
                confData.debugInjectData[index] = data.split(";")
                index = index + 1

        if confData.injectData is None:
            items = dictUtils.getKeyFromDict(projectSection, "injectdata")
        else:
            items = confData.injectData
        if items:
            confData.injectData = items.split(",")
            index = 0
            for data in confData.injectData:
                confData.injectData[index] = data.split(";")
                index = index + 1

        if confData.zipPath is None:
            confData.zipPath = dictUtils.getKeyFromDict(compilerSection, "zippath")
        if confData.appKey is None:
            confData.appKey = dictUtils.getKeyFromDict(projectSection, "appkey")
        if confData.appName is None:
            confData.appName = dictUtils.getKeyFromDict(projectSection, "appname")

        if confData.appNameTag is defaultAppNameTag:
            temp = dictUtils.getKeyFromDict(projectSection, "appnametag")
            if temp:
                confData.appNameTag = temp
        if confData.appVersionTag is defaultAppVersionTag:
            temp = dictUtils.getKeyFromDict(projectSection, "appversiontag")
            if temp:
                confData.appVersionTag = temp

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
            items = dictUtils.getKeyFromDict(uploaderSection, "updatingassets")
        else:
            items = confData.updatingAssets
        if items:
            confData.updatingAssets = items.split(",")

        if confData.releaseAssets is None:
            items = dictUtils.getKeyFromDict(uploaderSection, "releaseassets")
        else:
            items = confData.releaseAssets
        if items:
            confData.releaseAssets = items.split(",")

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
    if itemList is None:
        return
    if(os.path.exists(confData.buildDir)):
        if clear is True:
            print printer.title("Clearing: ") + confData.buildDir
            fileUtils.deleteDirRecursive(confData.buildDir)
            os.mkdir(confData.buildDir)
    else:
        os.mkdir(confData.buildDir)

    print printer.title("Copying Assets")

    for item in itemList:
        itemData = item.split(";")
        sourceItem = os.path.join(compilerDir,confData.projectRoot, itemData[0])

        if(len(itemData) == 2):
            destItem = os.path.join(compilerDir,confData.buildDir, itemData[1])
        else:
            destItem = os.path.join(compilerDir,confData.buildDir, itemData[0])

        print printer.subTitle("Copying: ") + sourceItem + printer.subTitle(" -> ") + destItem

        fileUtils.copyAllRecursive(sourceItem,destItem)
    print printer.okGreen("DONE!")
    return


def optimizeAssets():
    print printer.title("Optimizing Assets")
    compilerPath = os.path.join(compilerDir, "compiler.jar")
    pngOptPath = os.path.join(compilerDir, "pngquant.exe")
    jpgOptPat = os.path.join(compilerDir, "jpegtran.exe")
    DEVNULL = open(os.devnull, 'wb')
    for root, dirnames, filenames in os.walk(confData.buildDir):
        for extension in ['jpg', 'jpeg', 'png', 'js']:
            for filename in fnmatch.filter(filenames, '*.' + extension):
                filename = os.path.join(compilerDir,root, filename)
                print printer.subTitle("Optimizing: ") + filename
                if (extension == 'jpg') or (extension == 'jpeg'):
                    callString = '"{1}" -copy none -optimize -outfile "{0}" "{0}"'.format(filename,jpgOptPat)
                elif (extension == 'png'):
                    callString = '"{1}" --force --verbose --ext .png --speed 1 --quality=45-85 "{0}"'.format(filename,pngOptPath)
                elif (extension == 'js'):
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


def injectDebug(items,debugInjectData):
    if items is None:
        return
    print printer.title("Injecting Debug Files")
    for item in items:
        sourceItem = os.path.join(compilerDir,confData.projectRoot, item)
        destItem = os.path.join(compilerDir,confData.buildDir, item)

        print printer.subTitle("Copying: ") + sourceItem + printer.subTitle(" -> ") + destItem

        fileUtils.copyAllRecursive(sourceItem,destItem)
    for injectData in debugInjectData:
        injectStringToFile(injectData[0],injectData[1],injectData[2],confData.buildDir)
    print printer.okGreen("DONE!")
    return


def injectStrings(injectDatas,rootPath):
    if injectDatas is None:
        return
    for injectData in injectDatas:
        injectStringToFile(injectData[0],injectData[1],injectData[2],rootPath)


def injectStringToFile(file, toReplace, toInject, rootPath):
    if file is None:
        return
    injectTo = os.path.join(compilerDir,rootPath, file)
    if os.path.isfile(injectTo):
        fileUtils.replaceStringInFile(injectTo,toReplace,toInject)


def injectAppVersion(version, rootPath):
    print printer.title("Injecting App Version")
    for root, dirnames, filenames in os.walk(rootPath):
        for filename in filenames:
            filename = os.path.join(compilerDir,root, filename)
            injectStringToFile(filename,confData.appVersionTag,version,rootPath)


def injectAppName(rootPath):
    print printer.title("Injecting App Name")
    for root, dirnames, filenames in os.walk(rootPath):
        for filename in filenames:
            filename = os.path.join(compilerDir,root, filename)
            injectStringToFile(filename,confData.appNameTag,confData.appName,rootPath)


def bumpVersionNumber():
    print printer.title("Bumping version number")
    targetPath = os.path.join(compilerDir, confData.projectRoot, "appVersion.ini")
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
            print "Program Terminated."
            sys.exit()
    target = open(targetPath, 'w')
    target.write(str(version))
    target.close()
    confData.version = version
    return True


def prepareForRelease(clearBuildDir):
    # Copy actual assets
    copyAllAssets(confData.itemsToCopy,clearBuildDir)
    if confData.optimizeAssets is True:
        optimizeAssets()
    doInjections()


def doInjections():
    # Inject debug to all assets.
    if confData.injectDebug and confData.debugItems and confData.debugInjectData:
        injectDebug(confData.debugItems,confData.debugInjectData)
    # Inject configured tags to all assets.
    if confData.injectData:
        injectStrings(confData.injectData,confData.buildDir)
    injectAppVersion(str(confData.version),confData.buildDir)
    injectAppName(confData.buildDir)


def uploadUpdatingAssets():
    if confData.updatingAssets is not None:
        print printer.title("Preparing and Uplading uploadingAssets")
        # Prepare and upload updatingAssets assets if necessary.
        copyAllAssets(confData.updatingAssets, True)
        # Re-inject everything so updating assets also get an injection. Need to optimize just apply for the new files.
        doInjections()
        ftpHelper.startUpload(
            confData.updatingAssets,
            confData.domain,
            confData.username,
            confData.password,
            confData.buildDir,
            confData.targetPath
        )
        print printer.title("Clearing uploadingAssets")
        # Remove updating assets.
        for updatingAsset in confData.updatingAssets:
            updatingAsset = updatingAsset.split(";")
            if len(updatingAsset) == 2:
                fileUtils.deleteDirRecursive(os.path.join(compilerDir, confData.buildDir,updatingAsset[1]))
            else:
                fileUtils.deleteDirRecursive(os.path.join(compilerDir, confData.buildDir,updatingAsset[0]))


def uploadSource():
    print printer.title("Uploading Source Files")

    print printer.title("Preparing and Uplading normal assets")
    # Copy and prepare normal assets
    prepareForRelease(True)
    # Upload normal assets.
    ftpHelper.startUpload(
        confData.buildDir,
        confData.domain,
        confData.username,
        confData.password,
        confData.buildDir,
        confData.targetPath
    )

    if confData.releaseAssets:
        print printer.title("Preparing and Uplading releaseAssets")

        # Copy and preapre release only assets.
        copyAllAssets(confData.releaseAssets,False)
        if confData.optimizeAssets is True:
            optimizeAssets()
        doInjections()

        # Upload release assets.
        ftpHelper.startUpload(
            confData.releaseAssets,
            confData.domain,
            confData.username,
            confData.password,
            confData.buildDir,
            confData.targetPath
        )


try:
    readConfiguration()

    # Create and bump version number if necessary.
    if confData.version is None:
        bumpVersionNumber()

    if confData.uploadSource:
        # Delete everything, copy updatingAssets and upload them.
        uploadUpdatingAssets()
        # Delete everything again, copy and optimize all assets along side with release assets.
        uploadSource()
    else:
        # Delete everything , optimize assets.
        prepareForRelease(True)

    if confData.zipPath:
        fileUtils.createZipFile(confData.buildDir, confData.zipPath)
        if confData.uploadZip is True:
            ftpHelper.startUpload(confData.zipPath + ".zip", None)
        raw_input("Press Enter to continue...")
except:
        e = sys.exc_info()[0]
        print e
        raw_input("Exception occured press Enter to continue...")

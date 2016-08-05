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
import shutil
import printer
import configHelper
import fileUtils
import ftpHelper
from commonPaths import compiler_dir, cssOptPath, jpgOptPath, pngOptPath, compilerPath, htmlOptPath

defaultAppVersionTag = "<app-version>"
defaultAppNameTag = "<app-name>"

jpgFormats = ["jpg", "jpeg"]
pngFormats = ["png"]
htmlFormats = ["php", "html"]
cssFormats = ["css"]
jsFormats = ["js"]


class confData:
    username = ""
    password = ""
    domain = ""
    buildDir = None
    projectRoot = None
    itemsToCopy = None
    debugItems = None
    debugInjectData = None
    appKey = None
    appName = None
    injectDebug = None
    isVerbose = None
    zipPath = None
    uploadSource = None
    uploadZip = None
    ftpTimeout = None
    extraWinScpCmds = None
    targetPath = None
    updatingAssets = None
    releaseAssets = None
    injectData = None
    version = None
    bumpVersion = None
    appVersionTag = defaultAppVersionTag
    appNameTag = defaultAppNameTag
    optimizeAssets = None
    optimizeHtml = None
    optimizeCss = None
    optimizeJs = None
    optimizePng = None
    optimizeJpg = None


optExtensions = []


def readConfiguration():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", "--itemsToCopy",metavar='', help="Items to copy.")
        parser.add_argument("-d", "--debug",metavar='', help="Add debug scripts to the game.")
        parser.add_argument("-ak", "--appKey",metavar='', help="App Key")
        parser.add_argument("-an", "--appName",metavar='', help="App Name. Defaults to Game Key")
        parser.add_argument("-avt", "--appVersionTag",metavar='', help="App Key Tag")
        parser.add_argument("-ant", "--appNameTag",metavar='', help="App Name Tag.")
        parser.add_argument("-v", "--verbose",metavar='', help="Print log")
        parser.add_argument("-uz", "--uploadZip",metavar='', help="Should we upload the zip file.")
        parser.add_argument("-us", "--uploadSource",metavar='', help="Should we upload the source files.")
        parser.add_argument("-pr", "--projectRoot",metavar='', help="Root path of your JavaScript project.")
        parser.add_argument("-bd", "--buildDir",metavar='', help="Where to copy the compiled files.")
        parser.add_argument("-t", "--timeOut",metavar='', help="FTP timeout.")
        parser.add_argument("-wsc", "--winScpCmd",metavar='', help="Extra WinSCP commands.")
        parser.add_argument("-cf", "--configFile",metavar='', help="Choose alternative config file.", default="config.ini")
        parser.add_argument("-af", "--authFile",metavar='', help="Choose alternative auth file.", default="auth.ini")
        parser.add_argument("-ua", "--updatingAssets",metavar='', help="Alternative files to be used while updating.")
        parser.add_argument("-ra", "--releaseAssets",metavar='', help="Alternative files to be used when upload is finished.")
        parser.add_argument("-di", "--debugItems",metavar='', help="Items to be copied if debug is enabled")
        parser.add_argument("-dd", "--debugInjectData",metavar='', help="Debug Inject instructions.")
        parser.add_argument("-id", "--injectData",metavar='', help="Inject instructions.")
        parser.add_argument("-ver", "--version",metavar='', help="Version, it will be automatically created and bumped if not provided.")
        parser.add_argument("-bver", "--bumpVersion",metavar='',help="Should we bump the version number or not.")
        parser.add_argument("-zp", "--zipPath",metavar='', help="Where to export the zip file containing the project in the end.")
        parser.add_argument("-tp", "--targetPath",metavar='',help="Where to upload the project when the compilation is completed. This should be a directory name not the full path. Directory will be created if doesn't exists.")
        parser.add_argument("-o", "--optimize",metavar='', help="Optimizes assets on export.")
        parser.add_argument("-oh", "--optimizeHtml",metavar='',help="Should we optimize .html files. Needs optimize to be enabled.")
        parser.add_argument("-oc", "--optimizeCss",metavar='', help="Should we optimize .css files. Needs optimize to be enabled.")
        parser.add_argument("-ojs", "--optimizeJs",metavar='', help="Should we optimize .js files. Needs optimize to be enabled.")
        parser.add_argument("-oj", "--optimizeJpg",metavar='', help="Should we optimize .png files. Needs optimize to be enabled.")
        parser.add_argument("-op", "--optimizePng",metavar='', help="Should we optimize .jpg files. Needs optimize to be enabled.")

        args = parser.parse_args()
        if args.itemsToCopy is not None:
            confData.itemsToCopy = args.itemsToCopy
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
        if args.bumpVersion is not None:
            confData.bumpVersion = True if args.bumpVersion == "1" else False

        if args.optimize is not None:
            confData.optimizeAssets = True if args.optimize == "1" else False
        if args.optimizeHtml is not None:
            confData.optimizeHtml = True if args.optimizeHtml == "1" else False
        if args.optimizeCss is not None:
            confData.optimizeCss = True if args.optimizeCss == "1" else False
        if args.optimizeJs is not None:
            confData.optimizeJs = True if args.optimizeJs == "1" else False
        if args.optimizeJpg is not None:
            confData.optimizeJpg = True if args.optimizeJpg == "1" else False
        if args.optimizePng is not None:
            confData.optimizePng = True if args.optimizePng == "1" else False

        config = ConfigParser.ConfigParser()
        config.read(args.configFile)

        # Load Sections
        project_section = configHelper.configSectionMap(config, "Project")
        compiler_section = configHelper.configSectionMap(config, "Compiler")
        uploader_section = configHelper.configSectionMap(config, "Uploader")

        # Load Optimize Assets
        if confData.optimizeAssets is None:
            confData.optimizeAssets = bool(configHelper.getKeyFromDict(compiler_section, "optimize"))

        if confData.optimizeAssets is True:
            if confData.optimizeHtml is None:
                confData.optimizeHtml = bool(configHelper.getKeyFromDict(compiler_section, "optimizehtml"))
            if confData.optimizeCss is None:
                confData.optimizeCss = bool(configHelper.getKeyFromDict(compiler_section, "optimizecss"))
            if confData.optimizeJs is None:
                confData.optimizeJs = bool(configHelper.getKeyFromDict(compiler_section, "optimizejs"))
            if confData.optimizeJpg is None:
                confData.optimizeJpg = bool(configHelper.getKeyFromDict(compiler_section, "optimizejpg"))
            if confData.optimizePng is None:
                confData.optimizePng = bool(configHelper.getKeyFromDict(compiler_section, "optimizepng"))

        if confData.optimizeHtml:
            optExtensions.extend(htmlFormats)
        if confData.optimizeCss:
            optExtensions.extend(cssFormats)
        if confData.optimizeJs:
            optExtensions.extend(jsFormats)
        if confData.optimizeJpg:
            optExtensions.extend(jpgFormats)
        if confData.optimizePng:
            optExtensions.extend(pngFormats)

        # Load Target Path
        if confData.targetPath is None:
            confData.targetPath = configHelper.getKeyFromDict(uploader_section, "targetpath")
        # Load Project Root
        if confData.projectRoot is None:
            confData.projectRoot = os.path.normpath(configHelper.getKeyFromDict(project_section, "projectroot"))
        # Load Build Dir
        if confData.buildDir is None:
            confData.buildDir = os.path.normpath(configHelper.getKeyFromDict(project_section, "builddir"))
        else:
            confData.buildDir = os.path.normpath(confData.buildDir)
        confData.buildDir = os.path.join(compiler_dir, confData.projectRoot, confData.buildDir)
        # Load Items To Copy
        if confData.itemsToCopy is None:
            items = configHelper.getKeyFromDict(project_section, "itemstocopy")
        else:
            items = confData.itemsToCopy
        if items:
            confData.itemsToCopy = configHelper.splitSafe(items, ",")
        # Load Debug Items
        if confData.debugItems is None:
            items = configHelper.getKeyFromDict(project_section, "debugitems")
        else:
            items = confData.debugItems
        if items:
            confData.debugItems = configHelper.splitSafe(items, ",")
        # Load Debug Inject Data
        if confData.debugInjectData is None:
            items = configHelper.getKeyFromDict(project_section, "debuginjectdata")
        else:
            items = confData.debugInjectData
        if items:
            confData.debugInjectData = configHelper.splitSafe(items, ",")
            index = 0
            for data in confData.debugInjectData:
                confData.debugInjectData[index] = configHelper.splitSafe(data, ";")
                index += 1
        # Load Inject Data
        if confData.injectData is None:
            items = configHelper.getKeyFromDict(project_section, "injectdata")
        else:
            items = confData.injectData
        if items:
            confData.injectData = configHelper.splitSafe(items, ",")
            index = 0
            for data in confData.injectData:
                confData.injectData[index] = configHelper.splitSafe(data, ";")
                index += 1
        # Load Zip path
        if confData.zipPath is None:
            confData.zipPath = configHelper.getKeyFromDict(compiler_section, "zippath")
        if confData.zipPath is not None:
            confData.zipPath = confData.zipPath.replace(".zip", "")

        # Load App Key
        if confData.appKey is None:
            confData.appKey = configHelper.getKeyFromDict(project_section, "appkey")
        # Load Bump Version
        if confData.bumpVersion is None:
            confData.bumpVersion = bool(configHelper.getKeyFromDict(project_section, "bumpversion"))
        # Load App Name
        if confData.appName is None:
            confData.appName = configHelper.getKeyFromDict(project_section, "appname")
        # Load App Name Tag
        if confData.appNameTag is defaultAppNameTag:
            temp = configHelper.getKeyFromDict(project_section, "appnametag")
            if temp:
                confData.appNameTag = temp
        # Load App Version Tag
        if confData.appVersionTag is defaultAppVersionTag:
            temp = configHelper.getKeyFromDict(project_section, "appversiontag")
            if temp:
                confData.appVersionTag = temp
        # Load Inject Debug
        if confData.injectDebug is None:
            confData.injectDebug = configHelper.getKeyFromDict(compiler_section, "debug")
            if confData.injectDebug:
                confData.injectDebug = bool(confData.injectDebug)
        # Load Is Verbose
        if confData.isVerbose is None:
            confData.isVerbose = configHelper.getKeyFromDict(compiler_section, "verbose")
            if confData.isVerbose:
                confData.isVerbose = bool(confData.isVerbose)
        # Load Upload Source
        if confData.uploadSource is None:
            confData.uploadSource = configHelper.getKeyFromDict(uploader_section, "uploadsource")
            if confData.uploadSource:
                confData.uploadSource = bool(confData.uploadSource)
        # Load Uplaod Zip
        if confData.uploadZip is None:
            confData.uploadZip = configHelper.getKeyFromDict(uploader_section, "uploadzip")
            if confData.uploadZip:
                confData.uploadZip = bool(confData.uploadZip)
        # Load Extra Win SCP Commands
        if confData.extraWinScpCmds is None:
            confData.extraWinScpCmds = configHelper.getKeyFromDict(uploader_section, "extraWinScpCmds")
        # Load Updating Assets
        if confData.updatingAssets is None:
            items = configHelper.getKeyFromDict(uploader_section, "updatingassets")
        else:
            items = confData.updatingAssets
        if items:
            confData.updatingAssets = configHelper.splitSafe(items, ",")
        # Load Release Assets
        if confData.releaseAssets is None:
            items = configHelper.getKeyFromDict(uploader_section, "releaseassets")
        else:
            items = confData.releaseAssets
        if items:
            confData.releaseAssets = configHelper.splitSafe(items, ",")
        # Load FTP Time Out
        if confData.ftpTimeout is None:
            confData.ftpTimeout = configHelper.getKeyFromDict(uploader_section, "timeout")
            if confData.ftpTimeout:
                confData.ftpTimeout = int(confData.ftpTimeout)

        config = ConfigParser.ConfigParser()
        config.read(args.authFile)

        # Load FTP Connection Info
        ftp_section = configHelper.configSectionMap(config, "FTP")
        confData.username = configHelper.getKeyFromDict(ftp_section, "username")
        confData.password = configHelper.getKeyFromDict(ftp_section, "password")
        confData.domain = configHelper.getKeyFromDict(ftp_section, "domain")

        # Setting FTP Settings
        ftpHelper.timeOut = confData.ftpTimeout
        ftpHelper.extraWinScpCmds = confData.extraWinScpCmds
        ftpHelper.isVerbose = confData.isVerbose

        # Set Defaults
        confData.appVersionTag = confData.appVersionTag if confData.appVersionTag is not None else defaultAppVersionTag
        confData.appNameTag = confData.appNameTag if confData.appNameTag is not None else defaultAppNameTag
        confData.optimizeAssets = confData.optimizeAssets if confData.optimizeAssets is not None else True
        confData.optimizeHtml = confData.optimizeHtml if confData.optimizeHtml is not None else True
        confData.optimizeCss = confData.optimizeCss if confData.optimizeCss is not None else True
        confData.optimizeJs = confData.optimizeJs if confData.optimizeJs is not None else True
        confData.optimizePng = confData.optimizePng if confData.optimizePng is not None else True
        confData.optimizeJpg = confData.optimizeJpg if confData.optimizeJpg is not None else True
        confData.ftpTimeout = confData.ftpTimeout if confData.ftpTimeout is not None else 20
        confData.targetPath = confData.targetPath if confData.targetPath is not None else ""
    except:
        print sys.exc_info()[0]
    return


def copyAllAssets(item_list, clear):
    if item_list is None:
        return

    if os.path.exists(confData.buildDir):
        if clear is True:
            print printer.title("Clearing: ") + confData.buildDir
            fileUtils.deleteDirRecursive(confData.buildDir)
            os.mkdir(confData.buildDir)
    else:
        os.mkdir(confData.buildDir)

    print printer.title("Copying Assets")

    for item in item_list:
        item_data = item.split(";")
        source_item = os.path.join(compiler_dir, confData.projectRoot, item_data[0])

        if len(item_data) == 2:
            dest_item = os.path.join(compiler_dir, confData.buildDir, item_data[1])
        else:
            dest_item = os.path.join(compiler_dir, confData.buildDir, item_data[0])

        print printer.subTitle("Copying: ") + source_item + printer.subTitle(" -> ") + dest_item

        fileUtils.copyAllRecursive(source_item, dest_item)
    print printer.okGreen("DONE!")
    return


def optimizeAssets(paths):
    if confData.optimizeAssets is not True:
        return
    if paths is None:
        paths = [""]
    elif isinstance(paths, list) is False:
        paths = [paths]
    print printer.title("Optimizing Assets")
    devnull = open(os.devnull, 'wb')
    for path in paths:
        path = path.split(";")
        if len(path) == 2:
            path = path[1]
        else:
            path = path[0]
        path = os.path.join(confData.buildDir, path)
        if os.path.isdir(path):
            for root, dir_names, file_names in os.walk(path):
                for extension in optExtensions:
                    for filename in fnmatch.filter(file_names, '*.' + extension):
                        optimizeAsset(os.path.join(compiler_dir, root), filename, extension, devnull)
        elif os.path.isfile(path):
            file_extension = os.path.splitext(path)
            if len(file_extension) == 2:
                file_extension = file_extension[1][1:]
            else:
                continue
            for extension in optExtensions:
                if file_extension == extension:
                    optimizeAsset("", path, file_extension, devnull)

    devnull.close()
    print printer.okGreen("DONE!")
    return


def optimizeAsset(root, file_name, extension, devnull):
    if devnull is None:
        devnull = open(os.devnull, 'wb')
    file_name = os.path.join(root, file_name)
    print printer.subTitle("Optimizing: ") + file_name
    if extension in cssFormats:
        call_string = '{1} -i "{0}" -o "{0}"'.format(file_name, cssOptPath)
        startProcess(call_string,devnull)
    elif extension in jpgFormats:
        call_string = '"{1}" -copy none -optimize -outfile "{0}" "{0}"'.format(file_name, jpgOptPath)
        startProcess(call_string,devnull)
    elif extension in pngFormats:
        call_string = '"{1}" --force --verbose --ext .png --speed 1 --quality=45-85 "{0}"'.format(file_name, pngOptPath)
        startProcess(call_string,devnull)
    elif extension in jsFormats:
        call_string = 'java -jar "{1}" --js_output_file="{0}" "{0}"'.format(file_name, compilerPath)
        startProcess(call_string,devnull)
    elif extension in htmlFormats:
        temp_file_name = file_name + "temp"
        shutil.copyfile(file_name, temp_file_name)
        os.unlink(file_name)
        call_string = '{1} -o "{2}" "{0}" --collapse-whitespace'.format(temp_file_name, htmlOptPath, file_name)
        startProcess(call_string, devnull)
        os.unlink(temp_file_name)
    else:
        return False
    return True


def startProcess(call_string, devnull):
    if confData.isVerbose:
        subprocess.call(call_string, shell=True)
    else:
        subprocess.call(call_string, stdout=devnull, stderr=subprocess.STDOUT, shell=True)


def injectDebug(items, debug_inject_data):
    if items is None:
        return
    print printer.title("Injecting Debug Files")
    for item in items:
        source_item = os.path.join(compiler_dir, confData.projectRoot, item)
        dest_item = os.path.join(compiler_dir, confData.buildDir, item)

        print printer.subTitle("Copying: ") + source_item + printer.subTitle(" -> ") + dest_item

        fileUtils.copyAllRecursive(source_item, dest_item)
    for injectData in debug_inject_data:
        injectStringToFile(injectData[0], injectData[1], injectData[2], confData.buildDir)
    print printer.okGreen("DONE!")
    return


def injectStrings(inject_datas, root_path):
    if inject_datas is None:
        return
    for injectData in inject_datas:
        injectStringToFile(injectData[0], injectData[1], injectData[2], root_path)


def injectStringToFile(target_file, to_replace, to_inject, root_path):
    if target_file is None:
        return
    inject_to = os.path.realpath(os.path.join(compiler_dir, root_path, target_file))
    if os.path.isfile(inject_to):
        fileUtils.replaceStringInFile(inject_to, to_replace, to_inject)


def injectAppVersion(version, root_path):
    if version is None:
        version = ""
    print printer.title("Injecting App Version")
    for root, dir_names, file_names in os.walk(root_path):
        for filename in file_names:
            filename = os.path.join(compiler_dir, root, filename)
            injectStringToFile(filename, confData.appVersionTag, version, root_path)


def injectAppName(root_path):
    print printer.title("Injecting App Name")
    for root, dir_names, file_names in os.walk(root_path):
        for filename in file_names:
            filename = os.path.join(compiler_dir, root, filename)
            injectStringToFile(filename, confData.appNameTag, confData.appName, root_path)


def bumpVersionNumber():
    if confData.bumpVersion is not True:
        return
    print printer.title("Bumping version number")
    from datetime import datetime
    confData.version = datetime.now().strftime("%Y%m%d%H%M%S%f")
    target_path = os.path.join(compiler_dir, confData.projectRoot, "appVersion.ini")
    target = open(target_path, 'w')
    target.write(confData.version)
    target.close()
    return True


def doInjections():
    # Inject debug to all assets.
    if confData.injectDebug and confData.debugItems and confData.debugInjectData:
        injectDebug(confData.debugItems, confData.debugInjectData)
    # Inject configured tags to all assets.
    if confData.injectData:
        injectStrings(confData.injectData, confData.buildDir)
    injectAppVersion(confData.version, confData.buildDir)
    injectAppName(confData.buildDir)


def uploadUpdatingAssets():
    if confData.updatingAssets is not None:
        print printer.title("Preparing and Uploading uploadingAssets")
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
        for updating_asset in confData.updatingAssets:
            updating_asset = updating_asset.split(";")
            if len(updating_asset) == 2:
                fileUtils.deleteDirRecursive(os.path.join(compiler_dir, confData.buildDir, updating_asset[1]))
            else:
                fileUtils.deleteDirRecursive(os.path.join(compiler_dir, confData.buildDir, updating_asset[0]))


def uploadSource():
    print printer.title("Uploading Source Files")

    print printer.title("Preparing and Uploading normal assets")
    # Copy and prepare normal assets
    copyAllAssets(confData.itemsToCopy, True)
    doInjections()
    optimizeAssets(None)
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
        print printer.title("Preparing and Uploading releaseAssets")

        # Copy and preapre release only assets.
        copyAllAssets(confData.releaseAssets, False)
        doInjections()
        optimizeAssets(confData.releaseAssets)

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
        copyAllAssets(confData.itemsToCopy, True)
        copyAllAssets(confData.releaseAssets, False)
        doInjections()
        optimizeAssets(None)

    if confData.zipPath:
        fileUtils.createZipFile(confData.buildDir, confData.zipPath)
        if confData.uploadZip is True:
            ftpHelper.startUpload(
                confData.zipPath + ".zip",
                confData.domain,
                confData.username,
                confData.password,
                confData.projectRoot,
                confData.targetPath
            )
        raw_input("Press Enter to continue...")
except:
    e = sys.exc_info()[0]
    print e
    raw_input("Exception occurred press Enter to continue...")

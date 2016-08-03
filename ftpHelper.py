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

import os

import commonPaths
import printer
import subprocess

timeOut = 0
extraWinScpCmds = ""
isVerbose = False


def startUpload(paths, domain, username, password, build_dir, target_root_path):
    temp_file = os.path.abspath(os.path.normpath(os.path.join(commonPaths.compiler_dir, "ftpCmd.dat")))
    ftp_data_file = open(temp_file, "w")
    ftp_data_file.write("OPEN ftp://{0}:{1}@{2}\n".format(username, password, domain))
    ftp_data_file.write("option batch continue\n")
    ftp_data_file.write("MKDIR {0}\n".format(target_root_path))
    if isinstance(paths, list) is False:
        paths = [paths]
    print printer.title("Uploading: ") + str(paths) + printer.subTitle(" -> ") + target_root_path
    for path in paths:
        path = path.split(";")
        if len(path) == 2:
            local_path = os.path.realpath(os.path.join(commonPaths.compiler_dir, build_dir, path[1]))
            target_path = os.path.relpath(local_path, os.path.join(commonPaths.compiler_dir, build_dir))
        else:
            local_path = os.path.realpath(os.path.join(commonPaths.compiler_dir, build_dir, path[0]))
            target_path = os.path.relpath(local_path, os.path.join(commonPaths.compiler_dir, build_dir))
        ftp_data_file.write("LCD \"{0}\"\n".format(os.path.join(commonPaths.compiler_dir, build_dir)))
        ftp_data_file.write("CD \"{0}\"\n".format(target_root_path))
        if os.path.isdir(local_path):
            if target_path is None:
                ftp_data_file.write("SYNCHRONIZE remote \"{0}\"\n".format(local_path))
            else:
                ftp_data_file.write("SYNCHRONIZE remote \"{0}\" \"{1}\"\n".format(local_path, target_path))
        else:
            ftp_data_file.write("PUT -neweronly \"{0}\" \"{1}\"\n".format(local_path, target_path))
    ftp_data_file.write("option batch off\n")
    ftp_data_file.write("EXIT\n")

    ftp_data_file.close()
    devnull = open(os.devnull, 'wb')

    call_string = "\"" + os.path.normpath(os.path.join(commonPaths.compiler_dir, "WinSCP.com")) + "\""
    if timeOut > 0 is True:
        call_string += " /timeout={0}".format(timeOut)
    if extraWinScpCmds is not None:
        call_string += extraWinScpCmds
    call_string += " /script=\"{0}\"".format(temp_file)
    if isVerbose:
        subprocess.call(call_string, shell=True)
    else:
        subprocess.call(call_string, stdout=devnull, stderr=subprocess.STDOUT, shell=True)
    devnull.close()
    os.unlink(ftp_data_file.name)
    print printer.okGreen("DONE!")
    return

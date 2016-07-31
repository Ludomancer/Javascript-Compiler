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
import printer
import subprocess

timeOut = 0
extraWinScpCmds = ""
isVerbose = False


def startUpload(paths,domain,username,password,projectRoot, targetPath):
	tempFile = "ftpCmd.dat"
	ftpDataFile = open(tempFile, "w")
	ftpDataFile.write("OPEN ftp://{0}:{1}@{2}\n".format(username,password,domain))
	ftpDataFile.write("option batch continue\n")
	ftpDataFile.write("MKDIR {0}\n".format(targetPath))
	print printer.title("Uploading: ") + paths + printer.subTitle(" -> ") + targetPath
	if isinstance(paths,list) is False:
		paths = [paths]

	for path in paths:
		path = os.path.abspath(path)
		if os.path.isdir(path):
			ftpDataFile.write("SYNCHRONIZE remote {0} {1}\n".format(path, targetPath))
		else:
			fileName = os.path.basename(path)

			ftpDataFile.write("LCD {0}\n".format(projectRoot))
			ftpDataFile.write("CD {0}\n".format(targetPath))
			ftpDataFile.write("PUT -neweronly {0} {1}\n".format(path,fileName))

	ftpDataFile.write("option batch off\n")
	ftpDataFile.write("EXIT\n")

	ftpDataFile.close()
	DEVNULL = open(os.devnull, 'wb')

	callString = "WinSCP.com"
	if timeOut > 0 is True:
		callString += " /timeout={0}".format(timeOut)
	if extraWinScpCmds is not None:
		callString += extraWinScpCmds
	callString += " /script={0}".format(tempFile)

	if isVerbose:
		subprocess.call(callString)
	else:
		subprocess.call(callString, stdout=DEVNULL, stderr=subprocess.STDOUT)
	DEVNULL.close()

	os.remove(tempFile)

	print printer.okGreen("DONE!")
	return

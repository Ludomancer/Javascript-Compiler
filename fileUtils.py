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

import sys
import os
import shutil
import printer


def deleteDirRecursive(dir):
	for root, dirs, files in os.walk(dir):
				for f in files:
					os.unlink(os.path.join(root, f))
				for d in dirs:
					shutil.rmtree(os.path.join(root, d))
	return


def copyAllRecursive(sourceItem,destItem):
	if os.path.isdir(sourceItem):
		shutil.copytree(sourceItem, destItem)
	else:
		shutil.copyfile(sourceItem, destItem)
	return


def replaceStringInFile(filePath, tag,changeTo):
	print printer.title("Injecting " + tag + " with: ") + changeTo + " in " + filePath
	lines = []
	with open(filePath) as infile:
		for line in infile:
			line = line.replace(tag, changeTo)
			lines.append(line)
	with open(filePath, 'w') as outfile:
		for line in lines:
			outfile.write(line)
	print printer.okGreen("DONE!")
	return


def createZipFile(sourceDir, zipPath):
	print printer.title("Creating zip File: ") + zipPath
	try:
		if os.path.exists(zipPath):
			os.remove(zipPath)

		shutil.make_archive(zipPath, 'zip', sourceDir)
	except:
		e = sys.exc_info()[0]
		print e
	print printer.okGreen("DONE!")
	return

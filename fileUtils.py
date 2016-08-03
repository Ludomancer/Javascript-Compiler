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


def deleteDirRecursive(path):
    if os.path.isfile(path):
        os.unlink(path)
        return
    elif os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
        shutil.rmtree(path)
        return


def copyAllRecursive(sourceItem, destItem):
    if os.path.isdir(sourceItem):
        shutil.copytree(sourceItem, destItem)
    elif os.path.isfile(sourceItem):
        shutil.copyfile(sourceItem, destItem)
    return


def replaceStringInFile(file_path, tag, change_to):
    is_injected = False
    lines = []
    with open(file_path) as infile:
        for line in infile:
            if tag in line:
                line = line.replace(tag, change_to)
                is_injected = True
            lines.append(line)
    if is_injected:
        with open(file_path, 'w') as outfile:
            for line in lines:
                outfile.write(line)
        print printer.subTitle("Injected " + tag) + " with: " + printer.subTitle(change_to) + " in " + file_path
    return


def createZipFile(source_dir, zip_path):
    print printer.title("Creating zip File: ") + zip_path
    try:
        if os.path.exists(zip_path):
            os.remove(zip_path)

        shutil.make_archive(zip_path, 'zip', source_dir)
    except:
        e = sys.exc_info()[0]
        print e
    print printer.okGreen("DONE!")
    return

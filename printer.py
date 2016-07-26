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

class BgColors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def title(text):
	return getColorText(BgColors.HEADER,text);

def warn(text):
	return getColorText(BgColors.WARNING,text);

def error(text):
	return getColorText(BgColors.FAIL,text);

def subTitle(text):
	return getColorText(BgColors.BOLD,text);

def okGreen(text):
	return getColorText(BgColors.OKGREEN,text);

def okBlue(text):
	return getColorText(BgColors.OKBLUE,text);

def printInColor(color,text):
	print getColorText(color,text);

def getColorText(color, text):
	return color + text + BgColors.ENDC

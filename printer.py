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
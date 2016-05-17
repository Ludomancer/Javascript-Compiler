import os
import printer
import subprocess

timeOut = 0
extraWinScpCmds = ""
isVerbose = False


def startUpload(path,domain,username,password,projectRoot, targetPath, newFileName):
	path = os.path.abspath(path)
	print printer.title("Uploading: ") + path + printer.subTitle(" -> ") + targetPath
	tempFile = "ftpCmd.dat"
	ftpDataFile = open(tempFile, "w")
	ftpDataFile.write("OPEN ftp://{0}:{1}@{2}\n".format(username,password,domain))
	ftpDataFile.write("option batch continue\n")
	ftpDataFile.write("MKDIR {0}\n".format(targetPath))

	if os.path.isdir(path):
		ftpDataFile.write("SYNCHRONIZE remote {0} {1}\n".format(path, targetPath))
	else:
		if newFileName is None:
			fileName = os.path.basename(path)
		else:
			fileName = newFileName

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

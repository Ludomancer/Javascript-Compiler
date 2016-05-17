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

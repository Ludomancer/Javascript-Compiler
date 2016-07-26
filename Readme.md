# JavaScript Compiler
This project uses **Google Closure**, **WinSCP**, **jpegtran** and **pngquant** to optimize and upload your project depending on the configuration or command line arguments provided.

# Disclaimer
- This project uses several other projects for some of its features. They are not packaged within this repository and should be downloaded from their own websites, see description below for a step by step explanation of this process.
- I've created this tool for my own needs, some features may or may not make sense, feel free to suggest changes or send a pull-request!
- If you think there is something that I've forgot to give credit or a mistake, feel free to contact me.
- **Contribution are welcome**

# Instructions

- **Download** and **Install** [Python 2.7](https://www.python.org/downloads/)
- **Download** [pngquant](https://pngquant.org/).
- **Download** [jpegtran](http://jpegclub.org/jpegtran/).
- **Download** [Google Closure](https://developers.google.com/closure/compiler/).
- **Copy** "jpegtran.exe", "pngquant.exe" and "closure-compiler-v<version-number.jar" to root folder of python scripts.
- **Rename** "closure-compiler-v<version-number.jar" to **compiler.jar**
- **Download** [WinSCP Portable](https://winscp.net/eng/download.php)
- **Copy** WinSCP to root folder of python scripts.
- **Configure** the config.ini file. (See below and sample config.ini in the project.)
- **Create** and **configure** the auth.ini file. (See below)
- **Run** **package.py**

# Configuration Files
# config.ini

**Project Settings**
- **[Project]** = Title for project settings. Required.
- **gamename** = Name of the game, used when injection game name to files defined later.
- **gamekey** = Unique name of the game, works as an id and should not have spaces.
- **projectroot** = Root path of your JavaScript project.
- **builddir** = Where should the JavaScript Compiler export the optimized files.
- **items** = Which Files/Folders should be optimized. Comma separated file name list. Auto rename syntax, <file-name>:<new-file-name>
- **debugitems** = Only included if the debug switch is enabled.
- **debuginjectdata** = Replaces the given tag in given file with the given content. Syntax: <file-name>:<tag>:<new string>

**Compiler Settings**
- **[Compiler]** = Title for compiler settings. Required.
- **verbose** = Should we log more details while running.
- **debug** = Is debug mode enabled as described above.
- **optimize** = Should we optimize .js, .jpg and .png files.
- **zippath** = Where to export the zip file containing the project in the end.

**Uplaoder Settings**
- **[Uploader]** = Title for uploader settings. Required.
- **releaseindex** = index.html file to  be used while releasing the game. You can use "<app-name>" tag in your index file and it will replaced by the gamename variable. Also "<app-version>" will be replaced by the bumped app version.
- **updatingassets** = Assets to be copied to the server while the upload is still going on. An index file saying "Updating..." for example. Files provided here can be renamed automatically with the following Syntax, <file-name>:<new-file-name>.
- **targetpath** = Where to upload the project when the compilation is completed. This should be a directory name not the full path. Directory will be created if doesn't exists.
- **uploadzip** = Should we upload the created zip file.
- **uploadsource** = Should we uploaded the compiled project.
- **timeout** = Time out for WinSCP.

# auth.ini
**FTP Settings**
- **[FTP]** = Title for ftp settings. Required.
- **username** = Username for FTP connection.
- **password** = Password for FTP connection.
- **domain** = Domain for FTP connection.

# Command Line Parameters
**Notes**
- Same as configuring the config.ini file
- Command line options are preferred over config.ini file.
- Add 0 or 1 to toggle options. -o 1 to enabled optimization or -o 0 disable optimization for example.

**Options**
- **-o, --optimize** Meaning = Optimizes assets on export., default=None
- **-d, --debug** Meaning = Add debug scripts to the game., default=None
- **-gk, --gameKey** Meaning = Game Key, default=None
- **-gn, --gameName** Meaning = Game Name. Defaults to Game Key, default=None
- **-v, --verbose** Meaning = Print log, default=None
- **-uo, --uploadOnly** Meaning = Re-upload previous build, default=None
- **-uz, --uploadZip** Meaning = Should we upload the zip file., default=None
- **-us, --uploadSource** Meaning = Should we upload the source files., default=None
- **-bd, --buildDir** Meaning = Where to copy the compiled files., default=None
- **-t, --timeOut** Meaning = FTP timeout., default=None
- **-wsc, --winScpCmd** Meaning = Extra WinSCP commands., default=None
- **-cf, --configFile** Meaning = Choose alternative config file., default=config.ini
- **-af, --authFile** Meaning = Choose alternative auth file., default=auth.ini
- **-ui, --updatingAssets** Meaning = Alternative index.html to be used while updating., default=None
- **-ri, --releaseIndex** Meaning = Alternative index.html to be used when upload is finished., default=None

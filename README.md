# pyBackup
 A simple backup system made with python 3.0.
 This tool has been made with the only purpose to "experiment" with python and operating systems functionalities such as backup tools.
 I'll personally use this tool to make backups on the MEGA remote folder.
 At this version it does not support FTP transfer but i'll work on it in order to make it more secure and resilient to attacks
 such as ransomwares.

## Requirements
dirsync 2.2.5
py7zr 0.9.7

## Installation
This tool needs to be scheduled-run with your operating system task scheduler.
An example of the command to use is referenced below.

##Usage

```console
backup_tool.py -s "C:\\Source" -d "G:\\Destfolder" -j "JobName" -m MantainedBackupNumbers -q base64encodedPassword
```
Everytime you run this command you are basically running jobname that will backup the folder C:\\ source inside the root folder G:\\DestFolder and it will mantain at most MantainedBackupNumbers backups. Every version will be encrypted with 7zip using password base64encodedPassword.
Example of (Real) command:

```console
-s "D:\Research" -d "G:\\" -j "ResearchFolderJob" -m 3 -q bWFzdGVya2V5

```
where bWFzdGVya2V5 = masterkey.

Full help:

```console
Options:
  -h, --help            show this help message and exit
  -s SOURCE, --source=SOURCE
                        Source folder of backup
  -d DEST, --dest=DEST  Destination folder of backup
  -j JOBNAME, --jobname=JOBNAME
                        Name of the job
  -m MAX, --max=MAX     Maximum mantained backup number
  -q PASSWORD, --password=PASSWORD
                        base64 encoded password
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[GPL](https://choosealicense.com/licenses/gpl-3.0/#)

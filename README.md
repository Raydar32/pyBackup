# pyBackup
 A simple backup system made with python 3.0
## Installation
This tool needs to be scheduled-run with your operating system task scheduler.
An example of the command to use is referenced below.

##Usage

'''bash
backup_tool.py -s "C:\\Source" -d "G:\\Destfolder" -j "JobName" -m MantainedBackupNumbers -q base64encodedPassword
'''
Everytime you run this command you are basically running jobname that will backup the folder C:\\ source inside the root folder G:\\DestFolder and it will mantain at most MantainedBackupNumbers backups. Every version will be encrypted with 7zip using password base64encodedPassword.
Example of (Real) command:

'''bash
-s "D:\Research" -d "G:\\" -j "ResearchFolderJob" -m 3 -q bWFzdGVya2V5

'''
where bWFzdGVya2V5 = masterkey.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[GPL](https://choosealicense.com/licenses/gpl-3.0/#)

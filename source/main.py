#!/usr/bin/python
# -*- coding: utf-8 -*-

from dirsync import sync
import os
import py7zr
import shutil
import os.path
import base64
import optparse
import tkinter
import time
from tkinter import messagebox
__version__ = "0.4"

def b64encode(message):    
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')    
    return base64_message

def b64decode(base64_message):  
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    return message

def is_open(file_name):
    if os.path.exists(file_name):
        try:
            os.rename(file_name, file_name) #can't rename an open file so an error will be thrown
            return False
        except:
            return True
    raise NameError
    
class Folder:   

    def __init__(self, path):
        self.path = path
        self.mirrorPath = ''

    def setMirrorPath(self, mirror):
        self.mirrorPath = mirror

    def createMirror(self):
        sync(self.path, self.mirrorPath, 'sync', verbose=True)

    def deleteMirror(self):
        shutil.rmtree(self.mirrorPath)

    def getFolderName(self):
        return self.path.split('\\')[len(self.path.split('\\')) - 1]


def protectFolder(sourceFolder, encKey, target):
    with py7zr.SevenZipFile(target, 'w', password=encKey) as archive:
        archive.writeall(sourceFolder, 'backup')


class BackupJob:

    def __init__(self,sourceFolder,backupPath,jobName):
        '''
        Constructor method of the "BackupJob class."

        Parameters
        ----------
        sourceFolder : string
            source folder of backup.
        backupPath : string
            destination folder of backup (root folder).
        jobName : string
            Name of the job.

        Returns
        -------
        None.

        '''
        self.sourceFolder = sourceFolder
        self.jobName = jobName + '_0'
        self.backupRoot = os.path.join(backupPath, jobName)
        self.syncRoot = os.path.join(backupPath, jobName, 'sync')
        self.encRoot = os.path.join(backupPath, jobName, 'encrypt')
        self.backupZipName = os.path.join(self.encRoot, self.jobName) + '.zip'
        self.mantainedBackupNumber = 1
        self.maxBackups = 3
        self.backupPassword = 'masterkey'
        self.logPath = os.path.join(self.backupRoot,"backup_log.log")
        
        if not os.path.isdir(self.backupRoot):
            os.mkdir(self.backupRoot)

        if not os.path.isdir(self.syncRoot):
            os.mkdir(self.syncRoot)

        if not os.path.isdir(self.encRoot):
            os.mkdir(self.encRoot)
            

    def setMaxMaintainedBackupsNumber(self, num):
        self.maxBackups = num

    def setBackupPassword(self, password):
        self.backupPassword = password

    def setMantainedBackupNumber(self, num):
        self.mantainedBackupNumber = num

    def syncronize(self):
        '''
        This method uses the default operating system "folder mirroring" technique
        in order to syncronize source with dest.

        Returns
        -------
        None.

        '''
        self.sourceFolder.setMirrorPath(self.syncRoot)
        self.sourceFolder.createMirror()


    def cleanBackupFolder(self):
        '''
        This method cleans the backup folder, it uses the method 
        renameMantainedBackups() to manatain an ordered list of the 
        backups.
        
        Returns
        -------
        None.

        '''
        
        cartella = self.encRoot
        a = os.listdir(cartella)
        if len(a) > self.maxBackups:    
            aClean = [i.split('_') for i in a]
            for item in aClean:
                item[1] = item[1].replace(".zip","")
                item[1] = int(item[1])
            aClean = sorted(aClean, key=lambda a_entry: a_entry[1])
            #first element → oldest element
            actualFile = os.path.join(self.encRoot, a[0]) 
            
            #testing that file is not opened
            while is_open(actualFile):
                time.sleep(5)
            try:                   
                os.remove(actualFile)      
            except:
                payload = "Error in accessing file  " + actualFile + "\n Backup process skipped."
                messagebox.showerror("Backup Error", payload )            
            del a[0]

            
    def getCurrentBackupNumber(self):
        '''
        This method returns the lastest backup number that has been saved.

        Returns
        -------
        int
            last number.

        '''
        a = os.listdir(self.encRoot)
        if not a:
            return -1
        a.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))
        lastNum = a[len(a) - 1].replace('.zip', '').split('_')[1]
        return int(lastNum)
    

    def doBackup(self):
        self.cleanBackupFolder()
        self.syncronize()        
        current_milli_time = lambda: int(round(time.time() * 1000))
        protectFolder(self.syncRoot, 
                      b64decode(self.backupPassword),
                      os.path.join(self.encRoot,self.jobName.replace('_0', '_'+ str(current_milli_time()) + '.zip'
                      )))
      

def main():
    '''
    Main method.

    Returns
    -------
    None.

    '''
    root = tkinter.Tk()
    root.withdraw()

    parser = optparse.OptionParser()
    parser.add_option('-s', '--source', action="store", dest="source", help="Source folder of backup")
    parser.add_option('-d', '--dest', action="store", dest="dest", help="Destination folder of backup")
    parser.add_option('-j', '--jobname', action="store", dest="jobname", help="Name of the job")
    parser.add_option('-m', '--max', action="store", dest="max", help="Maximum mantained backup number")
    parser.add_option('-q', '--password', action="store", dest="password", help="base64 encoded password")
    
    options, args = parser.parse_args()
    
    Old = Folder(options.source)
    backup = BackupJob(Old, options.dest, options.jobname)
    backup.setBackupPassword(options.password)            
    backup.setMaxMaintainedBackupsNumber(int(options.max))
    backup.doBackup()


if __name__ == '__main__':
    main()

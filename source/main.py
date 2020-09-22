# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from dirsync import sync
import os
import py7zr
import shutil
import os.path
import base64


class Folder:
    def __init__(self, path):
        self.path = path
        self.mirrorPath = ""
    
    def setMirrorPath(self,mirror):
        self.mirrorPath = mirror

    def createMirror(self):         
        sync(self.path,self.mirrorPath,"sync",verbose=True)
        
    def deleteMirror(self):
        shutil.rmtree(self.mirrorPath)
    
    def getFolderName(self):
        return self.path.split("\\")[len(self.path.split("\\"))-1]
    
    
def protectFolder(sourceFolder, encKey,target):      
    with py7zr.SevenZipFile(target, 'w', password=encKey) as archive:
        archive.writeall(sourceFolder, "backup")  
        
        
class BackupJob:
    def __init__(self,sourceFolder,backupPath,jobName):
        self.sourceFolder = sourceFolder
        self.jobName = jobName + "_0"
        self.backupRoot = os.path.join(backupPath,jobName)
        self.syncRoot = os.path.join(backupPath,jobName,"sync")
        self.encRoot = os.path.join(backupPath,jobName,"encrypt")
        self.backupZipName = os.path.join(self.encRoot,self.jobName) + ".zip"
        self.mantainedBackupNumber = 1 
        self.maxBackups = 3
        self.backupPassword = "masterkey"
        
        # Predispongo l'ambiente per il backup 
        
        if(not os.path.isdir(self.backupRoot)):
            os.mkdir(self.backupRoot)
            
        if(not os.path.isdir(self.syncRoot)):
            os.mkdir(self.syncRoot)
            
        if(not os.path.isdir(self.encRoot)):
            os.mkdir(self.encRoot)
    def setMaxMaintainedBackupsNumber(self,num):
        self.maxBackups = num
        
    def setBackupPassword(self,password):
        self.backupPassword = password
    
    def renameMantainedBackups(self):   #Rinomina i backup in _0, _1 ... 
        cartella = self.encRoot
        a = os.listdir(cartella)
        aClean = [i.split("_")[0] for i in a]
        current = 0
        for i in aClean:
            aClean[current] = aClean[current] + "_" + str(current) + ".zip"
            os.rename(os.path.join(cartella,a[current]),os.path.join(cartella,aClean[current]))
            current = current + 1 

    def setMantainedBackupNumber(self,num):
        self.mantainedBackupNumber = num
        
    def syncronize(self):
        self.sourceFolder.setMirrorPath(self.syncRoot)
        self.sourceFolder.createMirror()
    
    def cleanBackupFolder(self):
        a = os.listdir(self.encRoot)
        if len(a)>self.maxBackups:
            os.remove(os.path.join(self.encRoot,a[0]))
            print("Rimosso: ",os.path.join(self.encRoot,a[0]))
            del a[0]
            self.renameMantainedBackups()
    
    def getCurrentBackupNumber(self):
        a = os.listdir(self.encRoot)
        if( not a ):
            return -1        
        a.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))
        lastNum = a[len(a)-1].replace(".zip","").split("_")[1]
        return int(lastNum)
        
    def doBackup(self):     
        self.syncronize()
        self.cleanBackupFolder()
        protectFolder(self.syncRoot,self.backupPassword, os.path.join(self.encRoot,self.jobName.replace("_0","_" + str(self.getCurrentBackupNumber() + 1) + ".zip")))
        
def main():
    Old = Folder("G:\\Old\\amore")    
    backup = BackupJob(Old,"G:\\","BackupJob")
    backup.setBackupPassword("pass")
    backup.setMaxMaintainedBackupsNumber(7)
    backup.doBackup()

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
if __name__ == "__main__":
    main()


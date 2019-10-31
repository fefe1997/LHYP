#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Install pydicom library
get_ipython().system('pip install -U pydicom')


# In[2]:


# Import libraries that I use 
import os
import pydicom as dicom
import pickle
import numpy as np
import re


# In[2]:


# Patient object implementation
class Patient:

    # Attributes
    laImages = []
    saImages = []
    gender = None
    weight = None
    hasHCM = False
    Normal = False
    hasother = False
    
    def __init__(self, patientDirectory):  

        for files in os.listdir(patientDirectory):
            # Load the la images
            if files == "la":
                laDirectory = patientDirectory + "/la"
                self.addNumpyLaImages(laDirectory)
            
            # Load sa images
            if files == "sa":
                saDirectory = patientDirectory + "/sa"
                self.setGender(saDirectory + "/contours.con")
                self.setWeight(saDirectory + "/contours.con")
                self.addNumpySaImages(saDirectory + "/images")
            
            # Checks the disease
            if files == "meta.txt":
                txtFile = patientDirectory +"/meta.txt"
                self.hasDisease(txtFile)
                
            
    # Checks the txt file and set the patient disease
    def hasDisease(self, txtFile):
        text = open(txtFile, "r")
        line = text.readline()
        if "HCM" in line:
            self.hasHCM=True
        elif "NORM" in line: 
            self.Normal=True
        else: 
            self.hasother=True

    # Convert dicom file to numpy array
    def dicomToNumpy(self, dicomFile):
        ds = dicom.read_file(dicomFile)
        return np.array(ds.pixel_array)
    
    
    # Reads the dicom files from la directory
    def addNumpyLaImages(self, laDirectory):
        os.chdir(laDirectory)
        for dicoms in os.listdir(laDirectory):
            if(dicoms.endswith('.dcm') and len(self.laImages) < 10):
                self.laImages.append(self.dicomToNumpy(dicoms))
    
    # Reads the dicom files from sa directory
    def addNumpySaImages(self, saDirectory):
        os.chdir(saDirectory)
        for dicoms in os.listdir(saDirectory):
            if(dicoms.endswith('.dcm') and len(self.saImages) < 10):
                self.saImages.append(self.dicomToNumpy(dicoms))
    
    # Set the gender attribute with the help of the .con file
    def setGender(self, conFile):
        if os.path.isfile(conFile):
            with open(conFile, "r") as fp:
                for line in fp:
                    if re.match("Patient_gender=(.*)", line):
                        line = re.split('=', line)
                        gender = line[1].replace('\n','')
                        self.gender = gender
       
    
    def setWeight(self, conFile):
        if os.path.isfile(conFile):
            with open(conFile, "r") as fp:
                for line in fp:
                    if re.match("Patient_weight=[0-9]+",line):
                        line = re.split("[,=. \-!?:]+", line)
                        weight = line[1]
                        self.weight = weight


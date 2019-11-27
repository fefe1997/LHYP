#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Install pydicom library
get_ipython().system('pip install -U pydicom')

# Import libraries that I use 
import os
import pydicom as dicom
import pickle
import numpy as np
import re
import logging


# In[ ]:


# Global functions that help reading images

# Get all slice locations from an image directory
def getSliceLocations(directory):
        os.chdir(directory)
        sliceLocations = []
        for dicomFile in os.listdir(directory):
            if dicomFile.endswith('.dcm'):
                try:
                    ds = dicom.dcmread(dicomFile)
                    sliceLocations.append(ds.SliceLocation)
                except:
                    logging.error('Something went wrong during reading the slice locations in ' 
                                  + directory + ' directory with this dicom file: ' + dicomFile)
        sliceLocations = set(sliceLocations)
        sliceLocations = list(sliceLocations)
        sliceLocations.sort()
        return sliceLocations


# Get the middle part of the slice locations
def reduceSliceLocations(sliceLocation):
    validSliceLocations = sliceLocation
    if len(validSliceLocations) < 3:
        logging.info('The slicelocation is less than 3')
        return validSliceLocations
    while len(validSliceLocations) > int(len(sliceLocation)/3):
        validSliceLocations = validSliceLocations[1:-1]
    return validSliceLocations


# Get the dicom images from the middle of the MRI slices
def addDicomImagesToArray(dicomDirectory):
    dicomImages = []
    sliceLocations = getSliceLocations(dicomDirectory)
    validSliceLocations = reduceSliceLocations(sliceLocations)
    os.chdir(dicomDirectory)
    for dicomFile in os.listdir(dicomDirectory):
        if dicomFile.endswith('.dcm') and len(dicomImages) < 10:
            try:
                ds = dicom.dcmread(dicomFile)
                if ds.SliceLocation in validSliceLocations:
                    logging.info('Appended an image to dicomImage: ' + dicomFile +' in ' + dicomDirectory)
                    dicomImages.append(np.array(ds.pixel_array))
            except:
                logging.error('Something went wrong in addDicomImagesToArray() in ' + dicomDirectory +
                              'during reading ' + dicomFile)
    return dicomImages


# In[1]:


# Patient object implementation
class Patient:

    def __init__(self, patientDirectory):
        
        # Attributes
        self.laImages = []
        self.saImages = []
        self.gender = None
        self.weight = None
        self.hasHCM = False
        self.Normal = False
        self.hasOther = False

        for files in os.listdir(patientDirectory):
            # Load the la images
            if files == "la":
                laDirectory = patientDirectory + "/la"
                self.laImages = addDicomImagesToArray(laDirectory)
            
            # Load sa images
            if files == "sa":
                saDirectory = patientDirectory + "/sa"
                self.setGender(saDirectory + "/contours.con")
                self.setWeight(saDirectory + "/contours.con")
                self.saImages = addDicomImagesToArray(saDirectory + "/images")
            
            # Checks the disease
            if files == "meta.txt":
                txtFile = patientDirectory +"/meta.txt"
                self.hasDisease(txtFile)
    
    
    # Getters
    def getGender(self):
        return self.gender
    
    
    def getWeight(self):
        return self.weight
    
    
    def getHasHCM(self):
        return self.hasHCM
    
    
    def getNormal(self):
        return self.Normal
    
    
    def getHasOther(self):
        return self.hasOther
    
    
    def getLaImages(self):
        return self.laImages
    
    
    def getSaImages(self):
        return self.saImages
         
    
    # Checks the txt file and set the patient disease
    def hasDisease(self, txtFile):
        text = open(txtFile, "r")
        line = text.readline()
        text.close()
        if "HCM" in line:
            self.hasHCM=True
        elif "NORM" in line: 
            self.Normal=True
        else: 
            self.hasOther=True    
    
    
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


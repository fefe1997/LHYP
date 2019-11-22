#!/usr/bin/env python
# coding: utf-8

# In[31]:


# Install pydicom library
get_ipython().system('pip install -U pydicom')


# In[37]:


# Import libraries that I use 
from Patient import Patient
import os
import pickle
import numpy as np


# In[38]:


# Root directory is where the patients' file are stored
# Target directory is where you would like to write the byte files
def readAllPatientToBytes(rootDirectory,targetDirectory):

    patientList = []
    
    # Iterate through the files of the patients
    for dirs in os.listdir(rootDirectory):
        patientDirectory = rootDirectory + "/" + dirs
        patientList.append(Patient(patientDirectory))

    # Save the patient objects to the target directory as a byte file
    os.chdir(targetDirectory)
    for i in range(len(patientList)):
        pickle.dump(patientList[i], open("Patient" + str(i), "wb+"))


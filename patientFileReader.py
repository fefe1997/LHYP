#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Install pydicom library
get_ipython().system('pip install -U pydicom')


# In[28]:


# Import libraries that I use 
from patient import Patient
import os


# In[29]:


# Root directory is where the patients' file are stored
# Target directory is where you would like to write the byte files
def readAllPatientToBytes(rootDirectory,targetDirectory):

    patientList = []
    
    # Iterate through the files of the patients
    for dirs in os.listdir(rootDirectory):
        patientDirectory = rootDirectory + "/" + dirs
        patientList.append( Patient(patientDirectory))

    # Save the patient objects to the target directory as a byte file
    os.chdir(targetDirectory)
    for i in range(len(patientList)):
        pickle.dump(patientList[i], open("Patient" + str(i), "wb+"))


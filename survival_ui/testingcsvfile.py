import pandas as pd
import pydicom
from PIL import Image
from matplotlib import pyplot as plt

data = pd.read_csv(r'DICOMFiles.csv')
data = data.dropna(axis=0)
df = data
# radiologydata
# image1 = Image.open('radiologicalImages/'+df['Radiology Image'].head(1).values[0])
# pass_dicom = 'radiologicalImagesDICOM/' + df['Radiology Image'].head(1).values[0]  # file name is 1-12.dcm
# print(pass_dicom)
# filename = pydicom.data.data_manager.get_files(pass_dicom)
# print(filename)
# ds = pydicom.dcmread(pass_dicom)
# plt.imshow(ds.pixel_array, cmap=plt.cm.bone)  # set the color map to bone
# filenamep = df['Radiology Image'].head(1).values[0].strip(".dcm")
# plt.savefig(filenamep + ".png")
# image1 = Image.open(filenamep + ".png")
for index, row in df.iterrows():
    print(row['Radiology Image'], row['Pathology Image'])
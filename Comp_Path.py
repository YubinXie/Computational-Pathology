import os
import subprocess
import Sample_Preprocess
import re
import sys
import numpy as np
print os.getcwd()
import Check_Label
import Collect_Img
import Overlay
import Preprocess_V2
import Preprocess_V3
import gc
import time
start_time = time.time()

def main():
    #Collect_Img.label()
    #CheckLabel()
    #Preprocess()
    #OverLay()
    #PreprocessV2()
    #PreprocessV3()
    Projection()
    print("--- %s seconds ---" % (time.time() - start_time))


def OverLay():
    with open ("Sample_List.txt") as OpenSampleList:
        for line in OpenSampleList:
            imagemarker = ""
            if "k" in line:
                imagemarker = "k;"
            if "l" in line:
                imagemarker = "l;"
            target = re.search('(\d+)',line)
            if(target):
                image = target.group(0)
                print image
                Overlay.main("../RawInput/Selected_3/","./Label_resize/", imagemarker,image, "../RawInput/Overlay_3/")

            gc.collect()

def CollectLabel(LabelMark):
    LabelMarkList = ["k","l","p","v"]
    LabelNameList = ["huangk", "mirsadrl", "pengy", "werneckv"]
    with open ("Sample_List.txt") as OpenSampleList:
        for line in OpenSampleList:
            if LabelMarkList[LabelMark] in line:
                Collect_Img.label()
                gc.collect()




def CheckLabel():
    with open ("Sample_List.txt") as OpenSampleList:
        for line in OpenSampleList:
            Color={}
            original_img=[]
            line=line.strip("\n")
            if "k" in line or "l" in line:
                Check_Label.main("Label/",line+".bmp")

def PreprocessV2():
    OutputFolder = "RawInput/"
    with open ("Sample_List.txt","r") as OpenSampleList:
        number = 0
        for line in OpenSampleList:
            target = re.search('(\d+)',line)
            if(target):
                number+=1
                SampleID = target.group(0)
                Preprocess_V2.main("../RawInput/Tissue/",SampleID,"../Output/08112017/")

def PreprocessV3():
    OutputFolder = "../Selected_output/"
    OverlayInputFolder = "../RawInput/Overlay_3/"
    SampleInputFolder = "../RawInput/Selected_3/"
    LabelInputFolder = "Label_resize/"
    LabelMarkers = ""
    with open ("Sample_List.txt","r") as OpenSampleList:
        number = 0
        for line in OpenSampleList:
            if "k" in line:
                LabelMarkers = "k;"
            if "l" in line:
                LabelMarkers = "l;"
            target = re.search('(\d+)',line)
            if(target):
                image = target.group(0)
            Preprocess_V3.main(SampleInputFolder,OverlayInputFolder,LabelInputFolder,LabelMarkers,image,OutputFolder)

def Preprocess():
    OutputFolder = "RawInput/"
    with open ("Sample_List.txt","r") as OpenSampleList:
        number = 0
        for line in OpenSampleList:
            target = re.search('(\d+)',line)
            if(target):
                number+=1
                SampleID = target.group(0)
                Sample_Preprocess.main("../RawInput/Tissue/",SampleID,"../RawInput/Box")


def Projection():
    WorkingFolder = "../Selected_output/"
    Allfiles = [file[19:27] for file in os.listdir(WorkingFolder) if "Segmentated_Thinned" in file]
    #print Allfiles
    Uniquefile = np.unique([ID[:6] for ID in Allfiles])
    #print Uniquefile
    for ID in Uniquefile:
        IDlist = [file for file in Allfiles if ID in file]
        print IDlist


if __name__ == '__main__':
  main()

import os
import subprocess
import Sample_Preprocess
import re
print os.getcwd()
import Check_Label
import Collect_Img
import Overlay
import Preprocess_V2
import gc
import time
start_time = time.time()

def main():
    #Collect_Img.label()
    #CheckLabel()
    #Preprocess()
    OverLay()
    #PreprocessV2()
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
                Overlay.main("../RawInput/Tissue/","Label/", imagemarker,image, "../RawInput/Overlay/")

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


if __name__ == '__main__':
  main()

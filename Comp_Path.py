import os
import subprocess
import Sample_Preprocess
import re
print os.getcwd()
import Check_Label
import Collect_Img

def main():
    #Collect_Img.label()
    CheckLabel()

def CollectLabel(LabelMark):
    LabelMarkList = ["k","l","p","v"]
    LabelNameList = ["huangk", "mirsadrl", "pengy", "werneckv"]
    with open ("Sample_List.txt") as OpenSampleList:
        for line in OpenSampleList:
            if LabelMarkList[LabelMark] in line:
                Collect_Img.label()




def CheckLabel():
    with open ("Sample_List.txt") as OpenSampleList:
        for line in OpenSampleList:
            Color={}
            original_img=[]
            line=line.strip("\n")
            if "k" in line or "l" in line:
                Check_Label.main("Label/",line+".bmp")


def Preprocess():
    OutputFolder = "RawInput/"
    with open ("../Sample_List.txt","r") as OpenSampleList:
        number = 0
        for line in OpenSampleList:
            target = re.search('(\d+)',line)
            if(target):
                number+=1
                SampleID = target.group(0)
                if SampleID != "521175":
                    continue
                    print SampleID
                    Sample_Preprocess.main("../RawInput/Tissue/",SampleID,"../RawInput/")
                else:
                    print line, "not found"


if __name__ == '__main__':
  main()

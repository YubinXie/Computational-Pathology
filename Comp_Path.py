import os
import subprocess
import Sample_Preprocess
import re
print os.getcwd()


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

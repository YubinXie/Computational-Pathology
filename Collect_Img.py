import urllib, cStringIO
import re
from PIL import Image

def main():
    locallabel()

def label():
    URLlink = "http://slides.mskcc.org/slides/pengy@mskcc.org/19;p;403769.svs/getLabelFileBMP"
    files = cStringIO.StringIO(urllib.urlopen(URLlink).read())
    img = Image.open(files)
    #w,l = img.size
    print w,l
    #new_imh=img.resize(1280,)

def locallabel():

    files = "RawInput/403769.svs_labels_pengy@mskcc.org.BMP"
    img = Image.open(files)
    #w,l = img.size
    #print w,l
    #new_imh=img.resize(1280,)



def sample():
    OutputFolder = "RawInput/"
    with open ("Sample_List.txt","r") as OpenSampleList:
        number = 0
        for line in OpenSampleList:
            target = re.search('(\d+)',line)
            if(target):
                number+=1
                SampleID = target.group(0)
                print SampleID
                urllib.urlretrieve("http://slides.mskcc.org/thumbnail/xiey@mskcc.org/aperio;" +SampleID + "/jpg/null/1280/1280", OutputFolder + SampleID + ".jpg")
            else:
                print line, "not found"
    print number, "found"


if __name__ == '__main__':
  main()

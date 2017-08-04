import urllib, cStringIO
import re
import PatchedPIL
from PatchedPIL import Image, ImageFile, BmpImagePlugin, ImagePalette
from matplotlib import pyplot as plt

def main():
    label()

def label():
    with open ("Sample_List.txt","r") as OpenSampleList:
        number = 0
        for line in OpenSampleList:
            target = re.search('k;(\d+).svs',line) #l;
            if(target):
                number+=1
                SampleID = target.group(0)
                print SampleID
                img=None
                URLlink=("http://slides.mskcc.org/slides/huangk@mskcc.org/19;" +SampleID + "/getLabelFileBMP") #
                try:
                    img = Image.open(cStringIO.StringIO(urllib.urlopen(URLlink).read()))
                except:
                    pass
                if img == None:
                    print SampleID, "no label"
                    continue
                w,l = img.size
                #print img[1,1]
                length=int(1280.0/float(w)*float(l))
                print length
                new_img=img.resize((1280,length))
                new_img.save("" + SampleID + ".bmp")

                #plt.imsave("../Output/Label/" + SampleID + ".bmp",new_img)
                break
            else:
                print line, "not found"
    #URLlink = "http://slides.mskcc.org/slides/pengy@mskcc.org/19;p;403769.svs/getLabelFileBMP"


def locallabel():

    files = "../RawInput/403769.svs_labels_pengy@mskcc.org.bmp"
    img = Image.open(files)
    w,l = img.size
    print w,l
    length=int(1280.0/float(w)*float(l))
    print length
    new_img=img.resize((1280,537))
    plt.imsave("../Output/test.bmp",new_img)



def sample():
    OutputFolder = "RawInput/"
    with open ("../Sample_List.txt","r") as OpenSampleList:
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

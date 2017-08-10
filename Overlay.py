from PIL import Image
from skimage import img_as_ubyte
import numpy as np
from matplotlib import pyplot as plt


SampleInputFolder = "../RawInput/Tissue/"
LabelInputFolder =  "../RawInput/Label/"
OutputFolder = "../RawInput/Overlay/"
image = "507065"
imagemarker = "l;"
def main(SampleInputFolder,LabelInputFolder, imagemarker,image, OutputFolder):
    try:
        Org_Lable_Img= img_as_ubyte(Image.open(LabelInputFolder + imagemarker + image + ".svs.bmp"))
        Org_Sample_Img = img_as_ubyte(Image.open(SampleInputFolder + image + ".jpg"))

        Org_Lable_Img = Org_Lable_Img[:,:,0:3]

        width, length, height= Org_Sample_Img.shape
        Sample_Mixed=np.zeros(shape=(width, length, height))
        for l in range(length):
            for w in range(width):
                if Org_Lable_Img[w,l,0]>=255 & Org_Lable_Img[w,l,1]>=255 & Org_Lable_Img[w,l,2]>=255:
                    Sample_Mixed[w,l]=(Org_Sample_Img[w,l])
                else:
                    Sample_Mixed[w,l]=(Org_Lable_Img[w,l])*0.3+(Org_Sample_Img[w,l])*0.7
        Sample_Mixed=Sample_Mixed.astype(np.uint8)
        plt.imsave(OutputFolder+"Overlay_"+image +"_alpha0.3.png",Sample_Mixed)
    except Exception, e:
        print "Errors when processing "+ image
        print e
        pass


if __name__ == '__main__':
  main(SampleInputFolder,LabelInputFolder, imagemarker,image, OutputFolder)

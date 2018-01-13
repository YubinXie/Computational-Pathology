from PIL import Image
from skimage import img_as_ubyte
import numpy as np
from matplotlib import pyplot as plt


SampleInputFolder = "../RawInput/Selected_3/"
LabelInputFolder =  "./Label_resize/"
OutputFolder = "../RawInput/Overlay_3/"
image = "465063"
imagemarker = "k;"
def main(SampleInputFolder,LabelInputFolder, imagemarker,image, OutputFolder):
    Color=np.array([[255,255,255],[255,255,0],[0,255,0],[0,0,255],[255,0,50],[0,255,255],[255,0,255]])
    try:
        Org_Lable_Img= (Image.open(LabelInputFolder + imagemarker + image + ".svs.bmp"))
        Lable_Img=Org_Lable_Img.load()
        Org_Sample_Img = img_as_ubyte(Image.open(SampleInputFolder + image + ".jpEg"))
        print Org_Lable_Img.size, Org_Sample_Img.shape
            #Org_Lable_Img = Org_Lable_Img[:,:,]

        width, length, height= Org_Sample_Img.shape
        Sample_Mixed=np.zeros(shape=(width, length,height))
        for l in range(length):
            for w in range(width):
                if Lable_Img[l,w] ==0:
                    Sample_Mixed[w,l]=(Org_Sample_Img[w,l])
                else:
                    #print (Lable_Img[l,w]), Org_Sample_Img[w,l]
                    Sample_Mixed[w,l]=(Org_Sample_Img[w,l])*0.6+Color[Lable_Img[l,w]]*0.4
        Sample_Mixed=Sample_Mixed.astype(np.uint8)
        plt.imsave(OutputFolder+"Overlay_"+image +"_alpha0.4.png",Sample_Mixed)
    except Exception, e:
        print "Errors when processing "+ image
        print e
        pass


if __name__ == '__main__':
  main(SampleInputFolder,LabelInputFolder, imagemarker,image, OutputFolder)

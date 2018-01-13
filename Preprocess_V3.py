import cv2
import scipy
import numpy as np
from PIL import Image
import sys
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
from skimage.morphology import thin, closing, square, skeletonize
from skimage.util import invert
from skimage.color import rgb2gray, label2rgb
from skimage import data,img_as_ubyte
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops

OutputFolder = '../Selected_output/'
SampleInputFolder = '../RawInput/Selected_3/'
LabelInputFolder = './Label_resize/'
OverlayInputFolder = '../RawInput/Overlay_3/'
LabelMarkers = "l;"
image = "414191"

def main(SampleInputFolder,OverlayInputFolder,LabelInputFolder,LabelMarkers,image,OutputFolder):
    try:
        # Loading
        print "Processing "+ image
        Sample_Img = cv2.imread(SampleInputFolder + image + ".jpeg" , 0)
        Org_Overlay_Img = img_as_ubyte(Image.open(OverlayInputFolder + "Overlay_" + image + "_alpha0.4.png"))
        Org_Sample_Img = img_as_ubyte(Image.open(SampleInputFolder + image + ".jpeg"))
        Org_Label_Img = Image.open(LabelInputFolder+LabelMarkers+image+".svs.bmp")
        #LabeL_Img=Org_Label_Img.load()


        kernel = np.ones((5,5),np.uint8)
        kernel_size=str(kernel.shape)
        ReginThreshold=5000
        GaussianValue=(15,15)
        ## Sample thinning
        # Otsu's thresholding after Gaussian filtering
        blur = cv2.GaussianBlur(Sample_Img,GaussianValue,0)
        #plt.imsave(OutputFolder+"blur_"+image+".png",blur,cmap=plt.cm.gray)

        ret1,th1 = cv2.threshold(blur,0,255,cv2.THRESH_OTSU)
        #plt.imsave(OutputFolder+"OTSU_"+image+".png",th1,cmap=plt.cm.gray)

        Sample_Closing = cv2.morphologyEx(th1, cv2.MORPH_CLOSE, kernel)
        #plt.imsave(OutputFolder+"closing_"+image+".png",Sample_Closing,cmap=plt.cm.gray)

        Sample_Closing_Inverted_Gray = rgb2gray(invert(Sample_Closing))
        Sample_Closing_Inverted_Binary=np.where(Sample_Closing_Inverted_Gray>np.mean(Sample_Closing_Inverted_Gray),1,0)

        Pre_Thinned = thin(Sample_Closing_Inverted_Binary)#, max_iter=100000) #skeletonize

        w,l = Sample_Closing_Inverted_Binary.shape
        print w,l,Org_Overlay_Img.shape
        Overlay_Thin=np.zeros(Org_Overlay_Img.shape)
        for width in range(w):
            for length in range(l):
                #print width,length
                if Pre_Thinned[width,length]==0:
                    Overlay_Thin[width,length] = Org_Overlay_Img[width,length]
                    #print Org_Overlay_Img[width,length]
                else:
                    Overlay_Thin[width,length] = (0,0,0,255)
        Sample_Closing_Inverted_Binary_Expanded=np.insert(Sample_Closing_Inverted_Binary,[l-1]*10,0,axis=1)
        Sample_Closing_Inverted_Binary_Expanded=np.insert(Sample_Closing_Inverted_Binary_Expanded,[0]*10,0,axis=1)
        Sample_Closing_Inverted_Binary_Expanded=np.insert(Sample_Closing_Inverted_Binary_Expanded,[w-1]*10,0,axis=0)
        Sample_Closing_Inverted_Binary_Expanded=np.insert(Sample_Closing_Inverted_Binary_Expanded,[0]*10,0,axis=0)
        #print Org_Sample_Img
        Org_Sample_Img=np.insert(Org_Sample_Img,[l-1]*10,255,axis=1)
        Org_Sample_Img=np.insert(Org_Sample_Img,[0]*10,255,axis=1)
        Org_Sample_Img=np.insert(Org_Sample_Img,[w-1]*10,255,axis=0)
        Org_Sample_Img=np.insert(Org_Sample_Img,[0]*10,255,axis=0)
        #print Org_Sample_Img
        print Sample_Closing_Inverted_Binary_Expanded.shape
        Thinned = thin(Sample_Closing_Inverted_Binary_Expanded, max_iter=100000)


        #BoundingBox(ReginThreshold):
        thresh = threshold_otsu(Sample_Closing_Inverted_Binary_Expanded)
        bw = closing(Sample_Closing_Inverted_Binary_Expanded > thresh, square(3))
        ## remove artifacts connected to image border
        cleared = clear_border(bw)
        ##  label image regions
        label_image = label(cleared)
        image_label_overlay = label2rgb(label_image, image=Sample_Closing_Inverted_Binary_Expanded)
        number=0
        fig, ax = plt.subplots(figsize=(10, 6))
        Overlay_Thin=Overlay_Thin.astype(np.uint8)
        ax.imshow(Overlay_Thin,cmap=plt.cm.gray)
        plt.imsave(OutputFolder+"Thinned_"+image+".png",Thinned,cmap=plt.cm.gray)
        for region in regionprops(label_image):
            if region.area >= ReginThreshold:
                print "Region AREA:",region.area
                NewImage=np.zeros((w+20,l+20))
                OriImage=np.zeros((w+20,l+20,3))
                Coords= region.coords
                #scipy.misc.imsave(str(number)+'outfile.jpg', NewImage)
                minr, minc, maxr, maxc = region.bbox
                Box_Sample_OrgImg = Org_Sample_Img[max(0,minr-10):min(maxr+10,w+19), max(minc-10,0):min(maxc+10,l+19)]
                width, length, height= Box_Sample_OrgImg.shape
                #NewImage=np.zeros((width, length))

                for list in range(len(Coords)):
                    NewImage[Coords[list][0],Coords[list][1]] = Sample_Closing_Inverted_Binary_Expanded[ Coords[list][0],Coords[list][1]]
                    OriImage[Coords[list][0],Coords[list][1]] = Org_Sample_Img[ Coords[list][0],Coords[list][1]]
                Box_Sample = thin(NewImage, max_iter=100000)
                BoxOriImage = OriImage[max(0,minr-10):min(maxr+10,w+19), max(minc-10,0):min(maxc+10,l+19)]
                Box_NewImage =NewImage[max(0,minr-10):min(maxr+10,w+19), max(minc-10,0):min(maxc+10,l+19)]
                Box_Sample=Box_Sample[max(0,minr-10):min(maxr+10,w+19), max(minc-10,0):min(maxc+10,l+19)]
                Box_Sample = np.where(Box_Sample>np.mean(Box_Sample),1,0)
                Box_Label = Org_Label_Img.crop(( max(minc-20,0),max(0,minr-20),min(maxc,l+19),min(maxr,w+19)))
                Box_Label.save(OutputFolder+"Segmentated_Label"+image+"_"+str(number) +".bmp")
                #Box_Sample = Sample_Thinned[max(0,minr-10):min(maxr+10,w), max(minc-10,0):min(maxc,l+10)]
                rect = mpatches.Rectangle((max(minc-10,0), max(minr-10,0 )), maxc - minc+10, maxr - minr+10,
                                    fill=False, edgecolor='red', linewidth=1)
                ax.add_patch(rect)
                #print Box_Sample_OrgImg.shape,Box_Sample.shape,width, length, height
                #Mix the sample and label file
                Sample_Mixed=np.zeros(shape=(width, length, height))
                for x in range(width):
                    for y in range(length):
                        if Box_Sample[x,y]==0:
                            Sample_Mixed[x,y]=(Box_Sample_OrgImg[x,y])
                        else:
                            BoxOriImage[x,y]=(0,0,0)
                #Reformat the image
                Sample_Mixed=Sample_Mixed.astype(np.uint8)
                BoxOriImage=BoxOriImage.astype(np.uint8)
                plt.imsave(OutputFolder+"Segmentated_Mixed_Thinned"+image+"_"+str(number) +".png",Sample_Mixed,cmap=plt.cm.gray)
                plt.imsave(OutputFolder+"Segmentated_Closing_"+image+"_"+str(number) +".png",Box_NewImage,cmap=plt.cm.gray)
                plt.imsave(OutputFolder+"Segmentated_Thinned"+image+"_"+str(number) +".png",Box_Sample,cmap=plt.cm.gray)
                plt.imsave(OutputFolder+"Segmentated_Ori"+image+"_"+str(number) +".png",BoxOriImage,cmap=plt.cm.gray)
                number+=1
        ax.set_axis_off() 
        plt.tight_layout()
        plt.show()
        plt.savefig(OutputFolder + "BoundingBox_" + image+ str(GaussianValue) +"_RegionThreshold_" +str(ReginThreshold),dpi=300)
    except Exception, e:
        print "Errors when processing "+ image
        print e
        pass

if __name__ == '__main__':
  main(SampleInputFolder,OverlayInputFolder,LabelInputFolder,LabelMarkers,image,OutputFolder)

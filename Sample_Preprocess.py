import cv2
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
from skimage.morphology import thin, closing, square
from skimage.util import invert
from skimage.color import rgb2gray, label2rgb
from skimage import data,img_as_ubyte
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops
from PIL import Image
import scipy

OutputFolder = 'Output/'
InputFolder = '../RawInput/Tissue/'
#ImageList= ["459591"]#, "406786" ,"423690", "410200"]
image="459591"

def main(InputFolder,image,OutputFolder):
    kernel = np.ones((5,5),np.uint8)
    kernel_size=str(kernel.shape)
    ReginThreshold=5000
    print image
    #Input sample and label files
    Sample_Img = cv2.imread(InputFolder + image + ".jpg" , 0)
    #Lable_Img = cv2.imread(InputFolder + image + ".svs_labels.bmp" , 0)
    #Org_Lable_Img= img_as_ubyte(Image.open(InputFolder + image + ".svs_labels.bmp"))
    Org_Sample_Img = img_as_ubyte(Image.open(InputFolder + image + ".jpg"))

    ## Sample thinning
    # Otsu's thresholding after Gaussian filtering
    blur = cv2.GaussianBlur(Sample_Img,(25,25),0)
    ret1,th1 = cv2.threshold(blur,0,255,cv2.THRESH_OTSU)
    Sample_Closing = cv2.morphologyEx(th1, cv2.MORPH_CLOSE, kernel)
    Sample_Closing_Inverted = invert(Sample_Closing)
    Sample_Closing_Inverted_Gray = rgb2gray(Sample_Closing_Inverted)
    Sample_Closing_Inverted_Binary=np.where(Sample_Closing_Inverted_Gray>np.mean(Sample_Closing_Inverted_Gray),1,0)
    Sample_Thinned = thin(Sample_Closing_Inverted_Binary)

    ##Lale Process
    #Label_Gray = rgb2gray(Lable_Img)
    #Lable_Gray_Inverted = invert(Label_Gray)
    #ret10,Lable_thresholding = cv2.threshold(Lable_Gray_Inverted,10,255,cv2.THRESH_BINARY) #Important
    #Lable_thresholding_Binary=np.where(Lable_thresholding > np.mean(Lable_thresholding),1,0)

    #BoundingBox(ReginThreshold):
    thresh = threshold_otsu(Sample_Closing_Inverted_Binary)
    bw = closing(Sample_Closing_Inverted_Binary > thresh, square(3))
    ## remove artifacts connected to image border
    cleared = clear_border(bw)
    Sample_Thinned = np.where(Sample_Thinned>np.mean(Sample_Thinned),1,0)
    ## label image regions
    label_image = label(cleared)
    image_label_overlay = label2rgb(label_image, image=Sample_Closing_Inverted_Binary)
    number=0
    fig, ax = plt.subplots(figsize=(10, 6))
    #NewImage=Sample_Closing_Inverted_Binary
    #w,l=Sample_Closing_Inverted_Binary.shape
    #for i in range(w):
#        for j in range(l):
    #        NewImage[i,j]=0


    ax.imshow(image_label_overlay,cmap=plt.cm.gray)
    #plt.imsave(OutputFolder+"Test_"+image+"_"+str(number) +".png",Sample_Closing,cmap=plt.cm.gray)
    for region in regionprops(label_image):
        #ax.imshow(region,cmap=plt.cm.gray)
        #print region
        if region.area >= ReginThreshold:  #600
        # dr3aw rectangle around segmented coins
            #Coords= region.coords
            #print Coords
            #for list in range(len(region.coords)):
            #    NewImage[ region.coords[list][0],region.coords[list][1]]=1


            #scipy.misc.imsave(str(number)+'outfile.jpg', NewImage)
            minr, minc, maxr, maxc = region.bbox
            Box_Sample_OrgImg = Org_Sample_Img[minr:maxr, minc:maxc]
            #Box_Label_OrgImg = Org_Lable_Img[minr:maxr, minc:maxc]
            Box_Sample = Sample_Thinned[minr:maxr, minc:maxc]
            #Box_Label = Lable_thresholding_Binary[minr:maxr, minc:maxc]
            #Box_Mixed= cv2.bitwise_or(img_as_ubyte(Box_Sample), img_as_ubyte(Box_Label))
            width, length, height= Box_Sample_OrgImg.shape
            rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                 fill=False, edgecolor='red', linewidth=1)
            ax.add_patch(rect)
            #Mix the sample and label file
            #Box_OrgMixed=np.zeros(shape=(width, length, height))
            Sample_Mixed=np.zeros(shape=(width, length, height))
            for l in range(length):
                for w in range(width):
                    #if Box_Label_OrgImg[w,l,0]>=255 & Box_Label_OrgImg[w,l,1]>=255 & Box_Label_OrgImg[w,l,2]>=255:
                        #Box_OrgMixed[w,l]=(Box_Sample_OrgImg[w,l])
                    #else:
                        #Box_OrgMixed[w,l]=(Box_Label_OrgImg[w,l])
                    if Box_Sample[w,l]==0:
                            Sample_Mixed[w,l]=(Box_Sample_OrgImg[w,l])
                    else:
                        Sample_Mixed[w,l]=(0,0,0)
            #Reformat the image
            #Box_OrgMixed=Box_OrgMixed.astype(np.uint8)
            Sample_Mixed=Sample_Mixed.astype(np.uint8)
            #plt.imsave(OutputFolder+"Segmentated_Thinned"+image+"_"+str(number) +".png",Box_Sample,cmap=plt.cm.gray)
            ##plt.imsave(OutputFolder+"Segmentated_Thinned"+image+"_"+str(number) +"_Label.png",Box_Label,cmap=plt.cm.gray)
            #plt.imsave(OutputFolder+"Segmentated_Mixed_Thinned"+image+"_"+str(number) +".png",Sample_Mixed,cmap=plt.cm.gray)
            number+=1
    ax.set_axis_off()
    plt.tight_layout()
    #plt.show()
    plt.savefig(OutputFolder + "BoundingBox_" + image+ "_RegionThreshold_" +str(ReginThreshold) +"kel25",dpi=300)


if __name__ == '__main__':
  main(InputFolder,image,OutputFolder)

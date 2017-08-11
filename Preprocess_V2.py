import cv2
import scipy
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
from skimage.morphology import thin, closing, square
from skimage.util import invert
from skimage.color import rgb2gray, label2rgb
from skimage import data,img_as_ubyte
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops


OutputFolder = '../Output/'
InputFolder = '../RawInput/Tissue/'

image="507469"

def main(InputFolder,image,OutputFolder):
    kernel = np.ones((5,5),np.uint8)
    kernel_size=str(kernel.shape)
    ReginThreshold=5000
    print image
    #Input sample and label files
    Sample_Img = cv2.imread(InputFolder + image + ".jpg" , 0)
    Org_Sample_Img = img_as_ubyte(Image.open(InputFolder + image + ".jpg"))

    ## Sample thinning
    # Otsu's thresholding after Gaussian filtering
    blur = cv2.GaussianBlur(Sample_Img,(75,75),0)
    ret1,th1 = cv2.threshold(blur,0,255,cv2.THRESH_OTSU)
    Sample_Closing = cv2.morphologyEx(th1, cv2.MORPH_CLOSE, kernel)
    Sample_Closing_Inverted_Gray = rgb2gray(invert(Sample_Closing))
    Sample_Closing_Inverted_Binary=np.where(Sample_Closing_Inverted_Gray>np.mean(Sample_Closing_Inverted_Gray),1,0)

    w,l = Sample_Closing_Inverted_Binary.shape
    Sample_Closing_Inverted_Binary_Expanded=np.insert(Sample_Closing_Inverted_Binary,[l-1]*10,0,axis=1)
    Sample_Closing_Inverted_Binary_Expanded=np.insert(Sample_Closing_Inverted_Binary_Expanded,[0]*10,0,axis=1)
    Sample_Closing_Inverted_Binary_Expanded=np.insert(Sample_Closing_Inverted_Binary_Expanded,[w-1]*10,0,axis=0)
    Sample_Closing_Inverted_Binary_Expanded=np.insert(Sample_Closing_Inverted_Binary_Expanded,[0]*10,0,axis=0)

    Org_Sample_Img=np.insert(Org_Sample_Img,[l-1]*10,0,axis=1)
    Org_Sample_Img=np.insert(Org_Sample_Img,[0]*10,0,axis=1)
    Org_Sample_Img=np.insert(Org_Sample_Img,[w-1]*10,0,axis=0)
    Org_Sample_Img=np.insert(Org_Sample_Img,[0]*10,0,axis=0)



    #BoundingBox(ReginThreshold):
    thresh = threshold_otsu(Sample_Closing_Inverted_Binary_Expanded)
    bw = closing(Sample_Closing_Inverted_Binary_Expanded > thresh, square(3))
    ## remove artifacts connected to image border
    cleared = clear_border(bw)
    ## label image regions
    label_image = label(cleared)
    image_label_overlay = label2rgb(label_image, image=Sample_Closing_Inverted_Binary_Expanded)
    number=0
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(image_label_overlay,cmap=plt.cm.gray)
    #plt.imsave(OutputFolder+"Test_"+image+"_"+str(number) +".png",Sample_Closing,cmap=plt.cm.gray)
    for region in regionprops(label_image):
        if region.area >= ReginThreshold:
            NewImage=np.zeros((w+20,l+20))
        # dr3aw rectangle around segmented coins
            Coords= region.coords
            #scipy.misc.imsave(str(number)+'outfile.jpg', NewImage)
            minr, minc, maxr, maxc = region.bbox
            Box_Sample_OrgImg = Org_Sample_Img[max(0,minr-10):min(maxr+10,w+19), max(minc-10,0):min(maxc+10,l+19)]
            width, length, height= Box_Sample_OrgImg.shape
            #NewImage=np.zeros((width, length))
            for list in range(len(region.coords)):
                NewImage[ region.coords[list][0],region.coords[list][1]] = Sample_Closing_Inverted_Binary_Expanded[ region.coords[list][0],region.coords[list][1]]

            Box_Sample = thin(NewImage)
            Box_NewImage =NewImage[max(0,minr-10):min(maxr+10,w+19), max(minc-10,0):min(maxc+10,l+19)]
            Box_Sample=Box_Sample[max(0,minr-10):min(maxr+10,w+19), max(minc-10,0):min(maxc+10,l+19)]
            Box_Sample = np.where(Box_Sample>np.mean(Box_Sample),1,0)
            #Box_Sample = Sample_Thinned[max(0,minr-10):min(maxr+10,w), max(minc-10,0):min(maxc,l+10)]
            rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
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
                        Sample_Mixed[x,y]=(0,0,0)
            #Reformat the image
            Sample_Mixed=Sample_Mixed.astype(np.uint8)
            plt.imsave(OutputFolder+"Segmentated_Mixed_Thinned"+image+"_"+str(number) +".png",Sample_Mixed,cmap=plt.cm.gray)
            plt.imsave(OutputFolder+"Segmentated_Ori_"+image+"_"+str(number) +".png",Box_NewImage,cmap=plt.cm.gray)
            plt.imsave(OutputFolder+"Segmentated_Thinned"+image+"_"+str(number) +".png",Box_Sample,cmap=plt.cm.gray)
            number+=1
    ax.set_axis_off()
    plt.tight_layout()
    #plt.show()
    plt.savefig(OutputFolder + "BoundingBox_" + image+ "_RegionThreshold_" +str(ReginThreshold) +"kel75",dpi=300)


if __name__ == '__main__':
  main(InputFolder,image,OutputFolder)

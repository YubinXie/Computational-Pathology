import cv2
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches

from skimage.morphology import skeletonize, thin, medial_axis, closing, square
from skimage.util import invert
from skimage.color import rgb2gray, label2rgb
from skimage import data,img_as_ubyte
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops
from PIL import Image
InputFolder='RawInput/'
OutputFolder='Output/'

ImageList= ["459591", "406786" ,"423690", "410200"]
kernel = np.ones((5,5),np.uint8)
kernel_size=str(kernel.shape)

def main():
  global img
  global image, Lable_Img,label_thresholding, Org_Lable_Img, Org_Sample_Img
  for image in ImageList:
    print image
    img = cv2.imread(InputFolder + image + ".jpg" , 0)
    Org_Lable_Img= Image.open(InputFolder + image + ".svs_labels.bmp")
    Org_Sample_Img = Image.open(InputFolder + image + ".jpg")
    
    Lable_Img = cv2.imread(InputFolder + image + ".svs_labels.bmp" , 0)
    Thresholding()
    #Plot_OtsuThresholding()
    Closing()
    #Invert()
    #Plot_Closing("_KernelSize_" + kernel_size)
    Invert()
    Thining()
    Label_Thresholding()
    #Plot_BinaryThresholding()

    BoundingBox(5000) #20000 SOME do not work #15000 all work for 4. If the image is total vetical, the average size is around 8000, here I take 3000 to keep the small pieces as well as to prevent too small pieces (1000)
    #np.savetxt('test.txt', thinned3)
    #Plot_Thinning("_Invert")
    # apply threshold



#plt.figure(figsize=(width/DPI,height/DPI))



def Thresholding():
  global th1, th2, th3, th4,blur,blur2
  # global thresholding
  ret1,th1 = cv2.threshold(img,200,255,cv2.THRESH_BINARY)

  # Otsu's thresholding
  ret2,th2 = cv2.threshold(img,0,255,cv2.THRESH_OTSU)

  # Otsu's thresholding after Gaussian filtering  
  blur = cv2.GaussianBlur(img,(75,75),0) #(75,75)
  blur2 = cv2.GaussianBlur(img,(25,25),0) #(25,25)

  ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_OTSU)
  ret4,th4 = cv2.threshold(blur2,0,255,cv2.THRESH_OTSU)

def Label_Thresholding():
  global label_thresholding, Lable_Img
  label_thresholding=rgb2gray(Lable_Img)
  label_thresholding = invert(label_thresholding)
  ret10,label_thresholding = cv2.threshold(label_thresholding,10,255,cv2.THRESH_BINARY) #Important

  label_thresholding=np.where(label_thresholding>np.mean(label_thresholding),1,0)

 # ret10,label_thresholding = cv2.threshold(Lable_Img,127,255,cv2.THRESH_BINARY)

def Closing():  
  global closing1, closing2, closing3
  closing1 = cv2.morphologyEx(th2, cv2.MORPH_CLOSE, kernel)
  closing2 = cv2.morphologyEx(th4, cv2.MORPH_CLOSE, kernel)
  closing3 = cv2.morphologyEx(th3, cv2.MORPH_CLOSE, kernel)

def Invert():
  global closing1, closing2, closing3
  closing1 = invert(closing1)
  closing2 = invert(closing2)
  closing3 = invert(closing3)


def Thining():
  global closing1, closing2, closing3, skeleton1, skeleton2, skeleton3, thinned1,thinned2,thinned3
  closing1=rgb2gray(closing1)
  closing1=np.where(closing1>np.mean(closing1),1,0)
  skeleton1 = skeletonize(closing1)

  closing2=rgb2gray(closing2)
  closing2=np.where(closing2>np.mean(closing2),1,0)
  skeleton2 = skeletonize(closing2)

  closing3=rgb2gray(closing3)
  closing3=np.where(closing3>np.mean(closing3),1,0)

  skeleton3 = skeletonize(closing3)

  thinned1= thin(closing1)
  thinned2= thin(closing2)
  thinned3= thin(closing3)
  #thinned3 = img_as_ubyte(thinned3)

def BoundingBox(ReginThreshold):
  global label_thresholding, closing3,thinned3,Org_Lable_Img, img, Org_Sample_Img
  Closing3=closing3 #thinned3
  thresh = threshold_otsu(Closing3)
  bw = closing(Closing3 > thresh, square(3))
  # remove artifacts connected to image border
  cleared = clear_border(bw)
  thinned3=np.where(thinned3>np.mean(thinned3),1,0)
  # label image regions
  label_image = label(cleared)
  image_label_overlay = label2rgb(label_image, image=Closing3)

  #fig, ax = plt.subplots(figsize=(10, 6))
  #ax.imshow(image_label_overlay,cmap=plt.cm.gray)

  for region in regionprops(label_image):
    # take regions with large enough areas
    if region.area >= ReginThreshold:  #600
    # draw rectangle around segmented coins
      minr, minc, maxr, maxc = region.bbox
      rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                 fill=False, edgecolor='red', linewidth=2)
      print minc, minr, maxc, maxr
      #ax.add_patch(rect)

  #ax.set_axis_off()
  #plt.tight_layout()
  #plt.show()
  #plt.savefig(OutputFolder + "BoundingBox_" + Image+ "_RegionThreshold_" +str(ReginThreshold),dpi=300)
  number=1
  Org_Lable_Img=img_as_ubyte(Org_Lable_Img)
  Org_Sample_Img=img_as_ubyte(Org_Sample_Img)
  for region in regionprops(label_image):
    if region.area >= ReginThreshold:  #600
    # draw rectangle around segmented coins

      minr, minc, maxr, maxc = region.bbox
      Box_Sample_OrgImg = Org_Sample_Img[minr:maxr, minc:maxc]
      Box_Label_OrgImg = Org_Lable_Img[minr:maxr, minc:maxc]

      Box_Sample = thinned3[minr:maxr, minc:maxc]
      Box_Label = label_thresholding[minr:maxr, minc:maxc]
      Box_Label = img_as_ubyte(Box_Label)
      Box_Sample = img_as_ubyte(Box_Sample)
      Box_Mixed= cv2.bitwise_or(Box_Sample, Box_Label)
      #Box_OrgMixed=cv2.add(Box_Sample_OrgImg, Box_Label_OrgImg)
      #print Box_Sample_OrgImg, Box_Label_OrgImg
      width, length, height= Box_Label_OrgImg.shape
      #Box_Sample_OrgImg=invert(Box_Sample_OrgImg)
      #Box_Label_OrgImg=(Box_Label_OrgImg)
      #print width, length, height
      Box_OrgMixed=np.zeros(shape=(width, length, height))
      Sample_Mixed=np.zeros(shape=(width, length, height))
      for l in range(length):
        for w in range(width):
            if Box_Label_OrgImg[w,l,0]>=255 & Box_Label_OrgImg[w,l,1]>=255 & Box_Label_OrgImg[w,l,2]>=255:
              Box_OrgMixed[w,l]=(Box_Sample_OrgImg[w,l])
            else:
              Box_OrgMixed[w,l]=(Box_Label_OrgImg[w,l])

            if Box_Sample[w,l]==0:
              Sample_Mixed[w,l]=(Box_Sample_OrgImg[w,l])
            else:
              Sample_Mixed[w,l]=(0,0,0)
      width, length= Box_Label.shape
      LineLength=0
        #if Box_Label[w,l+1]

              #print w,l,Box_Label_OrgImg[w,l,0],Box_Label_OrgImg[w,l,1],Box_Label_OrgImg[w,l,2]
      #Box_OrgMixed = (Box_Sample_OrgImg+ Box_Label_OrgImg)
      Box_OrgMixed=Box_OrgMixed.astype(np.uint8)
      Sample_Mixed=Sample_Mixed.astype(np.uint8)
      fig, ax = plt.subplots(2,3,figsize=(20, 12))
      ax[0,0].imshow(Box_Sample_OrgImg, cmap=plt.cm.gray)
      ax[0,0].set_axis_off()
      ax[0,1].imshow(Box_Label_OrgImg, cmap=plt.cm.gray)
      ax[0,1].set_axis_off()
      ax[0,2].imshow((Box_OrgMixed))
      ax[0,2].set_axis_off()
      ax[1,0].imshow(Box_Sample, cmap=plt.cm.gray)
      ax[1,0].set_axis_off()
      ax[1,1].imshow(Box_Label, cmap=plt.cm.gray)
      ax[1,1].set_axis_off()
      ax[1,2].imshow(Box_Mixed, cmap=plt.cm.gray)
      ax[1,2].set_axis_off()
      #ax[2,0].imshow(Sample_Mixed)
      plt.savefig(OutputFolder+"MergedBox_Thin_Label"+image+"_"+str(number),dpi=300)

      plt.tight_layout()
      #plt.show()
      fig, ax = plt.subplots(1,1,figsize=(10, 6))
      ax.imshow(Sample_Mixed)
      #plt.show()
      #plt.savefig(OutputFolder+"MergedBox_OrgSample_Thin_"+image+"_"+str(number),dpi=300)
      
      #plt.imsave(OutputFolder+"Segmentated_Thinned"+image+"_"+str(number) +".png",Box_Sample,cmap=plt.cm.gray)
      #plt.imsave(OutputFolder+"Segmentated_Thinned"+image+"_"+str(number) +"_Label.png",Box_Label,cmap=plt.cm.gray)
      plt.imsave(OutputFolder+"Segmentated_Mixed_Thinned"+image+"_"+str(number) +".png",Box_Mixed,cmap=plt.cm.gray)
      number+=1

#def calculating():
#  global Box_Label
#  width, length= Box_Label.shape
#  length=0
#  for w in range(width):
#    for l in range(length):
#      if Box_Label[w,l]=1:
#        if Box_Label[w+1,l]+Box_Label[w+1,l+1]+Box_Label[w,l+1]+Box_Label[w-1,l]+Box_Label[w+1,l]




def Plot_OtsuThresholding():
  global blur2
  images = [img, 0, th1,
          img, 0, th2,
          blur2,0,th4,
          blur, 0, th3]
  titles = ['Original Noisy Image','Histogram','Global Thresholding (v=127)',
          'Original Noisy Image','Histogram',"Otsu's Thresholding",
          'Gaussian filtered Image (25,25)','Histogram',"Otsu's Thresholding",
          'Gaussian filtered Image (75,75)','Histogram',"Otsu's Thresholding"]
  for i in xrange(4):

    plt.subplot(4,3,i*3+1), plt.imshow(images[i*3],'gray')
    plt.title(titles[i*3]), plt.xticks([]), plt.yticks([])
    plt.subplot(4,3,i*3+2),plt.hist(images[i*3].ravel(),256)
    plt.title(titles[i*3+1]), plt.xticks([]), plt.yticks([])
    plt.subplot(4,3,i*3+3),plt.imshow(images[i*3+2],'gray')
    plt.title(titles[i*3+2]), plt.xticks([]), plt.yticks([])
  plt.show()
  #plt.savefig(OutputFolder + "Thredsholding_" + image,dpi=300)

def Plot_BinaryThresholding():
  plt.subplot(2,1,1), plt.imshow(Org_Lable_Img)
  plt.subplot(2,1,2), plt.imshow(label_thresholding,'gray')
  #plt.show()
  plt.savefig(OutputFolder + "Label_" + image,dpi=300)
  #np.savetxt('markers.txt', label_thresholding)

def Plot_Closing(suffix):
  fig=plt.figure(figsize=(20,12))
  plt.subplot(3,2,1),plt.imshow(th2,'gray')
  plt.title("Otsu's Thresholding"), plt.xticks([]), plt.yticks([])
  plt.subplot(3,2,2),plt.imshow(closing1,'gray')
  plt.title("Closing_"+kernel_size), plt.xticks([]), plt.yticks([])
  plt.subplot(3,2,3),plt.imshow(th4,'gray')
  plt.title("Gaussian filtered (25,25) + Otsu's Thresholding"), plt.xticks([]), plt.yticks([])
  plt.subplot(3,2,4),plt.imshow(closing2,'gray')
  plt.title("Closing_"+kernel_size), plt.xticks([]), plt.yticks([])
  plt.subplot(3,2,5),plt.imshow(th3,'gray')
  plt.title("Gaussian filtered (75,75) + Otsu's Thresholding"), plt.xticks([]), plt.yticks([])
  plt.subplot(3,2,6),plt.imshow(closing3,'gray')
  plt.title("Closing_"+kernel_size), plt.xticks([]), plt.yticks([])
  #plt.show()
 # plt.savefig(OutputFolder+"Closing_"+image+suffix,dpi=200)
  plt.imsave(OutputFolder+"Closing3_"+kernel_size +".png",closing3,cmap=plt.cm.gray)


def Plot_Thinning(suffix):
  fig=plt.figure(figsize=(30,12))
  plt.subplot(3,3,1),plt.imshow(closing1,'gray')
  plt.title("Otsu's Thresholding +"+"Closing_"+kernel_size), plt.xticks([]), plt.yticks([])
  plt.subplot(3,3,2),plt.imshow(thinned1,'gray')
  plt.title("Thining"), plt.xticks([]), plt.yticks([])
  plt.subplot(3,3,3),plt.imshow(closing2,'gray')
  plt.title("Gaussian filtered (25,25) + Otsu's Thresholding +" + "Closing_"+kernel_size), plt.xticks([]), plt.yticks([])
  plt.subplot(3,3,4),plt.imshow(thinned2,'gray')
  plt.title("Thining"), plt.xticks([]), plt.yticks([])
  plt.subplot(3,3,5),plt.imshow(closing3,'gray')
  plt.title("Gaussian filtered (75,75) + Otsu's Thresholding + Closing_"+kernel_size), plt.xticks([]), plt.yticks([])
  plt.subplot(3,3,6),plt.imshow(thinned3,'gray')
  plt.title("Thining"), plt.xticks([]), plt.yticks([])
  plt.title("Gaussian filtered (75,75) + Otsu's Thresholding + Closing_"+kernel_size), plt.xticks([]), plt.yticks([])
  plt.subplot(3,3,7),plt.imshow(skeleton1,'gray')
  plt.title("Skeleton"), plt.xticks([]), plt.yticks([])
  plt.subplot(3,3,8),plt.imshow(skeleton2,'gray')
  plt.title("Skeleton"), plt.xticks([]), plt.yticks([])
  plt.subplot(3,3,9),plt.imshow(skeleton3,'gray')
  plt.title("Skeleton"), plt.xticks([]), plt.yticks([])
  plt.savefig(OutputFolder+"Thining_"+image+suffix,dpi=300)
  #plt.show()
  fig=plt.figure(figsize=(10,6))
  plt.subplot(1,1,1),plt.imshow(thinned3,'gray')
  plt.xticks([]), plt.yticks([]) #plt.title("Thining"),
  #plt.title("Gaussian filtered (75,75) + Otsu's Thresholding + Closing_"+kernel_size), plt.xticks([]), plt.yticks([])
  #plt.savefig(OutputFolder+"Along_Thining_"+image+suffix,dpi=300)
  #plt.imsave(OutputFolder+"Along_Thinned"+kernel_size +".png",thinned3,cmap=plt.cm.gray)
  #plt.imsave(OutputFolder+"Along_Thinned"+kernel_size +".png",thinned3,cmap=plt.cm.gray)


if __name__ == '__main__':
  main()

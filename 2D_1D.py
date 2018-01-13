##Created at 08/02/2017 by Yubin Xie, MSKCC
##Modified at #### by ***
## This script is to find the starting points in the binary images and find the shortest path between them (the starting point only have 1 connection instead of 2)
import itertools
import math
from scipy import misc
from scipy.sparse.dok import dok_matrix
from scipy.sparse.csgraph import dijkstra
import operator
from skimage import data,img_as_ubyte
from operator import sub, add
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import itertools
InputFolder = "../Selected_output/"
OutputFolder=""
OverlapFolder = "../RawInput/Overlay_3/"
TissueList = ["447088_0","447088_1"]   #"Segmentated_Thinned423690_2" "path" Segmentated_Thinned495400_1.png Segmentated_Label495400_1.bmp
import csv,cv2
global Pl, Index

def main(TissueList,InputFolder,OutputFolder,OverlapFolder):
    global Plot, SampleNumber, Index
    SampleNumber = len(TissueList)
    for Index in range(len(TissueList)):
        LabelFileName = "Segmentated_Label" + TissueList[Index]
        SampleID = "Segmentated_Thinned" + TissueList[Index]
        original_label = Image.open(InputFolder+LabelFileName+'.bmp' )
        label_img=np.asarray(original_label)
        GleasonList = np.unique(label_img)
        all_zeros = not label_img.any()
        if all_zeros == True:
            SampleNumber = SampleNumber -1
    Plot = plt.figure(figsize=(10*SampleNumber,8*(len(GleasonList)+1)),dpi=200)
    Overlap = Image.open(OverlapFolder +  "Overlay_" + str(TissueList[0][:6]) +"_alpha0.4.png")
    print Overlap
    #overlap_img =.astype(np.uint8)
    #print overlap_img
    plt.subplot(len(GleasonList)+2,1,1)
    plt.imshow(Overlap,cmap=plt.cm.gray)
    
    for Index in range(SampleNumber):
        mainpart(TissueList[Index])
    plt.savefig(str(TissueList[0][:6])+".png")

def mainpart(TissueID):
    global SampleNumber
    global Plot
    global Index
    SizeDic={}
    LabelFileName = "Segmentated_Label" + TissueID
    SampleID = "Segmentated_Thinned" + TissueID
    with open ("../RawInput/Selected_3/Output.txt", "r") as openSizeinformaiton:
        for line in openSizeinformaiton:
            ElementList = line.strip().split()
            SizeDic[ElementList[0]]=ElementList[1:]
    print SizeDic[TissueID[:6]+".svs"]
    DistanceLimit = 3000/(float(SizeDic[TissueID[:6]+".svs"][0]))/50.0
    SizeScale = float(SizeDic[TissueID[:6]+".svs"][0])*50
    Color=np.array([[255,255,255],[255,255,0],[0,255,0],[0,0,255],[255,0,50],[0,255,255],[255,0,255]])

    print SampleID
    ColorList = []
    def to_index(y, x):
        return y * img.shape[1] + x
    # Defines a reversed translation from index to 2 coordinates
    def to_coordinates(index):
        return index / img.shape[1], index % img.shape[1]
    # Defines the distance between 2 coordinates
    def distance(list1,list2):
        return math.hypot(list1[0]-list2[0],list1[1]-list2[1])
    def tupleadd(a,b):
        return tuple(map(sum,zip(a,b)))
    try:
        # Load the image
        original_img = misc.imread(InputFolder + SampleID+'.png')
        img = original_img[:, :, 0] + original_img[:, :, 1] + original_img[:, :, 2]
        original_label = Image.open(InputFolder+LabelFileName+'.bmp' )

        label_img=np.asarray(original_label)
        label_width,label_length=original_label.size
        #label_img=np.array(label_img)
        all_zeros = not label_img.any()
        GleasonList = np.unique(label_img)
        GleasonNumber = len(GleasonList)
        print "Gleason Grade Group:",GleasonNumber-1
        new_image = np.zeros((label_length,label_width,GleasonNumber))
        plot_new_image = np.zeros((label_length,label_width,GleasonNumber))

        for gleason in range(GleasonNumber):
            for width in range(label_width):
                for length in range(label_length):
                    if gleason==0 and label_img[length,width]!=0:
                        new_image[length,width,0] = label_img[length,width]
                        plot_new_image[length,width,0] = label_img[length,width]
                    else:
                        if label_img[length,width] == GleasonList[gleason]:
                            new_image[length,width,gleason] = GleasonList[gleason]
                            plot_new_image[length,width,gleason] = GleasonList[gleason]
                    if img[length,width]:
                        plot_new_image[length,width,gleason]= 8


        
        if all_zeros == True:
            raise ValueError("no label")




    # Defines a translation from 2 coordinates to a single number

        SourceList=[]

        for i in range(0,img.shape[0]-1):
            for j in range(0,img.shape[1]-1):
                if img[i,j]>=1:
                    img[i,j]=1

        for i in range(1,img.shape[0]-2):
            for j in range(1,img.shape[1]-2):
                if img[i,j]==0:
                    continue
                sourse=None
                NearValue=0
                CornerValue=0
                NearValueList=[]
                CornerValueList=[]
                NearPosition = [(-1,0),(0,-1),(0,1),(1,0),]
                CornerPosition = [(-1,1),(1,1),(-1,-1),(1,-1)]
                for direction in range(4):
                    NearValue=NearValue+img[tupleadd((i,j),NearPosition[direction])]
                    NearValueList.append(img[tupleadd((i,j),NearPosition[direction])])
                    CornerValue=CornerValue+img[tupleadd((i,j),CornerPosition[direction])]
                    CornerValueList.append(img[tupleadd((i,j),CornerPosition[direction])])
                if NearValue + CornerValue==1:
                    sourse = (i,j)
                if NearValue==1 and CornerValue==1:
                    NearDirection=NearPosition[NearValueList.index(1)]
                    CornerDirection=CornerPosition[CornerValueList.index(1)]
                    if (NearDirection[0]==CornerDirection[0]) or (NearDirection[1]==CornerDirection[1]):
                        sourse = (i,j)
                if sourse!=None:
                    if sourse not in SourceList:
                        SourceList.append(sourse)
        print len(SourceList), " single points are found in the image", SourceList




# Two pixels are adjacent in the graph if both are painted.
        adjacency = dok_matrix((img.shape[0] * img.shape[1],img.shape[0] * img.shape[1]), dtype=bool)
        directions = list(itertools.product([0, 1, -1], [0, 1, -1]))
        for i in range(1, img.shape[0] - 1):
            for j in range(1, img.shape[1] - 1):
                if not img[i, j]:
                    continue
                for y_diff, x_diff in directions:
                    if img[i + y_diff, j + x_diff]:
                        adjacency[to_index(i, j),
                            to_index(i + y_diff, j + x_diff)] = True
        Distance=[]
        Combination = [(p1,p2) for p1 in range(len(SourceList)) for p2 in range(p1+1,len(SourceList))]
        for p1,p2 in Combination:
            p1 = to_index(SourceList[p1][0],SourceList[p1][1])
            p2 = to_index(SourceList[p2][0],SourceList[p2][1])
            dist_matrix = dijkstra(adjacency, directed=False,unweighted=True,indices=[p1],limit=1000)
            Distance.append( dist_matrix[0,p2] )



    #Distance = [dist_matrix[to_index(SourceList[p1][0],SourceList[p1][1]),to_index(SourceList[p2][0],SourceList[p2][1])] for p1 in range(len(SourceList)) for p2 in range(p1+1,len(SourceList))]
        Start_End= Combination[Distance.index(max(Distance))]
        print Distance
        source = to_index(SourceList[Start_End[0]][0],SourceList[Start_End[0]][1])
        target = to_index(SourceList[Start_End[1]][0],SourceList[Start_End[1]][1])

        # Compute the shortest path between the source and all other points in the image
        _, predecessors = dijkstra(adjacency, directed=False, indices=[source],
                            unweighted=True, return_predecessors=True)
                            # Construct the path between source and target
        pixel_index = target
        pixels_path =  []
        while pixel_index != source:
            pixels_path.append(pixel_index)
            pixel_index = predecessors[0, pixel_index]

    #To visualize the chosen path
        for point in SourceList:
            original_img[point[0],point[1],0]=0
        Path=[]
        Distance=0
        DistanceDic={}
        DistanceList=[]
        LastPoint=to_coordinates(target)
        pixels_path.append(source)
        #print source,target
        Sample={}
        for gleason in range(GleasonNumber):
            Sample[gleason] = {}
        for pixel_index in pixels_path:

            #print pixel_index
            point=to_coordinates(pixel_index)
            Path.append(point)
            original_img[point[0],point[1],1]=0
            Distance=Distance+distance(LastPoint,(point))
            #print point, Distance
            DistanceList.append(distance(LastPoint,(point)))
            DistanceDic[(point)]=sum(DistanceList[:])
            LastPoint=(point)
            for gleason in range(GleasonNumber):
                Sample[gleason][point]=0
        print len(Path)
        print Distance
        #plt.imshow(original_img)
        #plt.savefig("Path_"+SampleID)
        ##########

        
        for gleason in range(GleasonNumber):
            print "Gleason Level: " ,GleasonList[gleason]
            for i in range(0,label_width -1):
                for j in range(0,label_length -1):
                    if new_image[j,i,gleason]:
                        LabelSampleDistanceList={}
                        for sample in Path:
                            LabelSampleDistanceList[sample]=distance(sample,(j,i)) # i j or j i
                        Sample[gleason][min(LabelSampleDistanceList, key=LabelSampleDistanceList.get)]+=1

            Xcoordinate=[]
            Ycoordinate=[]
            TumorNumber=1
            TumorSizeList=[]
            TumorStartPoint=[]
            TumorEndPoint=[]

            #TumorPoint=Path[np.nonzero(Sample.values())[0][0]]

            for i in range(len(Path)):
                if Sample[gleason][Path[i]] >0:
                    TumorPoint=Path[i]
                    break
            print "Plot ", gleason ," First tumor",DistanceDic[TumorPoint]
            TumorStartPoint.append(DistanceDic[TumorPoint])
            for i in range(len(Path)):
                X=sum(DistanceList[:i])
                Xcoordinate.append(X*SizeScale/1000.0)
                Ycoordinate.append(Sample[gleason][Path[i]])
                if Sample[gleason][Path[i]]>=1:
                    NextTumorPoint=Path[i]
                    #print NextTumorPoint

                    if (DistanceDic[NextTumorPoint]- DistanceDic[TumorPoint])>=DistanceLimit:
                        TumorNumber+=1
                        TumorEndPoint.append(DistanceDic[TumorPoint])
                        TumorPoint=Path[i]
                        TumorStartPoint.append(DistanceDic[TumorPoint])
                    TumorPoint=Path[i]
            print Sample[gleason]
            TumorEndPoint.append(DistanceDic[TumorPoint])
            TumorSizeList=map(sub, TumorEndPoint, TumorStartPoint)
            print TumorStartPoint,TumorEndPoint
            TumorSizeList = [round(i*(float(SizeDic[TissueID[:6]+".svs"][0]))/20.0,3) for i in TumorSizeList]
            print "Tumor Number = ",TumorNumber," Tumor Size = ", TumorSizeList
            AverageXcoordinate=[]
            AverageYcoordinate=[]
            for x in range(len(Xcoordinate)):
                AverageXcoordinate.append(sum(Xcoordinate[x:x+3])/len(Xcoordinate[x:x+3]))
                AverageYcoordinate.append(sum(Ycoordinate[x:x+3])/len(Ycoordinate[x:x+3]))
            plt.subplot(GleasonNumber+1,2*SampleNumber,2*(gleason+1)*SampleNumber+2+2*(int(Index)))
            plt.subplots_adjust(left=0.1, bottom=0.1, right=0.8, top=0.9, wspace=0.3, hspace=0.1)
            print np.unique(new_image[:,:,gleason])
            plt.imshow(plot_new_image[:,:,gleason])
            plt.subplot(GleasonNumber+1,2*SampleNumber,2*SampleNumber*(gleason+1)+1+2*(Index))
            plt.plot(Xcoordinate,Ycoordinate)
            plt.subplots_adjust(left=0.1, bottom=0.1, right=0.8, top=0.9, wspace=0.3, hspace=0.1)
            #plt.xlabel('Biopsy Length (mm)')
            plt.ylabel('Tumor Density')
            if gleason == 0:
                Title="All Gleason Score"
            else:
                Title="Gleason Score:"+str(GleasonList[gleason])
            plt.title(Title)
        #plt.savefig(OutputFolder+"TumorDistribution_"+SampleID)
        #plt.tight_layout()
       
        plt.xlabel('Biopsy Length (mm)')
        TumorSizeList = [round(i*(float(SizeDic[TissueID[:6]+".svs"][0]))/20.0,3) for i in TumorSizeList]
        plt.figtext(.02, .02*(1+Index), "Tumor Number = %d  Tumor Size = %s mm" % (TumorNumber,TumorSizeList))
        plt.suptitle( TissueList[Index][:6])
        plt.tight_layout() 

    except Exception, e:
        print e
        pass


if __name__ == '__main__':
  main(TissueList,InputFolder,OutputFolder,OverlapFolder)

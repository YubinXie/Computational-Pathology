##Created at 08/02/2017 by Yubin Xie, MSKCC
##Modified at #### by ***
## This script is to find the starting points in the binary images and find the shortest path between them (the starting point only have 1 connection instead of 2)
import itertools
import math
from scipy import misc
from scipy.sparse.dok import dok_matrix
from scipy.sparse.csgraph import dijkstra
import operator
from operator import sub, add
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import itertools
InputFolder = "../Output/Selected_Tissue2/"
OutputFolder=""
TissueID = "495400_0"   #"Segmentated_Thinned423690_2" "path" Segmentated_Thinned495400_1.png Segmentated_Label495400_1.bmp
def main(TissueID):
    LabelFileName = "Segmentated_Label" + TissueID
    SampleID = "Segmentated_Thinned" + TissueID
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
        original_img = misc.imread(SampleID+'.png')
        img = original_img[:, :, 0] + original_img[:, :, 1] + original_img[:, :, 2]
        original_label = Image.open(InputFolder+LabelFileName+'.bmp' )
        #label_img=original_label.load()
        label_img=np.asarray(original_label)
        label_width,label_length=original_label.size
        #label_img=np.array(label_img)
        print label_img
        all_zeros = not label_img.any()
        GleasonList = np.unique(label_img)
        GleasonNumber = len(GleasonList)
        for gleason in range(GleasonNumber-1):
            for width in label_width:
                for length in label_length:
                    if label_img[length,width] ==
        print all_zeros
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
        print (SourceList), "\n",len(SourceList), " single points are found in the image"




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
        Conbination = [(p1,p2) for p1 in range(len(SourceList)) for p2 in range(p1+1,len(SourceList))]
        for p1,p2 in Conbination:
            p1 = to_index(SourceList[p1][0],SourceList[p1][1])
            p2 = to_index(SourceList[p2][0],SourceList[p2][1])
            dist_matrix = dijkstra(adjacency, directed=False,unweighted=True,indices=[p1],limit=1000)
            Distance.append( dist_matrix[0,p2] )



    #Distance = [dist_matrix[to_index(SourceList[p1][0],SourceList[p1][1]),to_index(SourceList[p2][0],SourceList[p2][1])] for p1 in range(len(SourceList)) for p2 in range(p1+1,len(SourceList))]
        Start_End= Conbination[Distance.index(max(Distance))]
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
        for pixel_index in pixels_path:
            #print pixel_index
            point=to_coordinates(pixel_index)
            Path.append(point)
            Sample[point]=0
            original_img[point[0],point[1],1]=0
            Distance=Distance+distance(LastPoint,(point))
            #print point, Distance
            DistanceList.append(distance(LastPoint,(point)))
            DistanceDic[(point)]=sum(DistanceList[:])
            LastPoint=(point)
        print len(Path)
        print Distance
        #plt.imshow(original_img)
        #plt.savefig("Path_"+SampleID)
        ##########

        for i in range(0,label_width -1):
            for j in range(0,label_length -1):
                if label_img[j,i]:
                    LabelSampleDistanceList={}
                    for sample in Path:
                        LabelSampleDistanceList[sample]=distance(sample,(i,j))
                    Sample[min(LabelSampleDistanceList, key=LabelSampleDistanceList.get)]+=1

        Xcoordinate=[]
        Ycoordinate=[]
        TumorNumber=1
        TumorSizeList=[]
        TumorStartPoint=[]
        TumorEndPoint=[]

        #TumorPoint=Path[np.nonzero(Sample.values())[0][0]]

        for i in range(len(Path)):
            if Sample[Path[i]] >0:
                TumorPoint=Path[i]
                break

        print "First tumor",DistanceDic[TumorPoint]
        TumorStartPoint.append(DistanceDic[TumorPoint])
        for i in range(len(Path)):
            X=sum(DistanceList[:i])
            Xcoordinate.append(X)
            Ycoordinate.append(Sample[Path[i]])
            if Sample[Path[i]]>=1:
                NextTumorPoint=Path[i]
                #print NextTumorPoint
                if (DistanceDic[NextTumorPoint]- DistanceDic[TumorPoint])>=50:
                    TumorNumber+=1
                    TumorEndPoint.append(DistanceDic[TumorPoint])
                    TumorPoint=Path[i]
                    TumorStartPoint.append(DistanceDic[TumorPoint])
                TumorPoint=Path[i]
        TumorEndPoint.append(DistanceDic[TumorPoint])
        TumorSizeList=map(sub, TumorEndPoint, TumorStartPoint)
        print TumorStartPoint,TumorEndPoint
        print "Tumor Number = ",TumorNumber," Tumor Size = ", TumorSizeList

        plt.plot(Xcoordinate,Ycoordinate)
        plt.show()
        #plt.savefig(OutputFolder+"TumorDistribution_"+SampleID)
    except Exception, e:
        print e
        pass


if __name__ == '__main__':
  main(TissueID)

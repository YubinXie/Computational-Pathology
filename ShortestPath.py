import itertools
import math
from scipy import misc
from scipy.sparse.dok import dok_matrix
from scipy.sparse.csgraph import dijkstra
import operator
from operator import sub, add
import numpy as np

#SampleID_List=["410200_2", "410200_2", "423690_1", "423690_2", "406786_2", "459591_1", "459591_2"]
OutputFolder="Output/"

def main(SampleID):

    
    print SampleID
    # Load the image from disk as a numpy ndarray
    original_img = misc.imread('Output/Segmentated_Thinned'+SampleID+'.png')

# Create a flat color image for graph building:
    img = original_img[:, :, 0] + original_img[:, :, 1] + original_img[:, :, 2]


# Defines a translation from 2 coordinates to a single number
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
            if NearValue>=2:
                continue
            if CornerValue>=2:
                continue
                #One pixel as start point
            if NearValue==0:
                if CornerValue==1:
                    sourse=(i,j)
                    print "1.1",sourse
        #Two or more pixel as start point
            elif NearValue==1:
                if CornerValue==1:
                    NearDirection=NearPosition[NearValueList.index(1)]
                    CornerDirection=CornerPosition[CornerValueList.index(1)]
                    if (NearDirection[0]!=CornerDirection[0]) and (NearDirection[1]!=CornerDirection[1]):
                        continue
                Direction=NearPosition[NearValueList.index(1)]
                AgainstDirectionIndex=3-NearValueList.index(1)
                NextPointValue=1
                NextPoint=(i,j)
                while NextPointValue:
                    NextPoint = tupleadd(NextPoint, Direction)
                    if NextPoint[0]>=img.shape[0] or NextPoint[1]>=img.shape[1]:
                        break
                    NextPointValue=img[NextPoint]
                if NextPoint[0]>=img.shape[0] or NextPoint[1]>=img.shape[1]:
                    continue
                EndPoint= tuple(map(sub, NextPoint, Direction))
                EndNearValueList=[]
                EndCornerValueList=[]
                EndNearValue=0
                EndCornerValue=0
                for direction in range(4):
                    EndNearPoint=tupleadd(EndPoint,NearPosition[direction])
                    EndNearValue=EndNearValue+img[EndNearPoint]
                    EndNearValueList.append(img[EndNearPoint])
                    EndCornerPoint=tupleadd(EndPoint,CornerPosition[direction])
                    if EndCornerPoint[0]>=img.shape[0] or EndCornerPoint[1]>=img.shape[1]:
                        break
                    EndCornerValue=EndCornerValue+img[EndCornerPoint]
                    EndCornerValueList.append(img[EndCornerPoint])
                if EndNearValue==1:
                    if EndCornerValue==1:
                        sourse=(i,j)

                if EndNearValue==2:
                    if EndCornerValue==0:
                        sourse=(i,j)
                    if EndCornerValue==1:
                        EndNearValueList[AgainstDirectionIndex]=0
                        NearDirection=NearPosition[EndNearValueList.index(1)]
                        CornerDirection=CornerPosition[EndCornerValueList.index(1)]
                        if (NearDirection[0]==CornerDirection[0]) or (NearDirection[1]==CornerDirection[1]):
                            #print CornerDirection,NearDirection
                            #print EndNearValueList
                            sourse=(i,j)
            if sourse!=None:
                if sourse not in SourceList:
                    SourceList.append(sourse)
    print (SourceList)












# A sparse adjacency matrix.
# Two pixels are adjacent in the graph if both are painted.


adjacency = dok_matrix((img.shape[0] * img.shape[1],
                        img.shape[0] * img.shape[1]), dtype=bool)

# The following lines fills the adjacency matrix by
directions = list(itertools.product([0, 1, -1], [0, 1, -1]))
#print directions
for i in range(1, img.shape[0] - 1):
    for j in range(1, img.shape[1] - 1):
        if not img[i, j]:
            continue

        for y_diff, x_diff in directions:
            if img[i + y_diff, j + x_diff]:
                adjacency[to_index(i, j),
                          to_index(i + y_diff, j + x_diff)] = True

# We chose two arbitrary points, which we know are connected
source = to_index(SourceList[0][0],SourceList[0][1])
target = to_index(SourceList[1][0],SourceList[1][1])

# Compute the shortest path between the source and all other points in the image
_, predecessors = dijkstra(adjacency, directed=False, indices=[source],
                           unweighted=True, return_predecessors=True)
# Constructs the path between source and target
pixel_index = target
pixels_path = []
while pixel_index != source:
    pixels_path.append(pixel_index)
    pixel_index = predecessors[0, pixel_index]

# The following code is just for debugging and it visualizes the chosen path
import matplotlib.pyplot as plt
Path=[]
Distance=0
DistanceDic={}
DistanceList=[]
LastPoint=SourceList[1]
pixels_path.append(source)
for pixel_index in pixels_path:
    i, j = to_coordinates(pixel_index)
    original_img[i, j, 1] = 0
    Path.append((i,j))
    Distance=Distance+distance(LastPoint,(i,j))
    DistanceList.append(distance(LastPoint,(i,j)))
    DistanceDic[(i,j)]=sum(DistanceList[:])
    LastPoint=(i,j)

Path.append(SourceList[0])
#print Path
print Distance #DistanceList

for point in SourceList:
    original_img[point[0],point[1],0]=0

#plt.imshow(original_img)
#plt.show()


Label_Org_img = misc.imread('Output/Segmentated_Thinned'+SampleID+'_Label.png')
Label_img = Label_Org_img[:, :, 0] + Label_Org_img[:, :, 1] + Label_Org_img[:, :, 2]
Label_Width=Label_img.shape[0]
Label_Height=Label_img.shape[1]
LabelNumber=0
for i in range(0,Label_Width-2):
    for j in range(0,Label_Height-2):
        if Label_img[i,j]>=1:
            Label_img[i,j]=1
            LabelNumber+=1
if LabelNumber==0:
    print "No label!"



Sample={}
for sample in Path:
    Sample[sample]=0

for i in range(0,Label_Width-1):
    for j in range(0,Label_Height-1):
        #if i==0 or i==Label_Width-1:
          #  Label_img[i,j]=0
        #if j==0 or j==Label_Height-1:
          #  Label_img[i,j]=0
        if not Label_img[i,j]:
            continue
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

AverageXcoordinate=[]
AverageYcoordinate=[]
for x in range(len(Xcoordinate)):
    if x%3==0:
        AverageXcoordinate.append(sum(Xcoordinate[x:x+2])/len(Xcoordinate[x:x+2]))
        AverageYcoordinate.append(sum(Ycoordinate[x:x+2])/len(Ycoordinate[x:x+2]))

#print AverageXcoordinate
plt.plot(Xcoordinate,Ycoordinate)
#plt.show()

plt.savefig(OutputFolder+"TumorDistribution_"+SampleID)

with open(OutputFolder+"TumorDistribution_"+SampleID+".txt","w") as OpenOutput:
    for x in range(len(Xcoordinate)):
        OpenOutput.writelines(str(Xcoordinate[x])+"\t" +str(Ycoordinate[x]) + "\n\t\t")

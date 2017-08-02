##Created at 08/02/2017 by Yubin Xie, MSKCC
##Modified at #### by ***
## This script is to find the starting points in the binary images and find the shortest path between them
import itertools
import math
from scipy import misc
from scipy.sparse.dok import dok_matrix
from scipy.sparse.csgraph import dijkstra
import operator
from operator import sub, add
import numpy as np
from matplotlib import pyplot as plt
OutputFolder=""
SampleID="path"

def main(SampleID):

    print SampleID
    # Load the image
    original_img = misc.imread(SampleID+'.png')
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

    # Choose first two point
    source = to_index(SourceList[0][0],SourceList[0][1])
    target = to_index(SourceList[1][0],SourceList[1][1])

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
    for point in pixels_path:
        point=to_coordinates(point)
        Path.append(point)
        original_img[point[0],point[1],1]=0
    print Path
    plt.imshow(original_img)
    plt.show()

if __name__ == '__main__':
  main(SampleID)

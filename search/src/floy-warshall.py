import numpy as np
from representation import generateMatrix

def inmaze(pos,n):
    return all([0<=pos[0],pos[0]<n,0<=pos[1],pos[1]<n]) 

def get_successors(maze,successors,n):
    size=n*n
    dirs= [[0,1],[1,0],[0,-1],[-1,0]] #right, down, left, up
    for i in range(size-1):
        #get i-th state's position and jump number in the maze
        row = i/n
        col = i%n
        step = maze[row,col]
        # iterate 4 directions to gain all the successors 
        for move in dirs:
            pos= [row+int(move[0])*step, col+int(move[1])*step]
            if inmaze(pos, n):
                child = pos[0]*n+pos[1]
                successors[i].append(child)

def floyd(distance,successors,size):
    #careful to not to misuse the goal state
    for i in range(size):
        for j in range(size):
            distance[i][j] = -1
    
    for i in range(size-1): #don't include the goal state
        distance[i][i] = 0
        for j in successors[i]:
            distance[i][j]=1
    
    for k in range(size):
        for i in range(size):
            for j in range(size):
                if distance[i,k] != -1 and distance[k,j] != -1:
                    if distance[i,j] == -1 or distance[i,j]>distance[i,k]+distance[k,j]:
                        distance[i,j]= distance[i,k]+distance[k,j]

def better(maze,n):
    size=n*n
    successors=[[] for x in range(size)]
    get_successors(maze,successors,n)
    distance = np.zeros(shape=(size,size),dtype=np.int)
    floyd(distance,successors,size)
    return distance[0,size-1]
    

def main():
    while(1):
        n=int(input("Input the maze size (5-10): "))
        maze = generateMatrix(n)
        print(better(maze,n))
        print(maze)

if __name__ == "__main__": main()


import Queue
import numpy as np
from representation import generateMatrix


def inmaze(pos,n):
    return all([0<=pos[0],pos[0]<n,0<=pos[1],pos[1]<n]) 

def bfs(maze,n):
    goal = [n-1,n-1]
    flag = np.zeros((n,n))
    q = Queue.Queue()
    next = [[0,1],[1,0],[0,-1],[-1,0]] #right, down, left, up

    q.put([[0,0],0])
    while q.empty() != True:
        tmp = q.get()
        head = tmp[0] 
        path_cost = tmp[1]
        flag[head[0],head[1]]=1

        #print(head,goal)
        if head == goal:
            return -path_cost #inorder to return negtive value
        elif path_cost > n*n:
            break

        step = maze[head[0],head[1]]
        for move in next:
            pos= [head[0]+int(move[0])*step, head[1]+int(move[1])*step]
            if inmaze(pos, n):
                if flag[pos[0],pos[1]]==0:
                    q.put([pos,path_cost+1])
    return 10000

def evaluation(maze,n):
    #print(maze)
    #print(bfs(maze,n))
    return(bfs(maze,n))

def main():
    while(1):
        n=int(input("Input the maze size (5-10): "))
        maze = generateMatrix(n)
        print(evaluation(maze,n))
if __name__ == "__main__": main()


import numpy as np
import random as rd
from evaluation import evaluation 
from representation import generateMatrix

def annealing(n,cnt):
    maze = generateMatrix(n)
    first = evaluation(maze,n)
    minima = first
    print("Init energy: %d" %(first))
    #print(maze)
    backup = maze;

    temperature=2.5
    decay = 0.99999
    
    for i in range(cnt):
        #randomly choose a cell to change, make sure it's not goal state
        goal=[n-1,n-1]
        new_cell=goal
        while new_cell == goal:
            row = rd.randint(0,n-1)
            col = rd.randint(0,n-1)
            new_cell=[row,col]
    
        #change the jump number, make sure it's not same as before
        old_step = maze[row,col]
        new_step = old_step
        maxrnd = max(n-row-1,n-col-1,row,col)
        while new_step == old_step:
            new_step = rd.randint(1,maxrnd) 
        maze[row,col] = new_step
    
        #get the new energy
        nexte = evaluation(maze,n)
        if i % 1000 == 0:
            print("Current energy: %d" %(minima))
            print("temp diff %d" %(first-nexte))
            print("temp %f" %(temperature*0.5))
            #print(np.exp((first-nexte)/temperature))
            

        #if nexte <= first or rd.random()< np.exp((first-nexte)/temperature):
        if nexte <= first or rd.random()< temperature*0.5:
            first = nexte # minima < nexte < first, not minima keep going
            if nexte < minima: #new minima, store the matrix
                minima = nexte
                backup = maze
        else:
            maze = backup
        temperature = temperature*decay
    
    return (minima,maze)
    
if __name__ == "__main__" :
    #n=int(input("Input the maze size (5-10): ")) 
    #cnt=int(input("Input the number of iterations: "))
    print("------10000~90000------")
    m1=[]
    m2=[]
    for x in range(10000,100000,5000):
        minima, maze = annealing(5,x)
        print(minima)
        print(maze)
        m1.append(minima)
    print(m1)
    #print(maze)
    #print(minima)





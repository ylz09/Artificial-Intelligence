import random as rd
from floydwarshall import better
from representation import generateMatrix

def random_walk(n,cnt):
    maze = generateMatrix(n)
    first = better(maze,n)
    minima = first
    print("Init energy: %d" %(first))
    #print(maze)
    backup = maze;
    
    for i in range(cnt):
        #randomly choose a cell to change, make sure it's not goal state
        #if i % 100 == 0:
        #    print("Current energy: %d" %(minima))
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
        nexte = better(maze,n)
        if nexte < first:
            first = nexte # minima < nexte < first, not minima keep going
            if nexte < minima: #new minima, store the matrix
                minima = nexte
                backup = maze
        else:
            maze = backup
    
    return (minima,maze)

def test():
    for x in range(10000,100000,5000):
        minima, maze = random_walk(5,x)
        print(maze)
        print(minima)
        
    
if __name__ == "__main__" :
    #tg=int(input("1 to batch test, 0 to sigle test:")) 
    tg=0
    if tg:
        test()
    else:
        n=int(input("Input the maze size (5-10): ")) 
        cnt=int(input("Input the number of iterations: "))
        minima, maze = random_walk(n,cnt)
        print(maze)
        print(minima)





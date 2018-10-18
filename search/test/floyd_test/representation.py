import numpy as np
import random

def generateMatrix(n):
    maze= np.zeros(shape=(n,n),dtype=np.int)
    
    for i in range(n):#careful : i,j starts from 0
        for j in range(n):
            maxrnd = max(n-i-1,n-j-1,i,j) #max steps can go
            step = random.randint(1,maxrnd)
            maze[i,j] = step
    
    maze[n-1,n-1]=0 # down right:goal:0
    return maze

def main():
    while(1):
        n = int(input("Input Maze size (5-10), 0 to quit: "))
        if n == 0:
            break
        elif n > 10 or n < 5:
            print("Error input, try again!")
            continue
        maze = generateMatrix(n)
        print(maze)

if __name__ == "__main__": main()

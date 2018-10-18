from generation import random_walk
    
def random_restart():
    it=int(input("Input the number of restarts: ")) 
    n=int(input("Input the maze size (5-10): ")) 
    cnt=int(input("Input the iteration number per restart: ")) 
    mini=0
    for i in range(it):
        minima,maze=random_walk(n,cnt)
        if minima < mini:
            best = maze 
            mini = minima
    return mini,best
    
if __name__ == "__main__" :
    mini, best = random_restart()
    print("minimum energy: %d" %(mini))
    print("best maze:")
    print(best)





from generation import random_walk
    
def random_restart(it,n,cnt):
    mini=0
    for i in range(it):
        minima,maze=random_walk(n,cnt)
        if minima < mini:
            best = maze 
            mini = minima
    return mini,best

def test():
    m=[]
    for it in range(1,100):
        mini, best = random_restart(it,5,10000)
        print(mini)
        print(best)
        m.append(mini)
    print(m)
    
    
if __name__ == "__main__" :
    #t=int(input("1 to batch test, 0 to sigle test:")) 
    t=1
    if t:
        test()
    else:
        it=int(input("Input the number of restarts: ")) 
        n=int(input("Input the maze size (5-10): ")) 
        cnt=int(input("Input the iteration number per restart: ")) 
        mini, best = random_restart(it,n,cnt)
        print("minimum energy: %d" %(mini))
        print("best maze:")
        print(best)





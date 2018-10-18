This project is to generate the best maze ussing random walk or stochastic local search.
The best maze here means that this maze need most steps to travel from the start to the goal position.

First, how do we evaluate the maze? We can use BFS to measure the distance from the start to goal.
BFS can guarentee we can find a path, but we don't know whether it's shortest or not since each cell has different step size.

Second, in order to find the best maze from the current maze, we need change a maze cell legally and randomly.
At the same time, we should make sure that this change get can a better maze, if not we discard this change and recover the maze.

Third, how many times we can change the maze to get the "best" maze? There's no standard, but intuitively, the more the better.
Since we only consider the effective change. But we can't run the program endlessly. So we need do some experiments to see what's 
the best iterations we need for a certain size of maze.

Last, this stochastic method only consider the better moves, while ignore the worse moves, which will probably fall into the 
local minima. We don't want that. How to escape the local minima? 
There are several ways. The most popular is the random restart and uphill walk. 
Random restart is easy. We just need restart the search several times while keeping the best results.
Uphill walk means we allow the worse moves in the ceratin probability, for example, 0.001, this probability
should not be very large or we will never reach any minima (both local and global), also can't too samll, or 
we will not escape the local minima. Which p is best? Only god knows!!

This is very interesting and inspired project to feel the primitive power of AI.

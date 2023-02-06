# evolutionaryrobotics

link: 

Goal: have the creature "pronk/twerk" this was done by minimizing the time all legs touched the ground 

When trying to think of a fitness function, I created a leetcode-esque problem to solve.
Given an array of N by M with values -1 or 1 (whether or not touching the ground)
return the sum of length of contiguous subarrays where contig subarr means all -1 or 1s for some period of time in an efficient manner.

This is so that we want all legs in the air (as if jumping) but we want the length of contiguous subarray because or else it will just learn to "shuffle" its feet so that it gets a high fitness score.

abbreviating a 2d array into 1d where T means all -1s or 1s and F means mixture of 1s and -1s,
e.g. arry = [[1,1],[-1,-1],[1,-1],[1,1],[-1,1],[1,-1],[1,-1],[1,1]]
becomes [T,T,F,T,F,F,F,T] and the expected output is (2+1+1)=4


follow up
subarray of length at least N//k 

for example previous example has N=8, let k =4 so subarr of at least 8//4 = 2 (aka chains at least n//k% of the whole chain length so in this case at least 20%)
then func([T,T,F,T,F,F,F,T]) → 2
since the other 2 Ts have subarr length=1

This followup describes a tunable parameter to affect the fitness function. We want to ignore small instances of feet up in the air and only consider those with long hang/air time. In practice, a 5% was set because anything larger did not yield empirically positive results in generating the pronking behavior.

HOW TO RUN:
run `python search.py` but replace the parts where it calls a subprocess with your own path to python binary because mine is miniconda.


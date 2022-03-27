#!/usr/bin/env python
# coding: utf-8

# Define a function to calculate the probability of changes

from math import exp

def calc_prob(current, better, temp):
    current = 1000 - current
    best = 1000 - better
    if temp < 1:  # if the temperature is less than 1, we consider it is 0, so no changes occur
        return 0
    elif current > best:  # if the current state is worse, make the change with certain probability
        return exp((-1)*(current - better) / temp)
    else:  # make change 
        return 1


# Open the given file and initialize values


infile = open('Program2Input.txt', 'r')
line = infile.readline()
items = []
numOfPack = 25  # the number of packed items

t = 60000  # temperature

constant = 0.99  # constant to decrease the temperature

changes = 4000  # 10N
trials = 40000  # 100N

sol = 0, 0  # a tuple of the solution


# Read the file 
# Iterating through each line of file and assign the data to the list 'items' which is 2d array.   
# The default values in the file is string, so if it is a number, it should be converted to int/float.   
# After it is done, close the file.



while line != "":
    item = line.split()  # remove the whitespace between strings in each line
    item[0] = float(item[0])  # convert the string to float
    item[1] = float(item[1])
    items.append(item)
    
    line = infile.readline()  # go to the next line
infile.close()  # close the file


# Find the best number of packing item
# Import NumPy to use np.mean, np.sum and np.random.choice. np.mean and np.sum is very helpful for ndarray.   
# np.random.choice can generate list of random integers.   
# Devide 500 by mean weight so that we can assume the average number of packing items.


import numpy as np

mean = np.mean(items, axis= 0)  # it returns the list [mean(items[][0]),  mean(items[][1])]
numOfPack = int(500 / mean[1])
print(numOfPack)

# print(items) 


# Run simulated annealing
# Create the list of random integers range(0, 400) without duplication. Use the list for the random selection from items.   
# Get the sum of utilities and weights to find the better solution (utility).


from random import random

while changes != 0 and trials != 0:  # iterate until it reaches 10N changes or 100N trials
    
    random_select = np.random.choice(400, numOfPack, replace=False)  # select 'numOfPack' integers from 0 to 399 (index)
    
    selected = [items[i] for i in random_select]  # pick the values have the index
    
    # np.sum returns the list [sum(items[][0]),  sum(items[][1])]
    total_util = np.sum(selected, axis=0)[0]  # index 0 for utilities
    total_weight = np.sum(selected, axis=0)[1]  # index 1 for weights
    
    # penalty of -20 utility for every pound over the weight limit.
    if total_weight > 500:
        total_util -= 20
        
    # random() returns float between 0 and 1. If it is less than certain probabilites, make a change
    if random() < calc_prob(total_util, sol[0], t):
        sol = total_util, total_weight
        changes -= 1  # count a change
    
    trials -= 1  # count a trial
    t *= constant  # decrease the temperature


# Display the result

# Write to the output file
outfile = open('Result.txt', 'w')
outfile.write("The better utilities of"+" "+str(numOfPack)+" "+"items are"+" "+str(round(sol[0], 1))+" "+"with"
              +" "+str(round(sol[1], 1))+" "+"pounds"+"\n")
outfile.write("The number of changes is"+" "+str(4000-changes)+" "+"and trials is"+" "+str(40000-trials))
outfile.close()

# Just print
print(f"The better utilities of {numOfPack} items are {round(sol[0], 1)} with {round(sol[1], 1)} pounds")
print(f"The number of changes is {4000-changes} and trials is {40000-trials}")

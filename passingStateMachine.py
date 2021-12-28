# Class: CS 330-02
# Project: Programming Assignment 4
# Purpose: Implement a hard-coded state machine
# Author: Matthew Hise, mrh0036@uah.edu
# Date Created: 04/13/2021
# Date Modified: 04/13/2021

from enum import IntEnum
import random

# Initialize global variables and output file

# Scenario 1 prints each iteration in addition to overall results, while Scenario 2 outputs results only
scenario = 1
trace = (True, False)[scenario - 1]
debug = False
iterations = (100, 1000000)[scenario - 1]
random.seed()

f = open('CS 330, State machines, Scenario ' + str(scenario) + ' Output.txt', 'w')
state_counts = [0, 0, 0, 0, 0, 0, 0]
transition_counts = [0, 0, 0, 0, 0, 0, 0, 0, 0]
transition_probs = ([0.8, 0.4, 0.3, 0.4, 0.3, 0.3, 0.8, 0.8, 0.8],
                             [0.8, 0.5, 0.4, 0.3, 0.2, 0.3, 0.8, 0.8, 0.8])[scenario - 1]

# Define the states

class State(IntEnum):
    FOLLOW = 1
    PULL_OUT = 2
    ACCELERATE = 3
    PULL_IN_AHEAD = 4
    PULL_IN_BEHIND = 5
    DECELERATE = 6
    DONE = 7

# Define the stub functions

def follow():
    if (trace):
        f.write("State: 1 Follow\n")
    state_counts[State.FOLLOW - 1] += 1
    
def pull_out():
    if (trace):
        f.write("State: 2 Pull Out\n")
    state_counts[State.PULL_OUT - 1] += 1

def accelerate():
    if (trace):
        f.write("State: 3 Accelerate\n")
    state_counts[State.ACCELERATE - 1] += 1

def pull_in_ahead():
    if (trace):
        f.write("State: 4 Pull In Ahead\n")
    state_counts[State.PULL_IN_AHEAD - 1] += 1

def pull_in_behind():
    if (trace):
        f.write("State: 5 Pull In Behind\n")
    state_counts[State.PULL_IN_BEHIND - 1] += 1

def decelerate():
    if (trace):
        f.write("State: 6 Decelerate\n")
    state_counts[State.DECELERATE - 1] += 1

def done():
    if (trace):
        f.write("State: 7 Done\n")
    state_counts[State.DONE - 1] += 1

f.write("Name: Matthew Hise\nClass: CS 330-02\n\n")

# Enter state machine and begin loop

for i in range(iterations):
    if(trace):
        f.write("Iteration: " + str(i + 1) + "\n")

    state = State.FOLLOW
    follow()

    # Now that in Follow state, run state machine until Done

    while(state != State.DONE):
        r = random.random()

        if(state == State.FOLLOW):
            if(r < transition_probs[0]):
                transition_counts[0] += 1
                state = State.PULL_OUT
                pull_out()
            else:
                follow()
        
        elif(state == State.PULL_OUT):
            p_one = transition_probs[1]
            p_two = p_one + transition_probs[3]
            if(r < p_one):
                transition_counts[1] += 1
                state = State.ACCELERATE
                accelerate()
            elif(r < p_two):
                transition_counts[3] += 1
                state = State.PULL_IN_BEHIND
                pull_in_behind()
            else:
                pull_out()
                
        elif(state == State.ACCELERATE):
            p_one = transition_probs[2]
            p_two = p_one + transition_probs[4]
            p_three = p_two + transition_probs[5]
            if(r < p_one):
                transition_counts[2] += 1
                state = State.PULL_IN_AHEAD
                pull_in_ahead()
            elif(r < p_two):
                transition_counts[4] += 1
                state = State.PULL_IN_BEHIND
                pull_in_behind()
            elif(r < p_three):
                transition_counts[5] += 1
                state = State.DECELERATE
                decelerate()
            else:
                accelerate()
                
        elif(state == State.PULL_IN_AHEAD):
            if(r < transition_probs[8]):
                transition_counts[8] += 1
                state = State.DONE
                done()
            else:
                pull_in_ahead()
                
        elif(state == State.PULL_IN_BEHIND):
            if(r < transition_probs[6]):
                transition_counts[6] += 1
                state = State.FOLLOW
                follow()
            else:
                pull_in_behind()
                
        elif(state == State.DECELERATE):
            if(r < transition_probs[7]):
                transition_counts[7] += 1
                state = State.PULL_IN_BEHIND
                pull_in_behind()
            else:
                decelerate()

        else:
            print("Error! Invalid state value.")

    # Put a blank line in between iterations if outputting each iteration
    if(trace):
        f.write("\n")

# Calculate the state and transition totals

total_state_count = sum(state_counts)
total_transition_count = sum(transition_counts)

# Output the summary of all iterations to the file

f.write("Scenario: " + str(scenario) + "\n")
f.write("Iterations: " + str(iterations) + "\n")
f.write("State counts: " + ' '.join([str(elem) for elem in state_counts]) + "\n")
f.write("State frequencies: " + ' '.join(['{:.3f}'.format(elem / total_state_count) for elem in state_counts]) + "\n")
if(debug):
    f.write("Transition counts: " + ' '.join([str(elem) for elem in transition_counts]) + "\n")
    f.write("Transition frequencies: " + ' '.join(['{:.3f}'.format(elem / total_transition_count) for elem in transition_counts]) + "\n")


f.close()


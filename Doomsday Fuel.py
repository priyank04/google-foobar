'''
3.1 Doomsday Fuel

Doomsday Fuel
=============

Making fuel for the LAMBCHOP's reactor core is a tricky process because of the exotic matter involved. It starts as raw ore, then during processing, begins randomly changing between forms, eventually reaching a stable form. There may be multiple stable forms that a sample could ultimately reach, not all of which are useful as fuel. 

Commander Lambda has tasked you to help the scientists increase fuel creation efficiency by predicting the end state of a given ore sample. You have carefully studied the different structures that the ore can take and which transitions it undergoes. It appears that, while random, the probability of each structure transforming is fixed. That is, each time the ore is in 1 state, it has the same probabilities of entering the next state (which might be the same state).  You have recorded the observed transitions in a matrix. The others in the lab have hypothesized more exotic forms that the ore can become, but you haven't seen all of them.

Write a function solution(m) that takes an array of array of nonnegative ints representing how many times that state has gone to the next state and return an array of ints for each terminal state giving the exact probabilities of each terminal state, represented as the numerator for each state, then the denominator for all of them at the end and in simplest form. The matrix is at most 10 by 10. It is guaranteed that no matter which state the ore is in, there is a path from that state to a terminal state. That is, the processing will always eventually end in a stable state. The ore starts in state 0. The denominator will fit within a signed 32-bit integer during the calculation, as long as the fraction is simplified regularly. 

For example, consider the matrix m:
[
  [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
  [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
  [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
  [0,0,0,0,0,0],  # s3 is terminal
  [0,0,0,0,0,0],  # s4 is terminal
  [0,0,0,0,0,0],  # s5 is terminal
]
So, we can consider different paths to terminal states, such as:
s0 -> s1 -> s3
s0 -> s1 -> s0 -> s1 -> s0 -> s1 -> s4
s0 -> s1 -> s0 -> s5
Tracing the probabilities of each, we find that
s2 has probability 0
s3 has probability 3/14
s4 has probability 1/7
s5 has probability 9/14
So, putting that together, and making a common denominator, gives an answer in the form of
[s2.numerator, s3.numerator, s4.numerator, s5.numerator, denominator] which is
[0, 3, 2, 9, 14].

Languages
=========

To provide a Java solution, edit Solution.java
To provide a Python solution, edit solution.py

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Java cases --
Input:
Solution.solution({{0, 2, 1, 0, 0}, {0, 0, 0, 3, 4}, {0, 0, 0, 0, 0}, {0, 0, 0, 0,0}, {0, 0, 0, 0, 0}})
Output:
    [7, 6, 8, 21]

Input:
Solution.solution({{0, 1, 0, 0, 0, 1}, {4, 0, 0, 3, 2, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}})
Output:
    [0, 3, 2, 9, 14]

-- Python cases --
Input:
solution.solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]])
Output:
    [7, 6, 8, 21]

Input:
solution.solution([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
Output:
    [0, 3, 2, 9, 14]

Use verify [file] to test your solution and see how it does. When you are finished editing your code, use submit [file] to submit your answer. If your solution passes the test cases, it will be removed from your home folder.

'''

import unittest
from fractions import Fraction as frac
import operator

def transposeMatrix(m):
    return map(list,zip(*m))

def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def getMatrixDeternminant(m):
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
    return determinant

def getMatrixInverse(m):
    determinant = getMatrixDeternminant(m)
    if len(m) == 2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]]

    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m,r,c)
            cofactorRow.append(((-1)**(r+c)) * getMatrixDeternminant(minor))
        cofactors.append(cofactorRow)
    cofactors = transposeMatrix(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/determinant
    return cofactors

def multiplyMatrices(m1,m2):
    result = generate2DList(len(m1),len(m2[0]))
    for i in range(len(m1)):  
        for j in range(len(m2[0])):  
            for k in range(len(m2)):  
                result[i][j] += m1[i][k] * m2[k][j]  
    return result
    

def subtractMatrices(m1,m2):
    diff = []
    for row in range(len(m1)):
        diff.append(list(map(operator.sub, m1[row], m2[row])))
    return diff

def generate2DList(rows,cols):
    a = []
    for row in range(rows):
        a += [[0] * cols]
    return a

def generateIdentityMatrix(rows,cols):
    a = generate2DList(rows,cols)
    for cell in range(rows):
        a[cell][cell] = 1
    return a

def getSubmatrix(m,row,col):
    new_m = []

    for i in row:
        new_row = []
        for j in col:
            new_row.append(m[i][j])
        new_m.append(new_row)
    return new_m      

def transform_matrix(m):
    for i, row in enumerate(m):
        row_sum = sum(row)
        if row_sum == 0:
            m[i][i] = 1
        else:
            for j, col in enumerate(row):
                m[i][j] = frac(col,row_sum)               
                
def solution(m):
    terminal_states, non_terminal_states = [[],[]]
    for index, row in enumerate(m):
        if sum(row) == 0:
            terminal_states.append(index)
        else:
            non_terminal_states.append(index)
    
    # 1) Transforming matrix
        # Stored value in fractions for NON-TERMINAL STATES
        # Set value 1 for TERMINAL STATES
    transform_matrix(m)

    # 2) Get R and Q
    submatrix_Q = getSubmatrix(m,non_terminal_states,non_terminal_states)
    submatrix_R = getSubmatrix(m,non_terminal_states,terminal_states)
    print(submatrix_Q)
    
    # 3) generare Identity matrix
    iden_matrix = generateIdentityMatrix(len(submatrix_Q),len(submatrix_Q))
    print(iden_matrix)

    # 4) Calculate I - Q
    diff_iq = subtractMatrices(iden_matrix,submatrix_Q)
    print(diff_iq)

    # 5) find F = inverse(I-Q)
    submatrix_F = getMatrixInverse(diff_iq)
    print(submatrix_F)

    # 6) Multiply F and R
    product_FR = multiplyMatrices(submatrix_F,submatrix_R)
    print(product_FR)




test_input1 = [
            [0, 2, 1, 0, 0],
            [0, 0, 0, 3, 4],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
test_input2 = [
            [0, 2, 1, 0, 0],
            [1, 0, 0, 3, 4],
            [0, 0, 4, 2, 0],
            [0, 2, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]        
         
solution(test_input1)
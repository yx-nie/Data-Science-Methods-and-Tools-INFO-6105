#!/usr/bin/env python
# coding: utf-8

# In[24]:


import numpy as np
A=np.array([[1,2],[2,3],[3,4],[4,5],[5,6]])
X=np.array([[10],[20]])
B=np.array([[1,0,0,0,0],[0,2,0,0,0],[0,0,3,0,0],[0,0,0,4,0],[0,0,0,0,5]])

##transpose X before doing the result of AX
print("the result of AX is:\n",np.multiply(A,X.T))

print("the result of BA is:\n",np.matmul(B,A))


# In[28]:


import numpy as np
A=np.array([[1,2],[2,3],[3,4],[4,5],[5,6]])
B=np.array([[1,0,0,0,0],[0,2,0,0,0],[0,0,3,0,0],[0,0,0,4,0],[0,0,0,0,5]])
print("the rank of matrix A is:\n",np.linalg.matrix_rank(A))
print("the rank of matrix B is:\n",np.linalg.matrix_rank(B))
BA=np.matmul(B,A)
print(BA)
print("the rank of matrix BA is:\n",np.linalg.matrix_rank(BA))

##BA has the same rank as A but different from the rank of B.
##the reason is BA has the same shape of A, and its rank has to be no larger than the maximum number of columns of the matrix


# In[8]:


import numpy as np
A=np.array([[-2,1,8],
           [-1,-1,7],
           [3,0,4]])
B=np.array([[5,0,-7],
           [6,3,-9],
           [-2,-2,0]])
C=np.array([[6,3,-1],
           [2,4,5],
           [-1,-1,8]])
D=np.concatenate((A,B,C),axis=0)
print(D)

b=np.array([[3],[-10],[2]])
## For the result of ||(D.T)*x-b||^2
## According the least square equations, x=((D*(D.T)^(-1))*(D)*b
result_1=np.matmul(D,(D.T))
inv_result=np.linalg.inv(result_1)
result_2=np.matmul(inv_result, D)
x=np.matmul(result_2,b)

print(x)


# In[ ]:





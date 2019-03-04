import copy
import string
from itertools import chain
from numpy import array, matrix, matmul,dot,resize,asanyarray,append,vsplit,concatenate,flip,absolute,arange,transpose

"""
Maybe make colors assigned to numbers? 0=white,1=green,2=red,3=yellow,4=blue,5=orange
"""

def rot90(m, k=1, axes=(0,1)):
    axes = tuple(axes)
    if len(axes) != 2:
        raise ValueError("len(axes) must be 2.")

    m = asanyarray(m)

    if axes[0] == axes[1] or absolute(axes[0] - axes[1]) == m.ndim:
        raise ValueError("Axes must be different.")

    if (axes[0] >= m.ndim or axes[0] < -m.ndim
        or axes[1] >= m.ndim or axes[1] < -m.ndim):
        raise ValueError("Axes={} out of range for array of ndim={}."
            .format(axes, m.ndim))

    k %= 4

    if k == 0:
        return m[:]
    if k == 2:
        return flip(flip(m, axes[0]), axes[1])

    axes_list = arange(0, m.ndim)
    (axes_list[axes[0]], axes_list[axes[1]]) = (axes_list[axes[1]],
                                                axes_list[axes[0]])

    if k == 1:
        return transpose(flip(m,axes[1]), axes_list)
    else:
        # k == 3
        return flip(transpose(m, axes_list), axes[1])

def flip(m, axis):
    if not hasattr(m, 'ndim'):
        m = asarray(m)
    indexer = [slice(None)] * m.ndim
    try:
        indexer[axis] = slice(None, None, -1)
    except IndexError:
        raise ValueError("axis=%i is invalid for the %i-dimensional input array"
                         % (axis, m.ndim))
    return m[tuple(indexer)]


Cube = array([
    [0,0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1,1],
    [2,2,2,2,2,2,2,2,2],
    [3,3,3,3,3,3,3,3,3],
    [4,4,4,4,4,4,4,4,4],
    [5,5,5,5,5,5,5,5,5]
    ])
testCube =array([[1,2,3,4,5,6,7,8,9],[10,11,12,13,14,15,16,17,18],[19,20,21,22,23,24,25,26,27],[28,29,30,31,32,33,34,35,36],[37,38,39,40,41,42,43,44,45],[46,47,48,49,50,51,52,53,54]])
#now time to math bash to find a matrix for a rotation
#right up affects some layers
def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i+n]


def rightUp(Cube):
    afterImage = resize(copy.deepcopy(Cube),(6,3,3))
    de =rot90(afterImage[2],-1)
    afterImage[2] = (de)
    A = array(afterImage[0])
    B = array(afterImage[1])
    C = array(afterImage[3])
    D = array(afterImage[5])
    A1 = dot(A,[[0],[0],[1]])
    B1 = dot(B,[[0],[0],[1]])
    C1 = dot(C,[[1],[0],[0]])
    D1 = dot(D,[[0],[0],[1]])
    afterImage[0]=append(A[:,[0,1]],B1,1)
    afterImage[1]=append(B[:,[0,1]],D1,1)
    afterImage[3]=append(flip(A1,0),C[:,[1,2]],1)
    afterImage[5]=append(D[:,[0,1]],flip(C1,0),1)
    return resize(afterImage,(6,9))

def rightDown(Cube):
    afterImage = resize(copy.deepcopy(Cube),(6,3,3))
    de =rot90(afterImage[2],1)
    afterImage[2] = (de)
    A = array(afterImage[0])
    B = array(afterImage[1])
    C = array(afterImage[3])
    D = array(afterImage[5])
    A1 = dot(A,[[0],[0],[1]])
    B1 = dot(B,[[0],[0],[1]])
    C1 = dot(C,[[1],[0],[0]])
    D1 = dot(D,[[0],[0],[1]])
    afterImage[0]=append(A[:,[0,1]],flip(C1,0),1)
    afterImage[1]=append(B[:,[0,1]],A1,1)
    afterImage[3]=append(flip(D1,0),C[:,[1,2]],1)
    afterImage[5]=append(D[:,[0,1]],B1,1)
    return resize(afterImage,(6,9))
def upLeft(Cube):
    afterImage = resize(copy.deepcopy(Cube),(6,3,3))
    de =rot90(afterImage[0],-1)
    afterImage[0] = (de)
    A = array(afterImage[1])
    B = array(afterImage[2])
    C = array(afterImage[3])
    D = array(afterImage[4])
    A1 = resize(A,(1,3))
    B1 = resize(B,(1,3))
    C1 = resize(C,(1,3))
    D1 = resize(D,(1,3))
    afterImage[1]=concatenate((B1, A[[1,2]]), axis=0)
    afterImage[2]=concatenate((C1, B[[1,2]]), axis=0)
    afterImage[3]=concatenate((D1, C[[1,2]]), axis=0)
    afterImage[4]=concatenate((A1, A[[1,2]]), axis=0)
    return resize(afterImage,(6,9))
def upRight(Cube):
    afterImage = resize(copy.deepcopy(Cube),(6,3,3))
    de =rot90(afterImage[0],1)
    afterImage[0] = (de)
    A = array(afterImage[1])
    B = array(afterImage[2])
    C = array(afterImage[3])
    D = array(afterImage[4])
    A1 = resize(A,(1,3))
    B1 = resize(B,(1,3))
    C1 = resize(C,(1,3))
    D1 = resize(D,(1,3))
    afterImage[1]=concatenate((D1, A[[1,2]]), axis=0)
    afterImage[2]=concatenate((A1, B[[1,2]]), axis=0)
    afterImage[3]=concatenate((B1, C[[1,2]]), axis=0)
    afterImage[4]=concatenate((C1, D[[1,2]]), axis=0)
    return resize(afterImage,(6,9))



def leftUp(Cube):
    afterImage = resize(copy.deepcopy(Cube),(6,3,3))
    de =rot90(afterImage[4],1)
    afterImage[4] = (de)
    A = array(afterImage[0])
    B = array(afterImage[1])
    C = array(afterImage[3])
    D = array(afterImage[5])
    A1 = dot(A,[[1],[0],[0]])
    B1 = dot(B,[[1],[0],[0]])
    C1 = dot(C,[[0],[0],[1]])
    D1 = dot(D,[[1],[0],[0]])
    afterImage[0]=append(B1,A[:,[1,2]],1)
    afterImage[1]=append(D1,B[:,[1,2]],1)
    afterImage[3]=append(C[:,[0,1]],flip(A1,0),1)
    afterImage[5]=append(flip(C1,0),D[:,[1,2]],1)
    return resize(afterImage,(6,9))

def leftDown(Cube):
    afterImage = resize(copy.deepcopy(Cube),(6,3,3))
    de =rot90(afterImage[4],-1)
    afterImage[4] = (de)
    A = array(afterImage[0])
    B = array(afterImage[1])
    C = array(afterImage[3])
    D = array(afterImage[5])
    A1 = dot(A,[[1],[0],[0]])
    B1 = dot(B,[[1],[0],[0]])
    C1 = dot(C,[[0],[0],[1]])
    D1 = dot(D,[[1],[0],[0]])
    afterImage[0]=append(flip(C1,0),A[:,[1,2]],1)
    afterImage[1]=append(A1,B[:,[1,2]],1)
    afterImage[3]=append(C[:,[0,1]],flip(D1,0),1)
    afterImage[5]=append(B1,D[:,[1,2]],1)
    return resize(afterImage,(6,9))
def downLeft(Cube):
    afterImage = resize(copy.deepcopy(Cube),(6,3,3))
    de =rot90(afterImage[5],1)
    afterImage[5] = (de)
    A = array(afterImage[1])
    B = array(afterImage[2])
    C = array(afterImage[3])
    D = array(afterImage[4])
    A1 = resize(vsplit(A,1)[0][2],(1,3))
    B1 = resize(vsplit(B,1)[0][2],(1,3))
    C1 = resize(vsplit(C,1)[0][2],(1,3))
    D1 = resize(vsplit(D,1)[0][2],(1,3))
    afterImage[1]=concatenate((A[[0,1]],B1), axis=0)
    afterImage[2]=concatenate((B[[0,1]],C1), axis=0)
    afterImage[3]=concatenate((C[[0,1]],D1), axis=0)
    afterImage[4]=concatenate((D[[0,1]],A1), axis=0)
    return resize(afterImage,(6,9))
def downRight(Cube):
    afterImage = resize(copy.deepcopy(Cube),(6,3,3))
    de =rot90(afterImage[5],-1)
    afterImage[5] = (de)
    A = array(afterImage[1])
    B = array(afterImage[2])
    C = array(afterImage[3])
    D = array(afterImage[4])
    A1 = resize(vsplit(A,1)[0][2],(1,3))
    B1 = resize(vsplit(B,1)[0][2],(1,3))
    C1 = resize(vsplit(C,1)[0][2],(1,3))
    D1 = resize(vsplit(D,1)[0][2],(1,3))
    afterImage[1]=concatenate((A[[0,1]],D1), axis=0)
    afterImage[2]=concatenate((B[[0,1]],A1), axis=0)
    afterImage[3]=concatenate((C[[0,1]],B1), axis=0)
    afterImage[4]=concatenate((D[[0,1]],C1), axis=0)
    return resize(afterImage,(6,9))




def frontClock(Cube):
    afterImage = resize(copy.deepcopy(Cube),(6,3,3))
    de =rot90(afterImage[1],-1)
    afterImage[1] = (de)
    A = array(afterImage[0])
    B = array(afterImage[2])
    C = array(afterImage[5])
    D = array(afterImage[4])
    A1 = resize(vsplit(A,1)[0][2],(3,1))
    B1 = resize(dot(B,[[1],[0],[0]]),(1,3))
    C1 = resize(vsplit(C,1)[0][0],(3,1))
    D1 = resize(dot(D,[[0],[0],[1]]),(1,3))
    afterImage[0]=concatenate((A[[0,1]],flip(D1,1)), axis=0)
    afterImage[2]=append(A1,B[:,[1,2]],1)
    afterImage[5]=concatenate((flip(B1,1),C[[1,2]]), axis=0)
    afterImage[4]=append(D[:,[0,1]],flip(C1,1),1)
    return resize(afterImage,(6,9))

def frontCounter(Cube):
    afterImage = resize(copy.deepcopy(Cube),(6,3,3))
    de =rot90(afterImage[1],1)
    afterImage[1] = (de)
    A = array(afterImage[0])
    B = array(afterImage[2])
    C = array(afterImage[5])
    D = array(afterImage[4])
    A1 = resize(vsplit(A,1)[0][2],(3,1))
    B1 = resize(dot(B,[[1],[0],[0]]),(1,3))
    C1 = resize(vsplit(C,1)[0][0],(3,1))
    D1 = resize(dot(D,[[0],[0],[1]]),(1,3))
    afterImage[0]=concatenate((A[[0,1]],B1), axis=0)
    afterImage[2]=append(flip(C1,0),B[:,[1,2]],1)
    afterImage[5]=concatenate((D1,C[[1,2]]), axis=0)
    afterImage[4]=append(D[:,[0,1]],flip(A1,0),1)
    return resize(afterImage,(6,9))

def backClock(Cube):
    afterImage = resize(copy.deepcopy(Cube),(6,3,3))
    de =rot90(afterImage[3],1)
    afterImage[3] = (de)
    A = array(afterImage[0])
    B = array(afterImage[2])
    C = array(afterImage[5])
    D = array(afterImage[4])
    A1 = resize(vsplit(A,1)[0][0],(3,1))
    B1 = resize(dot(B,[[0],[0],[1]]),(1,3))
    C1 = resize(vsplit(C,1)[0][2],(3,1))
    D1 = resize(dot(D,[[1],[0],[0]]),(1,3))
    print(D1)
    afterImage[0]=concatenate((flip(D1,1),A[[1,2]]), axis=0)
    afterImage[2]=append(B[:,[0,1]],A1,1)
    afterImage[5]=concatenate((C[[0,1]],flip(B1,1)), axis=0)
    afterImage[4]=append(flip(C1,1),D[:,[1,2]],1)
    return resize(afterImage,(6,9))
def backCounter(Cube):
    afterImage = resize(copy.deepcopy(Cube),(6,3,3))
    de =rot90(afterImage[3],-1)
    afterImage[3] = (de)
    A = array(afterImage[0])
    B = array(afterImage[2])
    C = array(afterImage[5])
    D = array(afterImage[4])
    A1 = resize(vsplit(A,1)[0][0],(3,1))
    B1 = resize(dot(B,[[0],[0],[1]]),(1,3))
    C1 = resize(vsplit(C,1)[0][2],(3,1))
    D1 = resize(dot(D,[[1],[0],[0]]),(1,3))
    print(D1)
    afterImage[0]=concatenate((B1,A[[1,2]]), axis=0)
    afterImage[2]=append(B[:,[0,1]],flip(C1,0),1)
    afterImage[5]=concatenate((C[[0,1]],D1), axis=0)
    afterImage[4]=append(flip(A1,0),D[:,[1,2]],1)
    return resize(afterImage,(6,9))


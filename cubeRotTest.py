import copy
import string
from itertools import chain


def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i+n]

def rightUp(Cube):
    #rotating
    afterImage = copy.deepcopy(Cube)
    de =list(zip(*reversed(list(chunks(Cube[2],3)))))
    table = str.maketrans('()','[]')
    thingy = eval(str(de).translate(table))
    afterImage[2] = list(chain.from_iterable(thingy))
    #moving elements
    afterImage[0][2]=Cube[1][2]
    afterImage[0][5]=Cube[1][5]
    afterImage[0][8]=Cube[1][8]
    afterImage[1][2]=Cube[5][2]
    afterImage[1][5]=Cube[5][5]
    afterImage[1][8]=Cube[5][8]
    afterImage[5][2]=Cube[3][6]
    afterImage[5][5]=Cube[3][3]
    afterImage[5][8]=Cube[3][0]
    afterImage[3][0]=Cube[0][8]
    afterImage[3][3]=Cube[0][5]
    afterImage[3][6]=Cube[0][2]
    return afterImage
def rightDown(Cube):
    #rotating
    afterImage = copy.deepcopy(Cube)
    de =list(zip(*(list(chunks(Cube[2],3)))))[::-1]
    table = str.maketrans('()','[]')
    thingy = eval(str(de).translate(table))
    afterImage[2] = list(chain.from_iterable(thingy))
    #moving elements
    afterImage[0][2]=Cube[3][6]
    afterImage[0][5]=Cube[3][3]
    afterImage[0][8]=Cube[3][0]
    afterImage[1][2]=Cube[0][2]
    afterImage[1][5]=Cube[0][5]
    afterImage[1][8]=Cube[0][8]
    afterImage[5][2]=Cube[1][2]
    afterImage[5][5]=Cube[1][5]
    afterImage[5][8]=Cube[1][8]
    afterImage[3][0]=Cube[5][8]
    afterImage[3][3]=Cube[5][5]
    afterImage[3][6]=Cube[5][2]
    return afterImage
def upRight(Cube):
    afterImage = copy.deepcopy(Cube)
    de =list(zip(*(list(chunks(Cube[0],3))[::-1])))
    table = str.maketrans('()','[]')
    thingy = eval(str(de).translate(table))
    afterImage[0] = list(chain.from_iterable(thingy))
    afterImage[1][0]=Cube[2][0]
    afterImage[1][1]=Cube[2][1]
    afterImage[1][2]=Cube[2][2]
    afterImage[2][0]=Cube[3][0]
    afterImage[2][1]=Cube[3][1]
    afterImage[2][2]=Cube[3][2]
    afterImage[3][0]=Cube[4][0]
    afterImage[3][1]=Cube[4][1]
    afterImage[3][2]=Cube[4][2]
    afterImage[4][0]=Cube[1][0]
    afterImage[4][1]=Cube[1][1]
    afterImage[4][2]=Cube[1][2]
    return afterImage
def upLeft(Cube):
    afterImage = copy.deepcopy(Cube)
    de =list(zip(*reversed(list(chunks(Cube[0],3)))))
    table = str.maketrans('()','[]')
    thingy = eval(str(de).translate(table))
    afterImage[0] = list(chain.from_iterable(thingy))
    afterImage[1][0]=Cube[4][0]
    afterImage[1][1]=Cube[4][1]
    afterImage[1][2]=Cube[4][2]
    afterImage[2][0]=Cube[1][0]
    afterImage[2][1]=Cube[1][1]
    afterImage[2][2]=Cube[1][2]
    afterImage[3][0]=Cube[2][0]
    afterImage[3][1]=Cube[2][1]
    afterImage[3][2]=Cube[2][2]
    afterImage[4][0]=Cube[3][0]
    afterImage[4][1]=Cube[3][1]
    afterImage[4][2]=Cube[3][2]
    return afterImage
def leftUp(Cube):
    afterImage = copy.deepcopy(Cube)
    de =list(zip(*(list(chunks(Cube[4],3)))))[::-1]
    table = str.maketrans('()','[]')
    thingy = eval(str(de).translate(table))
    afterImage[4] = list(chain.from_iterable(thingy))
    afterImage[0][0]=Cube[1][0]
    afterImage[0][3]=Cube[1][3]
    afterImage[0][6]=Cube[1][6]
    afterImage[1][0]=Cube[5][0]
    afterImage[1][3]=Cube[5][3]
    afterImage[1][6]=Cube[5][6]
    afterImage[3][2]=Cube[0][6]
    afterImage[3][5]=Cube[0][3]
    afterImage[3][8]=Cube[0][0]
    afterImage[5][0]=Cube[3][8]
    afterImage[5][3]=Cube[3][5]
    afterImage[5][6]=Cube[3][2]
    return afterImage
def leftDown(Cube):
    afterImage = copy.deepcopy(Cube)
    de =list(zip(*reversed(list(chunks(Cube[4],3)))))
    table = str.maketrans('()','[]')
    thingy = eval(str(de).translate(table))
    afterImage[4] = list(chain.from_iterable(thingy))
    afterImage[1][0]=Cube[0][0]
    afterImage[1][3]=Cube[0][3]
    afterImage[1][6]=Cube[0][6]
    afterImage[5][0]=Cube[1][0]
    afterImage[5][3]=Cube[1][3]
    afterImage[5][6]=Cube[1][6]
    afterImage[0][6]=Cube[3][2]
    afterImage[0][3]=Cube[3][5]
    afterImage[0][0]=Cube[3][8]
    afterImage[3][8]=Cube[5][0]
    afterImage[3][5]=Cube[5][3]
    afterImage[3][2]=Cube[5][6]
    return afterImage
def downRight(Cube):
    afterImage = copy.deepcopy(Cube)
    de =list(zip(*reversed(list(chunks(Cube[5],3)))))
    table = str.maketrans('()','[]')
    thingy = eval(str(de).translate(table))
    afterImage[5] = list(chain.from_iterable(thingy))
    afterImage[1][6]=Cube[4][6]
    afterImage[1][7]=Cube[4][7]
    afterImage[1][8]=Cube[4][8]
    afterImage[2][6]=Cube[1][6]
    afterImage[2][7]=Cube[1][7]
    afterImage[2][8]=Cube[1][8]
    afterImage[3][6]=Cube[2][6]
    afterImage[3][7]=Cube[2][7]
    afterImage[3][8]=Cube[2][8]
    afterImage[4][6]=Cube[3][6]
    afterImage[4][7]=Cube[3][7]
    afterImage[4][8]=Cube[3][8]
    return afterImage

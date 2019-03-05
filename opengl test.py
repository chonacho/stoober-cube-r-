import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import math

import copy
import string

from itertools import chain, product, permutations

from numpy import array, matrix, matmul,dot,resize,asanyarray,append,vsplit,concatenate,flip,absolute,arange,transpose, asarray


def rot90(m, k=1, axes=(0, 1)):
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
        return transpose(flip(m, axes[1]), axes_list)
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
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [2, 2, 2, 2, 2, 2, 2, 2, 2],
    [3, 3, 3, 3, 3, 3, 3, 3, 3],
    [4, 4, 4, 4, 4, 4, 4, 4, 4],
    [5, 5, 5, 5, 5, 5, 5, 5, 5]
])
testCube = array(
    [[1, 2, 3, 4, 5, 6, 7, 8, 9], [10, 11, 12, 13, 14, 15, 16, 17, 18], [19, 20, 21, 22, 23, 24, 25, 26, 27],
     [28, 29, 30, 31, 32, 33, 34, 35, 36], [37, 38, 39, 40, 41, 42, 43, 44, 45], [46, 47, 48, 49, 50, 51, 52, 53, 54]])


# now time to math bash to find a matrix for a rotation
# right up affects some layers
def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i + n]


def rightUp(Cube):
    afterImage = resize(copy.deepcopy(Cube), (6, 3, 3))
    de = rot90(afterImage[2], -1)
    afterImage[2] = (de)
    A = array(afterImage[0])
    B = array(afterImage[1])
    C = array(afterImage[3])
    D = array(afterImage[5])
    A1 = dot(A, [[0], [0], [1]])
    B1 = dot(B, [[0], [0], [1]])
    C1 = dot(C, [[1], [0], [0]])
    D1 = dot(D, [[0], [0], [1]])
    afterImage[0] = append(A[:, [0, 1]], B1, 1)
    afterImage[1] = append(B[:, [0, 1]], D1, 1)
    afterImage[3] = append(flip(A1, 0), C[:, [1, 2]], 1)
    afterImage[5] = append(D[:, [0, 1]], flip(C1, 0), 1)
    return resize(afterImage, (6, 9))


def rightDown(Cube):
    afterImage = resize(copy.deepcopy(Cube), (6, 3, 3))
    de = rot90(afterImage[2], 1)
    afterImage[2] = (de)
    A = array(afterImage[0])
    B = array(afterImage[1])
    C = array(afterImage[3])
    D = array(afterImage[5])
    A1 = dot(A, [[0], [0], [1]])
    B1 = dot(B, [[0], [0], [1]])
    C1 = dot(C, [[1], [0], [0]])
    D1 = dot(D, [[0], [0], [1]])
    afterImage[0] = append(A[:, [0, 1]], flip(C1, 0), 1)
    afterImage[1] = append(B[:, [0, 1]], A1, 1)
    afterImage[3] = append(flip(D1, 0), C[:, [1, 2]], 1)
    afterImage[5] = append(D[:, [0, 1]], B1, 1)
    return resize(afterImage, (6, 9))


def upLeft(Cube):
    afterImage = resize(copy.deepcopy(Cube), (6, 3, 3))
    de = rot90(afterImage[0], -1)
    afterImage[0] = (de)
    A = array(afterImage[1])
    B = array(afterImage[2])
    C = array(afterImage[3])
    D = array(afterImage[4])
    A1 = resize(A, (1, 3))
    B1 = resize(B, (1, 3))
    C1 = resize(C, (1, 3))
    D1 = resize(D, (1, 3))
    afterImage[1] = concatenate((B1, A[[1, 2]]), axis=0)
    afterImage[2] = concatenate((C1, B[[1, 2]]), axis=0)
    afterImage[3] = concatenate((D1, C[[1, 2]]), axis=0)
    afterImage[4] = concatenate((A1, D[[1, 2]]), axis=0)
    return resize(afterImage, (6, 9))


def upRight(Cube):
    afterImage = resize(copy.deepcopy(Cube), (6, 3, 3))
    de = rot90(afterImage[0], 1)
    afterImage[0] = (de)
    A = array(afterImage[1])
    B = array(afterImage[2])
    C = array(afterImage[3])
    D = array(afterImage[4])
    A1 = resize(A, (1, 3))
    B1 = resize(B, (1, 3))
    C1 = resize(C, (1, 3))
    D1 = resize(D, (1, 3))
    afterImage[1] = concatenate((D1, A[[1, 2]]), axis=0)
    afterImage[2] = concatenate((A1, B[[1, 2]]), axis=0)
    afterImage[3] = concatenate((B1, C[[1, 2]]), axis=0)
    afterImage[4] = concatenate((C1, D[[1, 2]]), axis=0)
    return resize(afterImage, (6, 9))


def leftUp(Cube):
    afterImage = resize(copy.deepcopy(Cube), (6, 3, 3))
    de = rot90(afterImage[4], 1)
    afterImage[4] = (de)
    A = array(afterImage[0])
    B = array(afterImage[1])
    C = array(afterImage[3])
    D = array(afterImage[5])
    A1 = dot(A, [[1], [0], [0]])
    B1 = dot(B, [[1], [0], [0]])
    C1 = dot(C, [[0], [0], [1]])
    D1 = dot(D, [[1], [0], [0]])
    afterImage[0] = append(B1, A[:, [1, 2]], 1)
    afterImage[1] = append(D1, B[:, [1, 2]], 1)
    afterImage[3] = append(C[:, [0, 1]], flip(A1, 0), 1)
    afterImage[5] = append(flip(C1, 0), D[:, [1, 2]], 1)
    return resize(afterImage, (6, 9))


def leftDown(Cube):
    afterImage = resize(copy.deepcopy(Cube), (6, 3, 3))
    de = rot90(afterImage[4], -1)
    afterImage[4] = (de)
    A = array(afterImage[0])
    B = array(afterImage[1])
    C = array(afterImage[3])
    D = array(afterImage[5])
    A1 = dot(A, [[1], [0], [0]])
    B1 = dot(B, [[1], [0], [0]])
    C1 = dot(C, [[0], [0], [1]])
    D1 = dot(D, [[1], [0], [0]])
    afterImage[0] = append(flip(C1, 0), A[:, [1, 2]], 1)
    afterImage[1] = append(A1, B[:, [1, 2]], 1)
    afterImage[3] = append(C[:, [0, 1]], flip(D1, 0), 1)
    afterImage[5] = append(B1, D[:, [1, 2]], 1)
    return resize(afterImage, (6, 9))


def downLeft(Cube):
    afterImage = resize(copy.deepcopy(Cube), (6, 3, 3))
    de = rot90(afterImage[5], 1)
    afterImage[5] = (de)
    A = array(afterImage[1])
    B = array(afterImage[2])
    C = array(afterImage[3])
    D = array(afterImage[4])
    A1 = resize(vsplit(A, 1)[0][2], (1, 3))
    B1 = resize(vsplit(B, 1)[0][2], (1, 3))
    C1 = resize(vsplit(C, 1)[0][2], (1, 3))
    D1 = resize(vsplit(D, 1)[0][2], (1, 3))
    afterImage[1] = concatenate((A[[0, 1]], B1), axis=0)
    afterImage[2] = concatenate((B[[0, 1]], C1), axis=0)
    afterImage[3] = concatenate((C[[0, 1]], D1), axis=0)
    afterImage[4] = concatenate((D[[0, 1]], A1), axis=0)
    return resize(afterImage, (6, 9))


def downRight(Cube):
    afterImage = resize(copy.deepcopy(Cube), (6, 3, 3))
    de = rot90(afterImage[5], -1)
    afterImage[5] = (de)
    A = array(afterImage[1])
    B = array(afterImage[2])
    C = array(afterImage[3])
    D = array(afterImage[4])
    A1 = resize(vsplit(A, 1)[0][2], (1, 3))
    B1 = resize(vsplit(B, 1)[0][2], (1, 3))
    C1 = resize(vsplit(C, 1)[0][2], (1, 3))
    D1 = resize(vsplit(D, 1)[0][2], (1, 3))
    afterImage[1] = concatenate((A[[0, 1]], D1), axis=0)
    afterImage[2] = concatenate((B[[0, 1]], A1), axis=0)
    afterImage[3] = concatenate((C[[0, 1]], B1), axis=0)
    afterImage[4] = concatenate((D[[0, 1]], C1), axis=0)
    return resize(afterImage, (6, 9))


def frontClock(Cube):
    afterImage = resize(copy.deepcopy(Cube), (6, 3, 3))
    de = rot90(afterImage[1], -1)
    afterImage[1] = (de)
    A = array(afterImage[0])
    B = array(afterImage[2])
    C = array(afterImage[5])
    D = array(afterImage[4])
    A1 = resize(vsplit(A, 1)[0][2], (3, 1))
    B1 = resize(dot(B, [[1], [0], [0]]), (1, 3))
    C1 = resize(vsplit(C, 1)[0][0], (3, 1))
    D1 = resize(dot(D, [[0], [0], [1]]), (1, 3))
    afterImage[0] = concatenate((A[[0, 1]], flip(D1, 1)), axis=0)
    afterImage[2] = append(A1, B[:, [1, 2]], 1)
    afterImage[5] = concatenate((flip(B1, 1), C[[1, 2]]), axis=0)
    afterImage[4] = append(D[:, [0, 1]], flip(C1, 1), 1)
    return resize(afterImage, (6, 9))


def frontCounter(Cube):
    afterImage = resize(copy.deepcopy(Cube), (6, 3, 3))
    de = rot90(afterImage[1], 1)
    afterImage[1] = (de)
    A = array(afterImage[0])
    B = array(afterImage[2])
    C = array(afterImage[5])
    D = array(afterImage[4])
    A1 = resize(vsplit(A, 1)[0][2], (3, 1))
    B1 = resize(dot(B, [[1], [0], [0]]), (1, 3))
    C1 = resize(vsplit(C, 1)[0][0], (3, 1))
    D1 = resize(dot(D, [[0], [0], [1]]), (1, 3))
    afterImage[0] = concatenate((A[[0, 1]], B1), axis=0)
    afterImage[2] = append(flip(C1, 0), B[:, [1, 2]], 1)
    afterImage[5] = concatenate((D1, C[[1, 2]]), axis=0)
    afterImage[4] = append(D[:, [0, 1]], flip(A1, 0), 1)
    return resize(afterImage, (6, 9))


def backClock(Cube):
    afterImage = resize(copy.deepcopy(Cube), (6, 3, 3))
    de = rot90(afterImage[3], 1)
    afterImage[3] = (de)
    A = array(afterImage[0])
    B = array(afterImage[2])
    C = array(afterImage[5])
    D = array(afterImage[4])
    A1 = resize(vsplit(A, 1)[0][0], (3, 1))
    B1 = resize(dot(B, [[0], [0], [1]]), (1, 3))
    C1 = resize(vsplit(C, 1)[0][2], (3, 1))
    D1 = resize(dot(D, [[1], [0], [0]]), (1, 3))
    print(D1)
    afterImage[0] = concatenate((flip(D1, 1), A[[1, 2]]), axis=0)
    afterImage[2] = append(B[:, [0, 1]], A1, 1)
    afterImage[5] = concatenate((C[[0, 1]], flip(B1, 1)), axis=0)
    afterImage[4] = append(flip(C1, 1), D[:, [1, 2]], 1)
    return resize(afterImage, (6, 9))


def backCounter(Cube):
    afterImage = resize(copy.deepcopy(Cube), (6, 3, 3))
    de = rot90(afterImage[3], -1)
    afterImage[3] = (de)
    A = array(afterImage[0])
    B = array(afterImage[2])
    C = array(afterImage[5])
    D = array(afterImage[4])
    A1 = resize(vsplit(A, 1)[0][0], (3, 1))
    B1 = resize(dot(B, [[0], [0], [1]]), (1, 3))
    C1 = resize(vsplit(C, 1)[0][2], (3, 1))
    D1 = resize(dot(D, [[1], [0], [0]]), (1, 3))
    print(D1)
    afterImage[0] = concatenate((B1, A[[1, 2]]), axis=0)
    afterImage[2] = append(B[:, [0, 1]], flip(C1, 0), 1)
    afterImage[5] = concatenate((C[[0, 1]], D1), axis=0)
    afterImage[4] = append(flip(A1, 0), D[:, [1, 2]], 1)
    return resize(afterImage, (6, 9))


def rotation_matrix(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta degrees.
    """
    theta = theta * math.pi/180
    axis = asarray(axis)
    axis = axis / math.sqrt(dot(axis, axis))
    a = math.cos(theta / 2.0)
    b, c, d = -axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])


def rotate_vector(vector, axis, theta):
    """
    Rotates vector about axis by theta degrees
    """
    return dot(rotation_matrix(axis, theta), vector)


def generate_corners_sticker(center):
    """
    generates list of corner coordinates of a sticker given the center's coordinates
    generates in clockwise order
    """
    coordinates = []
    for i in [[-0.5, 0.5], [0.5, 0.5], [0.5, -0.5], [-0.5, -0.5]]:
        coordinates.append([center[0] + i[0], center[1] + i[1]])
    return coordinates


def drawEdges():
    """
    This function draws all the edges of the pieces.
    """
    glLineWidth(5)
    glBegin(GL_LINES)
    glColor3ub(0, 0, 0)
    for i in range(2):
        for x in range(2):
            for a, b in zip(permutations([3.01*(i-0.5), (x-0.5), -1.5]), permutations([3.01*(i-0.5), (x-0.5), 1.5])):
                glVertex3f(*a)
                glVertex3f(*b)
    glEnd()
    pass


def drawCube(cubeState):
    """
    cubeState is in the form
    Cube = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [2, 2, 2, 2, 2, 2, 2, 2, 2],
    [3, 3, 3, 3, 3, 3, 3, 3, 3],
    [4, 4, 4, 4, 4, 4, 4, 4, 4],
    [5, 5, 5, 5, 5, 5, 5, 5, 5]
    ]
    where each sublist is a face of the cube.
    """
    for face, faceList in enumerate(cubeState):
        for position, color in enumerate(faceList):
            draw_piece(face, position, colors[color])
    drawEdges()
    """
    for i in range(len(tempColors)):
        draw_piece(5, i, tempColors[i])
        draw_piece(4, i, tempColors[i])
        draw_piece(3, i, tempColors[i])
        draw_piece(2, i, tempColors[i])
        draw_piece(1, i, tempColors[i])
        draw_piece(0, i, tempColors[i])
    """


def draw_piece(face, position, color):
    """
    Face is a number from 0-5 inclusive, corresponds to sublist of Cube
    position is a number from 0-8 inclusive, corresponds to element of sublist of Cube
    color is a number from  0-5 inclusive
    """

    glBegin(GL_QUADS)
    glColor3ub(*color)
    for x, y, z in faces[face][position]:
        glVertex3f(x-1.5, y-1.5, z-1.5)
    glEnd()


def main():
    global colors  # constant
    global faces
    # global tempColors
    Cube = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [2, 2, 2, 2, 2, 2, 2, 2, 2],
        [3, 3, 3, 3, 3, 3, 3, 3, 3],
        [4, 4, 4, 4, 4, 4, 4, 4, 4],
        [5, 5, 5, 5, 5, 5, 5, 5, 5]
    ]
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glEnable(GL_DEPTH_TEST)

    colors = [[255, 255, 0], [255, 0, 0], [0, 128, 0], [255, 165, 0], [0, 0, 255], [255, 255, 255],
                  [0, 0, 0], [165, 42, 42]]
    # tempColors = [[255, 0, 0], [255, 165, 0], [255, 255, 0], [0, 128, 0], [0, 0, 255], [128, 0, 128], [255, 255, 255],
    #             [0, 0, 0], [165, 42, 42]]

    center_position_within_face = [list(map(lambda x: x + 0.5, a[::-1])) for a in
                                   product([2, 1, 0], [0, 1, 2])]
    # the one-liner above is responsible for creating a list representing location of centers of individual stickers
    # within each face
    faces = [[], [], [], [], [], []]
    horizantal_stickers = list(map(generate_corners_sticker, center_position_within_face))
    for i in horizantal_stickers:
        currentList0 = []
        currentList1 = []
        currentList2 = []
        currentList3 = []
        currentList4 = []
        currentList5 = []

        for x in i:
            # Remember to flip self.faces[0], self.faces[2], self.faces[3]
            currentList0.append([x[0], x[1], 3])
            currentList1.append([x[0], 0, x[1]])
            currentList2.append([3, x[0], x[1]])
            currentList3.append([3-x[0], 3, x[1]])
            currentList4.append([0, 3-x[0], x[1]])
            currentList5.append([x[0], 3-x[1], 0])
        faces[0].append(currentList0)
        faces[1].append(currentList1)
        faces[2].append(currentList2)
        faces[3].append(currentList3)
        faces[4].append(currentList4)
        faces[5].append(currentList5)
    print(center_position_within_face)

    coordinates = []

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0,0.0, -5)
    percievedZAxis = [0, 0, 1]
    percievedXAxis = [1, 0, 0]
    percievedYAxis = [0, 1, 0]

    while True:
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            glRotatef(-1, *percievedYAxis)
            percievedXAxis = rotate_vector(percievedXAxis, percievedYAxis, 1)
            percievedZAxis = rotate_vector(percievedZAxis, percievedYAxis, 1)
        if keys[K_RIGHT]:
            glRotatef(1, *percievedYAxis)
            percievedXAxis = rotate_vector(percievedXAxis, percievedYAxis, -1)
            percievedZAxis = rotate_vector(percievedZAxis, percievedYAxis, -1)
        if keys[K_UP]:
            glRotatef(-1, *percievedXAxis)
            percievedYAxis = rotate_vector(percievedYAxis, percievedXAxis, 1)
            percievedZAxis = rotate_vector(percievedZAxis, percievedXAxis, 1)
        if keys[K_DOWN]:
            glRotatef(1, *percievedXAxis)
            percievedYAxis = rotate_vector(percievedYAxis, percievedXAxis, -1)
            percievedZAxis = rotate_vector(percievedZAxis, percievedXAxis, -1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_w:
                    Cube = upLeft(Cube)
                if event.key == K_a:
                    Cube = leftUp(Cube)
                if event.key == K_s:
                    Cube = downLeft(Cube)
                if event.key == K_d:
                    Cube = rightUp(Cube)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        drawCube(Cube)
        pygame.display.flip()
        pygame.time.wait(10)


main()



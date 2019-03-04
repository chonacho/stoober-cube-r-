import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import math

import copy
import string

from itertools import chain, product, permutations

from numpy import array, matrix, matmul,dot,resize,asanyarray,append,vsplit,concatenate,flip,absolute,arange,transpose, asarray


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

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        drawCube(Cube)
        pygame.display.flip()
        pygame.time.wait(10)


main()



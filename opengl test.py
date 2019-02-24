import pygame
from pygame.locals import *

import itertools

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np
import math


def rotation_matrix(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta degrees.
    """
    theta = theta * math.pi/180
    axis = np.asarray(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(theta / 2.0)
    b, c, d = -axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])


def rotate_vector(vector, axis, theta):
    """
    Rotates vector about axis by theta degrees
    """
    return np.dot(rotation_matrix(axis, theta), vector)


def generate_corners_sticker(center):
    """
    generates list of corner coordinates of a sticker given the center's coordinates
    generates in clockwise order
    """
    coordinates = []
    for i in [[-0.5, 0.5], [0.5, 0.5], [0.5, -0.5], [-0.5, -0.5]]:
        coordinates.append([center[0] + i[0], center[1] + i[1]])
    return coordinates


def Cube():
    for i in range(len(tempColors)):
        draw_piece(5, i, tempColors[i])
        draw_piece(0, i, tempColors[i])


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
    global tempColors
    global faces
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_MULTISAMPLE)
    tempColors = [[255, 0, 0], [255, 165, 0], [255, 255, 0], [0, 128, 0], [0, 0, 255], [128, 0, 128], [255, 255, 255],
                  [0, 0, 0], [165, 42, 42]]

    center_position_within_face = [list(map(lambda x: x + 0.5, a[::-1])) for a in
                                   itertools.product([2, 1, 0], [0, 1, 2])]
    # the one-liner above is responsible for creating a list representing location of centers of individual stickers
    # within each face
    faces = [[], [], [], [], [], []]
    horizantal_stickers = list(map(generate_corners_sticker, center_position_within_face))
    for i in horizantal_stickers:
        currentList0 = []
        currentList5 = []
        for x in i:
            # Remember to flip self.faces[0]
            currentList0.append([x[0], 3 - x[1], 3])
            currentList5.append([x[0], x[1], 0])
        faces[0].append(currentList0)
        faces[5].append(currentList5)

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
        Cube()
        pygame.display.flip()
        pygame.time.wait(10)


main()



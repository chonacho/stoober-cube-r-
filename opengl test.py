from pyglet.gl import *
from pyglet.window import key
import itertools

WINDOW = 400
INCREMENT = 5


class Window(pyglet.window.Window):
    # Cube 3D start rotation
    xRotation = yRotation = 30

    def __init__(self, width, height, cube, title=''):
        super(Window, self).__init__(width, height, title)
        glClearColor(0, 0, 0, 1)
        glEnable(GL_DEPTH_TEST)
        self.cube = cube

        self.center_position_within_face = [list(map(lambda x: x+0.5, a[::-1])) for a in itertools.product([2, 1, 0], [0, 1, 2])]
        # the one-liner above is responsible for creating a list representing location of centers of individual stickers
        # within each face
        self.faces = [[], [], [], [], [], []]
        self.horizantal_stickers = list(map(self.generate_corners_sticker, self.center_position_within_face))
        for i in self.horizantal_stickers:
            currentList0 = []
            currentList5 = []
            for x in i:
                currentList0.append([x[0], x[1], 3])
                currentList5.append([x[0], x[1], 0])
            self.faces[0].append(currentList0)
            self.faces[5].append(currentList5)

    def draw_piece(self, face, position, color):
        """
        Face is a number from 0-5 inclusive, corresponds to sublist of Cube
        position is a number from 0-8 inclusive, corresponds to element of sublist of Cube
        color is a number from  0-5 inclusive
        """
        glPushMatrix()
        glRotatef(self.xRotation, 1, 0, 0)
        glRotatef(self.yRotation, 0, 1, 0)
        glBegin(GL_QUADS)
        glColor3ub(*color)
        for x, y, z in self.faces[face][position]:
            glVertex3f(x*50, y*50, z*50)
        glEnd()
        glPopMatrix()

    def on_draw(self):
        # Clear the current GL Window
        self.clear()

        # Push Matrix onto stack
        glPushMatrix()

        glRotatef(self.xRotation, 1, 0, 0)
        glRotatef(self.yRotation, 0, 1, 0)
        self.draw_piece(5, 0, [255, 255, 255])
        self.draw_piece(5, 5, [255, 0, 255])
        self.draw_piece(5, 7, [0, 255, 255])
        # Pop Matrix off stack
        glPopMatrix()

    def on_resize(self, width, height):
        # set the Viewport
        glViewport(0, 0, width, height)

        # using Projection mode
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        aspectRatio = width / height
        gluPerspective(35, aspectRatio, 1, 1000)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0, 0, -400)

    def on_text_motion(self, motion):
        if motion == key.UP:
            self.xRotation -= INCREMENT
        elif motion == key.DOWN:
            self.xRotation += INCREMENT
        elif motion == key.LEFT:
            self.yRotation -= INCREMENT
        elif motion == key.RIGHT:
            self.yRotation += INCREMENT

    @staticmethod
    def generate_corners_sticker(center):
        """
        generates list of corner coordinates of a sticker given the center's coordinates
        generates in clockwise order
        """
        coordinates = []
        for i in [[-0.5, 0.5], [0.5, 0.5], [0.5, -0.5], [-0.5, -0.5]]:
            coordinates.append([center[0]+i[0], center[1]+i[1]])
        return coordinates


if __name__ == '__main__':
    Window(WINDOW, WINDOW, 'Pyglet Colored Cube')
    pyglet.app.run()
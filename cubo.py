'''
Created on 11/05/2015

@author: philippeoz
'''

import OpenGL
from OpenGL.GLUT import *
from OpenGL.GL import *
from sys import argv
from random import uniform
from OpenGL.raw.GLU import gluPerspective, gluLookAt

coord = [
    1.0, 1.0, 1.0,
    1.0, -1.0, 1.0,
    -1.0, -1.0, 1.0,
    -1.0, 1.0, 1.0,

    1.0, 1.0, -1.0,
    1.0, -1.0, -1.0,
    -1.0, -1.0, -1.0,
    -1.0, 1.0, -1.0,

    0.3, 1.0, 1.0,
    1.0, 0.3, 1.0, 
    1.0, 1.0, 0.3  
]

frente = [3, 2, 1, 9, 8]    
esquerda = [7, 6, 2, 3]     
tras = [4, 5, 6, 7]        
direita = [1, 5, 4, 10, 9] 
topo = [10, 4, 7, 3, 8]    
fundo = [1, 2, 6, 5]       
canto = [8, 9, 10]       

ww=0
wh=0

last = True
rotx = 0
roty = 0
rotz = 0

lf = [ 0, 0, 15]
la = [ 0, 0, 0]
lv = [ 0, 1, 0]

class Cubo():
    def __init__(self, size):
        self.size = size
    
    def draw(self):
        glPushMatrix();
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_DOUBLE, 0, coord)
        glScaled(self.size / 2, self.size / 2, self.size / 2)
        glColor3ub(0xC0, 0x20, 0x40) 
        glDrawElements(GL_POLYGON, 5, GL_UNSIGNED_BYTE, frente)
        glColor3ub(0x00, 0xFF, 0x00) 
        glDrawElements(GL_POLYGON, 4, GL_UNSIGNED_BYTE, esquerda)
        glColor3ub(0x00, 0x00, 0xFF) 
        glDrawElements(GL_POLYGON, 4, GL_UNSIGNED_BYTE, tras)
        glColor3ub(0xFF, 0x00, 0xFF) 
        glDrawElements(GL_POLYGON, 5, GL_UNSIGNED_BYTE, direita)
        glColor3ub(0xFF, 0xFF, 0x00) 
        glDrawElements(GL_POLYGON, 5, GL_UNSIGNED_BYTE, topo)
        glColor3ub(0xFF, 0x88, 0x44) 
        glDrawElements(GL_POLYGON, 4, GL_UNSIGNED_BYTE, fundo)
        glColor3ub(0x88, 0x88, 0x88)
        glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_BYTE, canto)
        glDisableClientState (GL_VERTEX_ARRAY)
        glPopMatrix()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    glRotated(GLdouble(rotx), 1, 0, 0)
    glRotated(GLdouble(roty), 0, 1, 0)
    glRotated(GLdouble(rotz), 0, 0, 1)
    glPushMatrix()
    glBegin(GL_LINES)
    glColor3ub(0xFF, 0x00, 0x00)
    glVertex3d(0, 0, 0)
    glVertex3d(5, 0, 0)
    glEnd()
    glBegin(GL_LINES)
    glColor3ub(0x00, 0xFF, 0x00)
    glVertex3d(0, 0, 0)
    glVertex3d(0, 5, 0)
    glEnd()
    glBegin(GL_LINES)
    glColor3ub(0x00, 0x00, 0xFF)
    glVertex3d(0, 0, 0)
    glVertex3d(0, 0, 5)
    glEnd()
    glPopMatrix()
    Cubo(5).draw()
    glPopMatrix()
    glutSwapBuffers()

def confVisual(perspectiva):
    global last, ww, wh
    last = perspectiva
    d = 20

    glMatrixMode(GL_PROJECTION)
    glColor3ub(0xFF, 0xFF, 0x00) # topo 
    glDrawElements(GL_POLYGON, 5, GL_UNSIGNED_BYTE, topo)

    glColor3ub(0xFF, 0x88, 0x44) # fundo
    glLoadIdentity()

    if perspectiva: 
        f = float(ww) / float(wh)
        gluPerspective(60, f, 10, -1000)
    else:
        if ww >= wh:
            f = float(ww) / float(wh)
            glOrtho(-d * f, d * f, -d, d, -21, 100)
        else:
            f = float(wh) / float(ww)
            glOrtho(-d, d, -d * f, d * f, -21, 100)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(lf[0], lf[1], lf[2],
              la[0], la[1], la[2],
              lv[0], lv[1], lv[2])


def reshape(width, height):
    global last, ww, wh
    if height == 0:
        height = 1
    if width == 0:
        width = 1
    glViewport( 0, 0, width, height)
    ww = width
    wh = height
    confVisual(last)



def keyboard(key, x, y):
    global rotx, roty, rotz, lv, lf, last, la
    if key == '\033':
        exit()
    elif key == 'p':
        confVisual(True)
        print "perspectiva"
    elif key == 'o':
        print "ortogonal"
        confVisual(False)
    elif key == 'x':
        rotx = (rotx + 5) % 360
    elif key == 'X':
        rotx = (rotx + 355) % 360
    elif key == 'y':
        roty = (roty + 5) % 360
    elif key == 'Y':
        roty = (roty + 355) % 360
    elif key == 'z':
        rotz = (rotz + 5) % 360
    elif key == 'Z':
        rotz = (rotz + 355) % 360
    elif key == 't':
        lf[0] = 0
        lf[1] = 15
        lf[2] = 0
        lv[0] = 0
        lv[1] =  0
        lv[2] = -1
        confVisual(last)
        rotx = 0
        roty = 0
        rotz = 0
    elif key == 'f':
        lf[0] = 0
        lf[1] = -15
        lf[2] = 0
        lv[0] = 0
        lv[1] =  0
        lv[2] = -1
        confVisual(last)
        rotx = 0
        roty = 0
        rotz = 0
    elif key == 'F':
        lf[0] = 0
        lf[1] = 0
        lf[2] = 15
        lv[0] = 0
        lv[1] = 1
        lv[2] = 0
        confVisual(last)
        rotx = 0
        roty = 0
        rotz = 0
    elif key == 'T':
        lf[0] = 0
        lf[1] = 0
        lf[2] = -15
        lv[0] = 0
        lv[1] = 1
        lv[2] =   0
        confVisual(last)
        rotx = 0
        roty = 0
        rotz = 0
    elif key == 'd':
        lf[0] = 15
        lf[1] = 0
        lf[2] = 0
        lv[0] =  0
        lv[1] = 1
        lv[2] = 0
        confVisual(last)
        rotx = 0
        roty = 0
        rotz = 0
    elif key == 'e':
        lf[0] = -15
        lf[1] = 0
        lf[2] = 0
        lv[0] = 0
        lv[1] = 1
        lv[2] = 0
        confVisual(last)
        rotx = 0
        roty = 0
        rotz = 0
    elif key == 'c':
        lf[0] = 15
        lf[1] = 15
        lf[2] = 15
        lv[0] =  0
        lv[1] =  1
        lv[2] =  0
        confVisual(last)
        rotx = 0
        roty = 0
        rotz = 0
    glutPostRedisplay()

if __name__ == '__main__':
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    w = 800
    h = 600
    x_pos = (glutGet(GLUT_SCREEN_WIDTH) - w) / 2
    y_pos = (glutGet(GLUT_SCREEN_HEIGHT) - h) / 2
    glutInitWindowPosition(x_pos, y_pos)
    glutInitWindowSize(w, h)
    glutCreateWindow("Francisco Philippe - Cubo_2")
    glClearColor( 0.0, 0.0, 0.0, 0.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutMainLoop()
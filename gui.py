import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from stlParser import parseTriangles

# verticies = (
#     (1, -1, -1),
#     (1, 1, -1),
#     (-1, 1, -1),
#     (-1, -1, -1),
#     (1, -1, 1),
#     (1, 1, 1),
#     (-1, -1, 1),
#     (-1, 1, 1)
#     )
#
# edges = (
#     (0,1),
#     (0,3),
#     (0,4),
#     (2,1),
#     (2,3),
#     (2,7),
#     (6,3),
#     (6,4),
#     (6,7),
#     (5,1),
#     (5,4),
#     (5,7)
#     )
#
# colors = (
#     (1,0,0),
#     (0,1,0),
#     (0,0,1),
#     (0,1,0),
#     (1,1,1),
#     (0,1,1),
#     (1,0,0),
#     (0,1,0),
#     (0,0,1),
#     (1,0,0),
#     (1,1,1),
#     (0,1,1),
#     )
#
# surfaces = (
#     (0,1,2,3),
#     (3,2,7,6),
#     (6,7,5,4),
#     (4,5,1,0),
#     (1,5,7,2),
#     (4,0,3,6)
#     )
#
#
# def Cube():
#     glBegin(GL_QUADS)
#     for surface in surfaces:
#         x = 0
#         for vertex in surface:
#             x+=1
#             glColor3fv(colors[x])
#             glVertex3fv(verticies[vertex])
#     glEnd()
#
#     glBegin(GL_LINES)
#     for edge in edges:
#         for vertex in edge:
#             glVertex3fv(verticies[vertex])
#     glEnd()

def STLImage(triangles):
    glBegin(GL_TRIANGLES)
    glColor3fv((0.6, 0.3, 0.0)) #medium grey = 0.5, 0.5, 0.5
    #print(len(triangles))
    for t in triangles:
        glVertex3fv(t)
    glEnd()

    glBegin(GL_LINE_STRIP)
    glColor3fv((0.7, 0.4, 0.1)) #light grey = 0.6, 0.6, 0.6
    for t in triangles:
        glVertex3fv(t)
    glEnd()


def main(inputFileName=r"examples\surface-mount-hinge-1.snapshot.9\1798A210_SURFACE-MOUNT HINGE.stl"):
    pygame.init()
    display = (800,600)
    maxLength = 1500000 #largest number of triangles drawn to save on processing time
    simplificationFactor = 1 #only draws every 5th triangle to save on processing power

    triangles, [maxX, maxY, maxZ] = parseTriangles(inputFileName)
    #print len(triangles)
    triangles = triangles[0:maxLength:simplificationFactor]
    xLength = maxX * 1.5
    yLength = maxY * 1.5
    zLength = maxZ * 1.5
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(60, (display[0]/display[1]), 0.1, -10 * max(xLength, yLength, zLength))

    glFrontFace(GL_CW)

    glTranslatef(0.0,0.0, -10 * max(xLength, yLength, zLength))
    glTranslatef(-2.0, 0.4, 0)
    glRotatef(70, -2.5, -0.75, -1.25)
    xRotation = 0
    yRotation = 0
    currentlyMoving = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    xRotation = -xLength
                elif event.key == pygame.K_RIGHT:
                    xRotation = xLength
                if event.key == pygame.K_DOWN:
                    yRotation = -yLength
                elif event.key == pygame.K_UP:
                    yRotation = yLength
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    xRotation = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    yRotation = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glTranslatef(0,0,zLength * 3)
                elif event.button == 5:
                    glTranslatef(0,0,-zLength * 3)
                else:
                    pygame.mouse.get_rel()
                    currentlyMoving = True
            elif event.type == pygame.MOUSEBUTTONUP and currentlyMoving == True:
                translation = pygame.mouse.get_rel()
                glTranslatef(translation[0] * xLength / float(display[0]), -translation[1] * yLength / float(display[1]), 0)
                currentlyMoving = False

        if xRotation != 0 or yRotation != 0:
            glRotatef(5, yRotation, xRotation, 0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        STLImage(triangles)
        pygame.display.flip()
        pygame.time.wait(10)


main()

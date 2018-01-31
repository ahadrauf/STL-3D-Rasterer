import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from stlParser import parseTriangles

def STLImage(triangles):
    glBegin(GL_TRIANGLES)
    glColor3fv((0.6, 0.3, 0.0)) #medium grey = 0.5, 0.5, 0.5
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

    triangles, [maxX, maxY, maxZ] = parseTriangles(inputFileName)
    #the program slows down after about 750,000 triangles, so this code is designed to
    #   keep the number of triangles (maxLength / simplificationFactor) around 500,000
    #   (maxLength gets rounded to the nearest multiple of 500,000, and simplificationFactor
    #   is designed to divide into maxLength to get 500,000)
    maxLength = 500000 * max(round(len(triangles) / 500000), 1) #largest number of triangles drawn to save on processing time
    simplificationFactor = max(int(len(triangles) / 500000), 1) #skips a few triangles to save on processing power
    triangles = triangles[0:maxLength:simplificationFactor]
    xLength = maxX * 1.5
    yLength = maxY * 1.5
    zLength = maxZ * 1.5
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(60, (display[0]/display[1]), 0.1, -2 * max(xLength, yLength, zLength))

    glFrontFace(GL_CW)

    glTranslatef(0.0,0.0, -2 * max(xLength, yLength, zLength))
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

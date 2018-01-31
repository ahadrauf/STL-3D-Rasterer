import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from stlParser import parseTriangles
from math import sqrt

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


def main(inputFileName=r"examples\silla-salon-1.snapshot.1\SILLA SALON_MOD_1.stl"):
    pygame.init()
    display = (800,600)

    triangles, [maxX, maxY, maxZ] = parseTriangles(inputFileName)
    maxDimension = sqrt(maxX*maxX + maxY*maxY + maxZ*maxZ)
    #the program slows down after about 75,000 triangles, so this code is designed to
    #   keep the number of triangles (maxLength / simplificationFactor) around 50,000
    #   (maxLength gets rounded to the nearest multiple of 50,000, and simplificationFactor
    #   is designed to divide into maxLength to get 50,000)
    maxLength = 50000 * max(int(round(len(triangles) / 50000)), 1) #largest number of triangles drawn to save on processing time
    simplificationFactor = max(int(len(triangles) / 50000), 1) #skips a few triangles to save on processing power
    triangles = [(x / maxDimension, y / maxDimension, z / maxDimension) for x, y, z in triangles[0:maxLength:simplificationFactor]] #normalizes size
    xLength = maxX * 1.5
    yLength = maxY * 1.5
    zLength = maxZ * 1.5
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(60, (display[0]/display[1]), 0.1, 50)

    glFrontFace(GL_CW) #Because STL files typically have the CW direction represent the normal vector (using the right hand rule)
    glEnable(GL_CULL_FACE) #Stops faces from being rastered if they're on the inside of the shape

    glTranslatef(0, -0.25, -1.5)
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
                    yRotation = yLength
                elif event.key == pygame.K_UP:
                    yRotation = -yLength
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    xRotation = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    yRotation = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glTranslatef(0,0,0.3)
                elif event.button == 5:
                    glTranslatef(0,0,-0.3)
                else:
                    pygame.mouse.get_rel()
                    currentlyMoving = True
            elif event.type == pygame.MOUSEBUTTONUP and currentlyMoving == True:
                translation = pygame.mouse.get_rel()
                glTranslatef(translation[0] * 10 / float(display[0]), -translation[1] * 10 / float(display[1]), 0)
                currentlyMoving = False

        if xRotation != 0 or yRotation != 0:
            glRotatef(5, yRotation, xRotation, 0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        STLImage(triangles)
        pygame.display.flip()
        pygame.time.wait(10)

main()

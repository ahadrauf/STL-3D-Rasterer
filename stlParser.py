"""
Custom parser for standard binary STL files
"""

#Basic algorithm based on StackOverflow post by DaClown
#https://stackoverflow.com/questions/7566825/python-parsing-binary-stl-file

# Binary STL file structure: (taken from https://en.wikipedia.org/wiki/STL_%28file_format%29)
# UINT8[80] - Header
# UINT32 - Number of triangles
#
# foreach triangle
#   REAL32[3] - Normal vector (usually written as little endian)
#   REAL32[3] - Vertex 1 (usually written as little endian)
#   REAL32[3] - Vertex 2 (usually written as little endian)
#   REAL32[3] - Vertex 3 (usually written as little endian)
#   UINT16 - Attribute byte count (usually 0, just ignore for most applications)
# end

import struct

points = []

def unpack(f, sig, length):
    s = f.read(length)
    return struct.unpack(sig, s)

def read_triangle(f):
    #each normal vector/point is represented by their x, y, and z components
    #   -> 4 bits * 3 variables = 12 bits
    f.seek(f.tell() + 12) #skip over normal vector
    p1 = unpack(f,"<3f", 12)
    p2 = unpack(f,"<3f", 12)
    p3 = unpack(f,"<3f", 12)
    f.seek(f.tell() + 2)

    points.append(p1)
    points.append(p2)
    points.append(p3)

    return max(p1[0], p2[0], p3[0]), max(p1[1], p2[1], p3[1]), max(p1[2], p2[2], p3[2])


def read_length(f):
    length = struct.unpack("@i", f.read(4))
    return length[0]

def read_header(f):
    f.seek(f.tell()+80)

def parseTriangles(infilename):
        try:
            f = open (infilename, "rb")
            maxX = 0; maxY = 0; maxZ = 0; #used to specify STL file size
            read_header(f)
            l = read_length(f)
            try:
                for _ in range(l):
                    [tempX, tempY, tempZ] = read_triangle(f)
                    maxX = max(maxX, tempX)
                    maxY = max(maxY, tempY)
                    maxZ = max(maxZ, tempZ)
            except Exception, e:
                print "Exception",e[0]
            print "Finished parsing STL file"
            return points, [maxX, maxY, maxZ]
        except Exception, e:
            print e

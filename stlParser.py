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

#normals = []
points = []
#triangles = []
#bytecount = []

#fb = [] # debug list

def unpack(f, sig, length):
    s = f.read(length)
    #fb.append(s)
    return struct.unpack(sig, s)

def read_triangle(f):
    #each normal vector/point is represented by their x, y, and z components
    #   -> 4 bits * 3 variables = 12 bits
    #n = unpack(f,"<3f", 12)
    f.seek(f.tell() + 12) #skip over normal vector
    p1 = unpack(f,"<3f", 12)
    p2 = unpack(f,"<3f", 12)
    p3 = unpack(f,"<3f", 12)
    #b = unpack(f,"<h", 2)
    f.seek(f.tell() + 2)

    #normals.append(n)
    #l = len(points)
    points.append(p1)
    points.append(p2)
    points.append(p3)
    #triangles.append((l, l+1, l+2))
    #bytecount.append(b[0])

    return max(p1[0], p2[0], p3[0]), max(p1[1], p2[1], p3[1]), max(p1[2], p2[2], p3[2])


def read_length(f):
    length = struct.unpack("@i", f.read(4))
    return length[0]

def read_header(f):
    f.seek(f.tell()+80)

# def write_as_ascii(outfilename):
#     f = open(outfilename, "w")
#     f.write ("solid "+outfilename+"\n")
#     for n  in range(len(triangles)):
#         f.write ("facet normal {} {} {}\n".format(normals[n][0],normals[n][1],normals[n][2]))
#         f.write ("outer loop\n")
#         f.write ("vertex {} {} {}\n".format(points[triangles[n][0]][0],points[triangles[n][0]][1],points[triangles[n][0]][2]))
#         f.write ("vertex {} {} {}\n".format(points[triangles[n][1]][0],points[triangles[n][1]][1],points[triangles[n][1]][2]))
#         f.write ("vertex {} {} {}\n".format(points[triangles[n][2]][0],points[triangles[n][2]][1],points[triangles[n][2]][2]))
#         f.write ("endloop\n")
#         f.write ("endfacet\n")
#     f.write ("endsolid "+outfilename+"\n")
#     f.close()

# def main():
#     infilename = r"silla-salon-1.snapshot.1\SILLA SALON_MOD_1.stl"
#     outfilename = r"silla-salon-1.snapshot.1\SILLA SALON_MOD_1_ascii.stl"
#
#     try:
#         f = open (infilename, "rb")
#
#         read_header(f)
#         l = read_length(f)
#         try:
#             for _ in range(l):
#                 read_triangle(f)
#         except Exception, e:
#             #print(len(fb), fb[len(fb) - 1])
#             print "Exception",e[0]
#         print len(normals), len(points), len(triangles), l
#         write_as_ascii(outfilename)
#
#     except Exception, e:
#         print e
#
#
# if __name__ == '__main__':
#     main()

def parseTriangles(infilename):
        #infilename = r"silla-salon-1.snapshot.1\SILLA SALON_MOD_1.stl"

        try:
            f = open (infilename, "rb")

            maxX = 0; maxY = 0; maxZ = 0;

            read_header(f)
            l = read_length(f)
            try:
                for _ in range(l):
                    [tempX, tempY, tempZ] = read_triangle(f)
                    maxX = max(maxX, tempX)
                    maxY = max(maxY, tempY)
                    maxZ = max(maxZ, tempZ)
            except Exception, e:
                #print(len(fb), fb[len(fb) - 1])
                print "Exception",e[0]
            #print len(normals), len(points), len(triangles), l
            print "Finished parsing STL file"
            #write_as_ascii(outfilename)
            return points, [maxX, maxY, maxZ]

        except Exception, e:
            print e

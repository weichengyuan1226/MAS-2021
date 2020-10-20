import math
from mysubdivision import taper_face, my_mesh_thicken
from shapes import Sphere
from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist
from compas.datastructures import subdivision as sd
from compas.geometry import angle_vectors

from compas_rhino import unload_modules
unload_modules('shapes')
unload_modules('mysubdivision')


def math_map_list(values, toMin=0, toMax=1):
    """
    Maps the values of a list from a minimum value to a maximum value.
    Arguments:
    ----------
    values : list to be mapped
    Optional Arguments:
    ----------
    toMin : minimum value of the list's target range (default = 0)
    toMax : maximum value of the list's target range (default = 1)
    """
    minValue = min(values)
    maxValue = max(values)
    delta = maxValue - minValue
    deltaTarget = toMax - toMin
    newValues = [toMin +(value-minValue)*deltaTarget/delta for value in values]
    return newValues


sphere = Sphere([0, 0, 0], 5)

vs, fs = sphere.to_vertices_and_faces(u=12, v=12)
sphere_mesh = Mesh.from_vertices_and_faces(vs, fs)


# turn sphere into egg
for key, attr in sphere_mesh.vertices(True):

    if attr['z'] > 0:

        attr['z'] *= 1.8


# smooth egg
sphere_smooth = sd.mesh_subdivide_catmullclark(sphere_mesh, k=1, fixed=None)

# analyse vertical orientation of faces, as difference to vertical orientation
# map values to range

face_normals = []

for key in sphere_smooth.faces():

    face_normals.append( sphere_smooth.face_normal(key, unitized=True) )

face_angles = [angle_vectors(normal,[0,0,1]) for normal in face_normals]

for i in range(len(face_angles)):
    face_angles[i] = abs(face_angles[i] - 0.5*math.pi)

# map list to another range
face_angles = math_map_list(face_angles, 0.3, 1)

# analyse z positions of faces
z_positions = []
for key in sphere_smooth.faces():

    z_positions.append( sphere_smooth.face_center(key)[2])

z_positions = math_map_list(z_positions, 0, 1)

#larger opening the larger z
fractions = math_map_list(z_positions, 0.9, 0.1)

#closed when below 0.2 (=20%)
doCaps = [True] * len(z_positions)

for i in range(len(z_positions)):
    if z_positions[i] > 0.2:
        doCaps[i]=False

#parametric subdivision based on the analyses
#deeper opening when vertical face, large opening when higher, closed on the bottom
fkeys = list(sphere_smooth.faces())
print (len(fkeys))
for f, a, r, c in zip(fkeys, face_angles, fractions, doCaps):
    new_keys = taper_face(sphere_smooth, f, a, r, c)

sphere_tapered = sphere_smooth

# turn into volume by offset
offset_sphere = my_mesh_thicken(sphere_tapered, 0.5)

# smooth egg
sphere_tapered_smooth = sd.mesh_subdivide_catmullclark(offset_sphere, k=1, fixed=None)

artist = MeshArtist(sphere_tapered_smooth , layer="smooth_tapered_sphere")

artist.clear_layer()

artist.draw_faces(color = [0,0.7,0.7], join_faces=True)

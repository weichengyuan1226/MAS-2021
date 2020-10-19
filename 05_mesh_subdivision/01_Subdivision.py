from mysubdivision import mesh_subdivide_pyramid, mesh_subdivide_tapered
from compas.geometry import Circle
from compas.datastructures import meshes_join
from shapes import Sphere, Cylinder, Torus, Cone
from mysubdivision import pyramid_face
from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist
from compas.datastructures import subdivision as sd
from compas.geometry import Translation, Scale
import math

from compas_rhino import unload_modules
unload_modules('mysubdivision')

unload_modules('shapes')

# 2D Subdivision

vertices = [
    [0.5, 0.0, 0.0],
    [0.0, 1.0, 0.0],
    [-0.5, 0.0, 0.0],
    [1.0, 1.0, 0.0]
]

faces = [
        [0, 1, 2],
        [1, 0, 3]
]

my_mesh = Mesh.from_vertices_and_faces(vertices, faces)

artist = MeshArtist(my_mesh, layer="00_my_first mesh")

artist.clear_layer()
artist.draw_vertices()
artist.draw_faces()
artist.draw_edges()
artist.draw_vertexlabels()
artist.draw_facelabels()
artist.draw_edgelabels()

# iterate through the mesh
# for key,attr in my_mesh.vertices(True):
#     print (key, attr['x'], attr['y'], attr['z'])

# for key in my_mesh.faces():
#     print(key)

# for key in my_mesh.edges():
#     print(key)

# get topology information
vertex = 0
#print (my_mesh.vertex_neighbors(vertex , ordered=False))
#print (my_mesh.vertex_degree(vertex))
#print (my_mesh.vertex_faces(vertex, ordered=False))

# get geometry information
face = 0
myVertex = my_mesh.vertex_coordinates(vertex)
myCentroid = my_mesh.face_centroid(face)
myNormal = my_mesh.face_normal(face)

# subdivision schemes available in compas
point = [1.5, 0, 0]
T = Translation.from_vector(point)
mesh = my_mesh.transformed(T)

# Subdivide a mesh using simple insertion of vertices
subd = sd.mesh_subdivide_tri(mesh, 1)
artist2 = MeshArtist(subd, layer="01_subdivide_tri")
artist2.clear_layer()
artist2.draw_vertices()
artist2.draw_faces()
artist2.draw_edges()
artist2.draw_vertexlabels()
artist2.draw_facelabels()
artist2.draw_edgelabels()


# Subdivide a mesh by cutting corners
subd = sd.mesh_subdivide_corner(mesh, 1)
artist3 = MeshArtist(subd, layer="02_subdivide_corners")
artist3.clear_layer()
artist3.draw_vertices()
artist3.draw_faces()
artist3.draw_edges()
artist3.draw_vertexlabels()
artist3.draw_facelabels()
artist3.draw_edgelabels()

# Subdivide a mesh such that all faces are quads
subd = sd.mesh_subdivide_quad(mesh, 1)
artist4 = MeshArtist(subd, layer="03_subdivide_quads")
artist4.clear_layer()
artist4.draw_vertices()
artist4.draw_faces()
artist4.draw_edges()
artist4.draw_vertexlabels()
artist4.draw_facelabels()
artist4.draw_edgelabels()

# Subdivide a mesh using the Catmull-Clark algorithm
subd = sd.mesh_subdivide_catmullclark(mesh, k=1, fixed=None)
artist5 = MeshArtist(subd, layer="04_subdivide_catmull")
artist5.clear_layer()
artist5.draw_vertices()
artist5.draw_faces()
artist5.draw_edges()
artist5.draw_vertexlabels()
artist5.draw_facelabels()
artist5.draw_edgelabels()

# Subdivide a triangle mesh using the Loop algorithm
subd = sd.trimesh_subdivide_loop(mesh, k=1)
artist6 = MeshArtist(subd, layer="05_subdivide_loop")
artist6.clear_layer()
artist6.draw_vertices()
artist6.draw_faces()
artist6.draw_edges()
artist6.draw_vertexlabels()
artist6.draw_facelabels()
artist6.draw_edgelabels()

# Subdivide a mesh following the doo-sabin scheme
subd = sd.mesh_subdivide_doosabin(mesh, k=1, fixed=None)
artist7 = MeshArtist(subd, layer="06_subdivide_doosabin")
artist7.clear_layer()
artist7.draw_vertices()
artist7.draw_faces()
artist7.draw_edges()
artist7.draw_vertexlabels()
artist7.draw_facelabels()
artist7.draw_edgelabels()

# 3d mesh - Custom rules
# n of faces - 4, 6, 8, 12, 20
poly = Mesh.from_polyhedron(8)

S = Scale.from_factors([5, 5, 5])
poly.transform(S)

point = [8, 0.5, 0]
T = Translation.from_vector(point)
poly.transform(T)

mesh2 = sd.mesh_subdivide_tri(poly)
mesh3 = mesh_subdivide_pyramid(mesh2, k=1, height=0.5)
mesh4 = sd.trimesh_subdivide_loop(mesh3)
mesh5 = sd.mesh_subdivide_catmullclark(mesh4)

# subdivide each face of the mesh
centers = []
for key in mesh5.faces():
    centers.append( mesh5.face_centroid(key) )

# map positions to TPMS (Gyroid)
properties = [math.sin(v[0])*math.cos(v[1]) + math.sin(v[1])*math.cos(v[2]) +
              math.sin(v[2])*math.cos(v[2]) for v in centers]

fkeys = list(mesh5.faces())

for f, p in zip(fkeys, properties):
    new_keys = pyramid_face(mesh5, f, p)

# spiky ball

artist9 = MeshArtist(mesh5, layer="07_3d")
artist9.clear_layer()
artist9.draw_mesh()

# 3d mesh - Custom shapes
my_circle = Circle([[0, 0, 0], [0, 0, 1]], 5)
my_cone = Cone(my_circle, 5)
vs, fs = my_cone.to_vertices_and_faces(u=11, v=11)
my_cone_mesh = Mesh.from_vertices_and_faces(vs, fs)

point = [21, 0, 0]
T = Translation.from_vector(point)
my_cone_mesh.transform(T)

artist = MeshArtist(my_cone_mesh, layer="08_cone")
artist.clear_layer()
artist.draw_mesh()
mesh = my_cone_mesh

for i in range(3):
    sd = mesh_subdivide_tapered(mesh, 1, height=2/(i+1), ratio=0.4, doCap=True)
    mesh = sd

artist10 = MeshArtist(sd, layer="09_cone_tapered")
artist10.clear_layer()
artist10.draw_mesh()


# atomium

origin = (0, 0, 0)
normal = (0, 0, 1)
plane = (origin, normal)
r_axis = 3.0
r_pipe = 1.5
torus = Torus(plane, r_axis, r_pipe)

vs, fs = torus.to_vertices_and_faces(u=11, v=11)
torus_mesh = Mesh.from_vertices_and_faces(vs, fs)

vertex_spheres = []
for v in torus_mesh.vertices():
    v_coords = torus_mesh.vertex_coordinates(v)
    sphere = Sphere(v_coords, 0.2)
    vs, fs = sphere.to_vertices_and_faces(u=12, v=12)
    sphere_mesh = Mesh.from_vertices_and_faces(vs, fs)
    vertex_spheres.append(sphere_mesh)

spheres_mesh = meshes_join(vertex_spheres)
torus_and_spheres = meshes_join([spheres_mesh, torus_mesh])

edge_cylinders = []

for e in torus_mesh.edges():

    e_mid = torus_mesh.edge_midpoint(e[0], e[1])
    e_dir = torus_mesh.edge_direction(e[0], e[1])
    e_len = torus_mesh.edge_length(e[0], e[1])
    circle = Circle((e_mid, e_dir), 0.1)
    cylinder = Cylinder(circle, e_len)
    vs, fs = cylinder.to_vertices_and_faces(u=16)
    cyl_mesh = Mesh.from_vertices_and_faces(vs, fs)
    edge_cylinders.append(cyl_mesh)

all_cylinders = meshes_join(edge_cylinders)

atomium = meshes_join([all_cylinders, spheres_mesh])

point = [35, 0.5, 0]
T = Translation.from_vector(point)
atomium.transform(T)

artist10 = MeshArtist(atomium, layer="10 atomium")
artist10.clear_layer()
artist10.draw_mesh()

from mysubdivision import*
from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist
from compas.geometry import Translation
from compas_rhino import unload_modules
unload_modules('mysubdivision')


vertices = [
    [0.5, 0.0, 0.0],
    [0.0, 1.0, 0.0],
    [-0.5, 0.0, 0.0],
    [1.0, 1.0, 0.0],
    [0.5, 2.0, 0.0]
]

faces = [
        [0, 1, 2],
        [1, 0, 3,4]
]

my_mesh = Mesh.from_vertices_and_faces(vertices, faces)

artist = MeshArtist(my_mesh, layer="00_my_base_mesh")
artist.draw_faces( join_faces=True)
artist.draw_vertexlabels()
artist.draw_facelabels()

#for meshes

point = [2.5, 0, 0]
T = Translation.from_vector(point)
my_mesh = my_mesh.transformed(T)

mesh1 = mesh_subdivide_pyramid(my_mesh, k=1, height=0.5)
artist2 = MeshArtist(mesh1, layer="00_my_mesh_pyramid")
artist2.draw_faces( join_faces=True)


mesh2 = mesh_subdivide_tapered(my_mesh, k=1, height=1.0, ratio=0.5, doCap=False )
artist3 = MeshArtist(mesh2, layer="01_my_mesh_tapered")
artist3.draw_faces( join_faces=True)

mesh3 = my_mesh_thicken(my_mesh, 0.5)
artist4 = MeshArtist(mesh3, layer="02_my_mesh_offset")
artist4.draw_faces( join_faces=True)

#for faces

# pyramid_face
mesh4 = my_mesh.copy()
fkeys = list(mesh4.faces())

for f in fkeys[:-1]:
    new_keys = pyramid_face(mesh4, f, height = 0.5)


artist4 = MeshArtist(mesh4, layer="03_my_face_pyramid")
artist4.draw_faces( join_faces=True)


# segment_face

mesh4 = my_mesh.copy()
fkeys = list(mesh4.faces())

for f in fkeys:
    new_keys = segment_face(mesh4, f, num=4, start_index=2)

print new_keys
artist5 = MeshArtist(mesh4, layer="04_my_face_segment")
artist5.draw_faces( join_faces=True)

# taper_face

mesh5 = my_mesh.copy()
fkeys = list(mesh4.faces())

for f in fkeys[:-1]:
    new_keys = taper_face(mesh5, f, height = 0.5)


artist6 = MeshArtist(mesh5, layer="05_my_face_taper")
artist6.draw_faces( join_faces=True)

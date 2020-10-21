from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist
from compas.datastructures import subdivision as sd

from compas_rhino import unload_modules
unload_modules('mysubdivision')
import mysubdivision as msd

import random


# #empty list
# my_list = []
# #empty dictionary
# my_dict = {}

# my_list = ["John"]

# my_dict = { "name" : "John", 1 : [2,4,3]  }

# #get value
# print (my_list[0])

# print (my_dict["name"])
# print (my_dict.get(1))

# #update value
# my_list[0] = "Mary"
# my_dict["name"] = "Mary"
# #create a new key/value
# # not posiible : my_list[1] = "Zurich"
# my_dict["adress"] = "Zurich"

# print my_dict

# # if attr["z"]>0:
# #     attr["z"] *=1.8

def subdivide_by_ftype(mesh):

    fkeys = list(mesh.faces())

    for fk in fkeys:
        ftype = mesh.face_attribute(fk, 'ftype')

        if ftype == 'plot':
            new_keys = msd.taper_face(mesh, fk, height=0, ratio=0.45, doCap=True)

            for key in new_keys[:-1]:
                mesh.face_attribute(key, 'ftype', 'circulation')
            mesh.face_attribute(new_keys[-1], 'ftype', 'construction')

        elif ftype=='construction':
            if random.random()<0.2:
                # make a park
                new_keys = msd.pyramid_face(mesh, fk, height=0.1)
                for key in new_keys:
                    mesh.face_attribute(key, 'ftype', 'park')
            else:
                # make a building
                num = random.randint(5,10)
                temp_fk = fk
                for i in range(num):

                    r = random.random() * 0.6 - 0.3
                    new_keys = msd.taper_face(mesh, temp_fk, height=0.1, ratio=r, doCap = True, keep_original=True)

                    for key in new_keys[:-1]:
                        mesh.face_attribute(key, 'ftype', 'facade')
                    mesh.face_attribute(temp_fk, 'ftype', 'floor')
                    temp_fk = new_keys[-1]
                mesh.face_attribute(temp_fk, 'ftype', 'roof')

        elif ftype=='facade':
            # make a facade
            fvs = mesh.face_vertices(fk)
            facade_length = mesh.edge_length(fvs[0],fvs[1])
            num_subdivisions = int(facade_length/0.05)
            if num_subdivisions>1:
                new_keys = msd.segment_face(mesh, fk, num=num_subdivisions)
                for key in new_keys:
                    mesh.face_attribute(key, 'ftype', 'panel')
            else:
                mesh.face_attribute(fk, 'ftype', 'panel')


mesh = Mesh()
a = mesh.add_vertex(x=0, y=0, z=0)
b = mesh.add_vertex(x=1, y=0, z=0)
c = mesh.add_vertex(x=1, y=1, z=0)
d = mesh.add_vertex(x=0, y=1, z=0)
f = mesh.add_face([a, b, c, d])

mesh = sd.mesh_subdivide_tri(mesh)

mesh = sd.mesh_subdivide_quad(mesh)

fkeys = list(mesh.faces())

for fk in fkeys:

    new_keys = msd.segment_face(mesh, fk, num=2, start_index=0)

    for key in new_keys:
        mesh.face_attribute(key, "ftype", "plot")


# artist = MeshArtist(mesh, layer="level1")
# artist.clear_layer()
# artist.draw_faces( join_faces=True)

m1 = mesh.copy()
subdivide_by_ftype(m1)
# artist2 = MeshArtist(m1, layer="level2")
# artist2.clear_layer()

m1fkeys = list(m1.faces())

#circulation = [key for key in m1fkeys if m1.face_attribute(key, 'ftype')== "circulation"]
#construction = [key for key in m1fkeys if m1.face_attribute(key, 'ftype')== "construction"]

# artist2.draw_faces( circulation, color= (255,0,0), join_faces=True)
# artist2.draw_faces( construction, color= (0,0,255), join_faces=True)

m2 = m1.copy()
subdivide_by_ftype(m2)
# artist3 = MeshArtist(m2, layer="level3")
# artist3.clear_layer()

# m2fkeys = list(m2.faces())

# circulation = [key for key in m2fkeys if m2.face_attribute(key, 'ftype')== "circulation"]
# park = [key for key in m2fkeys if m2.face_attribute(key, 'ftype')== "park"]
# facade = [key for key in m2fkeys if m2.face_attribute(key, 'ftype')== "facade"]
# floor = [key for key in m2fkeys if m2.face_attribute(key, 'ftype')== "floor"]
# roof = [key for key in m2fkeys if m2.face_attribute(key, 'ftype')== "roof"]

# artist3.draw_faces( circulation, color= (255,0,0), join_faces=True)
# artist3.draw_faces( park, color= (0,255,0), join_faces=True)
# artist3.draw_faces( facade, color= (0,255,255), join_faces=True)
# artist3.draw_faces( floor, color= (255,255,0), join_faces=True)
# artist3.draw_faces( roof, color= (160,32,255), join_faces=True)

m3 = m2.copy()
subdivide_by_ftype(m3)
artist4 = MeshArtist(m3, layer="level4")

m3fkeys = list(m3.faces())

circulation = [key for key in m3fkeys if m3.face_attribute(key, 'ftype')== "circulation"]
park = [key for key in m3fkeys if m3.face_attribute(key, 'ftype')== "park"]
floor = [key for key in m3fkeys if m3.face_attribute(key, 'ftype')== "floor"]
roof = [key for key in m3fkeys if m3.face_attribute(key, 'ftype')== "roof"]
panel = [key for key in m3fkeys if m3.face_attribute(key, 'ftype')== "panel"]

artist4.draw_faces( circulation, color= (255,0,0), join_faces=True)
artist4.draw_faces( park, color= (0,255,0), join_faces=True)
artist4.draw_faces( floor, color= (255,255,0), join_faces=True)
artist4.draw_faces( roof, color= (160,32,255), join_faces=True)
artist4.draw_faces( panel, color= (255,160,16), join_faces=True)

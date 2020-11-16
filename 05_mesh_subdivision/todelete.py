from shapes import Polyhedron
from compas_rhino.artists import MeshArtist
from compas.datastructures import Mesh

poly = Mesh.from_polyhedron(12)
print (poly)

artist = MeshArtist(poly, layer='00_my_mesh')

artist.clear_layer()
artist.draw_faces()
artist.draw_mesh(join_faces=True)
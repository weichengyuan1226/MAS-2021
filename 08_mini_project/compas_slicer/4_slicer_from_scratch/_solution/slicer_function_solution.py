from compas.geometry import Point, Plane, Vector, intersection_segment_plane
from compas_slicer.slicers.slice_utilities import create_graph_from_mesh_edges, sort_graph_connected_components
import compas_slicer.utilities as utils
import os
from compas.datastructures import Mesh
from compas.geometry import Polyline
import logging

logger = logging.getLogger('logger')
logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.INFO)



class LevelSlicer(object):

    def __init__(self, mesh, z):
        self.mesh = mesh
        self.z = z

        self.intersected_edges = []  # list of tupples (int, int)
        self.intersection_points = {}  # dict
        # key: tupple (int, int), The edge from which the intersection point originates.
        # value: :class: 'compas.geometry.Point', The zero-crossing point.
        self.edge_point_index_relation = {}  # dict that stores node_index and edge relationship
        # key: tupple (int, int) edge
        # value: int, index of the intersection point
        self.sorted_points = {}  # dict
        # key: int, The index of the connected component
        # value: list, :class: 'compas.geometry.Point', The sorted zero-crossing points.
        self.sorted_edges = {}  # dict
        # key: int, The index of the connected component.
        # value: list, tupple (int, int), The sorted intersected edges.
        self.closed_paths_booleans = {}  # dict
        # key: int, The index of the connected component.
        # value: bool, True if path is closed, False otherwise.

    def edge_is_intersected(self, u, v):
        """ Returns True if the edge u,v has a zero-crossing, False otherwise. """
        a = self.mesh.vertex_attributes(u, 'xyz')
        b = self.mesh.vertex_attributes(v, 'xyz')
        z = [a[2], b[2]]  # check if the plane.z is withing the range of [a.z, b.z]
        return min(z) <= self.z < max(z)

    def find_zero_crossing_point(self, u, v):
        """ Finds the position of the zero-crossing on the edge u,v. """
        a = self.mesh.vertex_attributes(u, 'xyz')
        b = self.mesh.vertex_attributes(v, 'xyz')
        plane = Plane(Point(0, 0, self.z), Vector(0, 0, 1))
        return intersection_segment_plane((a, b), plane)

    def find_intersected_edges(self):
        """ Creates a list of edges that are intersected and the resuling pts"""
        for edge in list(self.mesh.edges()):
            if self.edge_is_intersected(edge[0], edge[1]):
                point = self.find_zero_crossing_point(edge[0], edge[1])
                if point:  # Sometimes the result can be None
                    if edge not in self.intersected_edges and tuple(reversed(edge)) not in self.intersected_edges:
                        self.intersected_edges.append(edge)
                        # create [edge - point] dictionary
                        self.intersection_points[edge] = Point(point[0], point[1], point[2]),

            # create [edge - point] dictionary
            for i, e in enumerate(self.intersection_points):
                self.edge_point_index_relation[e] = i

    def compute(self):
        self.find_intersected_edges()
        G = create_graph_from_mesh_edges(self.mesh, self.intersected_edges,
                                         self.intersection_points,
                                         self.edge_point_index_relation)
        self.sorted_points, self.sorted_edges = sort_graph_connected_components(G, self.intersection_points)
        self.label_closed_paths()

    def label_closed_paths(self):
        for key in self.sorted_edges:
            first_edge = self.sorted_edges[key][0]
            last_edge = self.sorted_edges[key][-1]
            u, v = first_edge
            self.closed_paths_booleans[key] = u in last_edge or v in last_edge


##############################################################
# DATA = os.path.join(os.path.dirname(__file__), '1_data_cylinder')
# MODEL = 'cylinder_uneven.obj'

DATA = os.path.join(os.path.dirname(__file__), '2_data_bunny')
MODEL = 'bunny.obj'

OUTPUT_DIR = utils.get_output_directory(DATA)  # creates 'output' folder if it doesn't already exist

if __name__ == "__main__":
    print('here')
    mesh = Mesh.from_obj(os.path.join(DATA, MODEL))

    level_slicer = LevelSlicer(mesh, 32.0)
    level_slicer.compute()

    for i, key in enumerate(level_slicer.sorted_points):
        pts_dict = utils.point_list_to_dict(level_slicer.sorted_points[key])
        utils.save_to_json(pts_dict, OUTPUT_DIR, 'pts_%d.json' % i)

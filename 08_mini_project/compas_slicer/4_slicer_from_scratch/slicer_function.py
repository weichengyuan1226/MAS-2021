from compas.geometry import Point, Plane, Vector, intersection_segment_plane
from compas_slicer.slicers.slice_utilities import create_graph_from_mesh_edges, sort_graph_connected_components
import compas_slicer.utilities as utils
import os
from compas.datastructures import Mesh
from compas.geometry import Polyline
import logging

logger = logging.getLogger('logger')
logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.INFO)




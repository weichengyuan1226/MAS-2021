import os
from compas.datastructures import Mesh
import logging
import compas_slicer.utilities as utils
from compas_slicer.slicers import CurvedSlicer
from compas_slicer.post_processing import simplify_paths_rdp
from compas_slicer.pre_processing import CurvedSlicingPreprocessor
from compas_slicer.pre_processing import create_mesh_boundary_attributes
from compas_slicer.print_organization import set_extruder_toggle
from compas_slicer.print_organization import add_safety_printpoints
from compas_slicer.print_organization import set_linear_velocity
from compas_slicer.print_organization import set_blend_radius
from compas_slicer.print_organization import CurvedPrintOrganizer
import time

logger = logging.getLogger('logger')
logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.INFO)

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')
OUTPUT_PATH = utils.get_output_directory(DATA_PATH)
OBJ_INPUT_NAME = os.path.join(DATA_PATH, '_mesh.obj')
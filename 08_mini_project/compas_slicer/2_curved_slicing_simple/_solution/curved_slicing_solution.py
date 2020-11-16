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

start_time = time.time()

### --- Load initial_mesh
print(os.path.dirname(__file__))
mesh = Mesh.from_obj(os.path.join(DATA_PATH, OBJ_INPUT_NAME))

### --- Load targets (boundaries)
low_boundary_vs = utils.load_from_json(DATA_PATH, 'boundaryLOW.json')
high_boundary_vs = utils.load_from_json(DATA_PATH, 'boundaryHIGH.json')
create_mesh_boundary_attributes(mesh, low_boundary_vs, high_boundary_vs)

parameters = {
    'avg_layer_height': 5.0  # controls number of curves that will be generated
}

preprocessor = CurvedSlicingPreprocessor(mesh, parameters, DATA_PATH)
preprocessor.create_compound_targets()

## --- slicing
slicer = CurvedSlicer(mesh, preprocessor, parameters)
slicer.slice_model()  # compute_norm_of_gradient contours
simplify_paths_rdp(slicer, threshold=1.0)
slicer.printout_info()
utils.save_to_json(slicer.to_data(), OUTPUT_PATH, 'curved_slicer.json')

# ### --- Print organizer
print_organizer = CurvedPrintOrganizer(slicer, parameters, DATA_PATH)
print_organizer.create_printpoints()

set_extruder_toggle(print_organizer, slicer)
add_safety_printpoints(print_organizer, z_hop=10.0)
set_linear_velocity(print_organizer, "by_layer_height")
set_blend_radius(print_organizer, d_fillet=10.0)

### --- Save printpoints dictionary to json file
printpoints_data = print_organizer.output_printpoints_dict()
utils.save_to_json(printpoints_data, OUTPUT_PATH, 'out_printpoints.json')

end_time = time.time()
print("Total elapsed time", round(end_time - start_time, 2), "seconds")

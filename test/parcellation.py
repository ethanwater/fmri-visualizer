# Parcellation functions for brain image analysis
# For each timestamp (second) of fMRI data, we have a vector of cortical and subcortical activations.
# These activations are based on grayordinates (cortical vertices and subcortical voxels).
# We can use parcellation to group these activations into meaningful regions of interest (ROIs) for further analysis.   

# Sample output per timestamp: (timestamp, [[...cortical activations...] + [...subcortical activations...]])
# There are 20,484 cortical vertices and 8,802 subcortical voxels, resulting in a total of 29,286 activations per timestamp.

import time
import numpy as np
from nibabel.freesurfer.io import read_annot
from plot.plot_stacked_subplots import plot_stacked_subplots

CORTICAL_VERTICES = 20484 #cortical Activations
SUBCORTICAL_VOXELS = 8802 #subcortical Activations
TOTAL_ACTIVATIONS = CORTICAL_VERTICES + SUBCORTICAL_VOXELS

LR_HEMISPHERE_VERTICES = 10242 # the amount of vertices in both the left and right hemispheres of the cortex
TEST_TIMESTAMPS = 90 # length of the fMRI recording. used for testing.
SIGMA = 1.5

LH_YEO7_2011_NETWORK = "resources/atlases/fsaverage_parcel_outline/lh.Yeo2011_7Networks_N1000.annot"
RH_YEO7_2011_NETWORK = "resources/atlases/fsaverage_parcel_outline/rh.Yeo2011_7Networks_N1000.annot"

cortical_networks = [
    "visual", "somatomotor", "dorsal_attention", 
    "ventral_attention", "limbic", "frontoparietal", "default_mode"
]
subcortical_structures = [
    "thalamus", "caudate", "putamen", "pallidum", 
    "hippocampus", "amygdala", "accumbens", "ventral_diencephalon"
]
all_regions = cortical_networks + subcortical_structures

def load_yeo7_2011_network():
    lh_labels, _, lh_names = read_annot(LH_YEO7_2011_NETWORK)
    rh_labels, _, rh_names = read_annot(RH_YEO7_2011_NETWORK)
    return ((lh_labels, _, lh_names), (rh_labels, _, rh_names))

def temporal_normalization(activations_29286, n_timestamps):
    if n_timestamps > 1:
        # Calculate mean and std for each vertex/voxel across the time axis (axis 1)
        vertex_means = activations_29286.mean(axis=1, keepdims=True)
        vertex_stds = activations_29286.std(axis=1, keepdims=True)
        
        # Prevent division by zero for any silent/masked vertices
        vertex_stds[vertex_stds == 0] = 1.0
        
        # Z-score the raw BOLD data
        normalized_data = (activations_29286 - vertex_means) / vertex_stds
    else:
        # If testing with 1 timestamp, we can't z-score across time, so fallback to raw
        normalized_data = activations_29286

    return normalized_data

def parcellate_activations(activations_29286, n_timestamps, anomalies=None):
    start_time = time.perf_counter()
    #normalize the activation values
    activations_29286_normalized = temporal_normalization(activations_29286, n_timestamps)

    (lh_labels, _, lh_names), (rh_labels, _, rh_names) = load_yeo7_2011_network()

    cortical_activations = activations_29286_normalized[:CORTICAL_VERTICES, :]
    _subcortical_activations = activations_29286_normalized[CORTICAL_VERTICES:, :]

    # split the cortex into left and right hemispheres (10,242 each)
    lh_activations = cortical_activations[:LR_HEMISPHERE_VERTICES, :]
    rh_activations = cortical_activations[LR_HEMISPHERE_VERTICES:, :]

    # dictionaries to accumulate means smoothly instead of mutating tuples
    lh_means = {net: np.zeros(n_timestamps) for net in cortical_networks}
    rh_means = {net: np.zeros(n_timestamps) for net in cortical_networks}

    # helper map to link FreeSurfer .annot string fragments to our cortical_networks list
    yeo_map = {
        b'7Networks_1': 'visual',
        b'7Networks_2': 'somatomotor',
        b'7Networks_3': 'dorsal_attention',
        b'7Networks_4': 'ventral_attention',
        b'7Networks_5': 'limbic',
        b'7Networks_6': 'frontoparietal',
        b'7Networks_7': 'default_mode'
    }

    #left hemisphere
    for idx, name in enumerate(lh_names):
        if name in yeo_map:
            network_key = yeo_map[name]
            mask = (lh_labels == idx)
            if np.any(mask):
                lh_means[network_key] = lh_activations[mask, :].mean(axis=0)

    #right hemisphere
    for idx, name in enumerate(rh_names):
        if name in yeo_map:
            network_key = yeo_map[name]
            mask = (rh_labels == idx)
            if np.any(mask):
                rh_means[network_key] = rh_activations[mask, :].mean(axis=0)

    # final dictionary mapping to the requested tuple layout: (activations_list, standard deviation)
    cortical_parcellation = {}

    for net in cortical_networks:
        bilateral_mean = (lh_means[net] + rh_means[net]) / 2
        metric_value = float(np.std(bilateral_mean))
        
        # save as final tuple: (list of means, metric_value)
        cortical_parcellation[net] = (bilateral_mean.tolist(), metric_value)
        
        # unpack for the print log
        means_list, std_val = cortical_parcellation[net]

    # TODO: we parcellate the subcortex based on Meta's mapping conditions
    end_time = time.perf_counter()
    print(f"Execution Time: {np.round((end_time-start_time) * 1000, decimals=5)}ms")
    plot_stacked_subplots(cortical_parcellation, None, sigma=SIGMA)




def test_parcellate_activations():
    cortical = np.random.randn(TOTAL_ACTIVATIONS, TEST_TIMESTAMPS).astype(np.float32)
    parcellate_activations(cortical, TEST_TIMESTAMPS, anomalies=[22.5])

test_parcellate_activations()
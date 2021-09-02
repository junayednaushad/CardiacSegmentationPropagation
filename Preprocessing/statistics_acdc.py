""" Statistics of the UK Biobank cases """

import sys
sys.path.append('C:\\Users\\mpnau\\Documents\\ml_programs\\CardiacSegmentationPropagation')

import os
import numpy as np
from PIL import Image
from scipy import interpolate
import nibabel as nib

import config



def statistics():

    data_path = config.data_root
    code_path = config.code_root

    statistics_file = os.path.join(code_path, 'Preprocessing', 'statistics_record.txt')
    statistics = open(statistics_file, 'w')

    eids = sorted([x for x in os.listdir(data_path) \
        if os.path.isdir(os.path.join(data_path,x))])

    print('There are {} eids in total'.format(len(eids)))

    useful_eid_count = 0

    # For each case
    for eid in eids:
        print('Processing eid = {}  (# {})'.format(eid, eids.index(eid)) )

        # Define the paths
        eid_path = os.path.join(data_path, eid)
        original_2D_path = os.path.join(eid_path, 'original_2D')

        if not os.path.exists(original_2D_path):
            os.makedirs(original_2D_path)

        sa_zip_file = os.path.join(eid_path, eid+'_4d.nii.gz')

        # Indicators of file existence
        if os.path.isfile(sa_zip_file):
            has_sa = 1
            has_gt_sa = 1
            useful_eid_count += 1
        else:
            has_sa = 0
            has_gt_sa = 0

        rows = 0
        columns = 0
        slices = 0
        times = 0

        spacing_x = -1
        spacing_y = -1
        spacing_z = -1
        spacing_t = -1

        if (has_sa == 1):
            img = nib.load(sa_zip_file)
            (spacing_x, spacing_y, spacing_z, spacing_t) = img.header.get_zooms()
            data = img.get_fdata()

            rows = data.shape[0]
            columns = data.shape[1]
            slices = data.shape[2]
            times = data.shape[3]

        info_path = os.path.join(eid_path, 'Info.cfg')
        with open(info_path, 'r') as f:
            ed_es_instant0 = f.readline()
            ed_es_instant1 = f.readline()
        f.close()
        ed_es_instant0 = int(ed_es_instant0.split('ED: ')[1].split('\n')[0])
        ed_es_instant1 = int(ed_es_instant1.split('ES: ')[1].split('\n')[0])

        files = [x for x in os.listdir(eid_path) if '_gt' in x]
        for file in files:
            if int(file.split('frame')[1].split('_')[0]) == ed_es_instant0:
                instant0_path = os.path.join(eid_path, file)
            if int(file.split('frame')[1].split('_')[0]) == ed_es_instant1:
                instant1_path = os.path.join(eid_path, file)

        # The min/max indices of the slices on which the ground-truth segmentation is present
        ed_es_instant0_min_slice = -1
        ed_es_instant0_max_slice = -1
        ed_es_instant1_min_slice = -1
        ed_es_instant1_max_slice = -1

        instant0 = nib.load(instant0_path).get_fdata()
        for s in range(slices):
            if(instant0[:,:,s].max() > 0):
                if ed_es_instant0_min_slice < 0:
                    ed_es_instant0_min_slice = s
                ed_es_instant0_max_slice = max(ed_es_instant0_max_slice, s)

        instant1 = nib.load(instant1_path).get_fdata()
        for s in range(slices):
            if(instant1[:,:,s].max() > 0):
                if ed_es_instant1_min_slice < 0:
                    ed_es_instant1_min_slice = s
                ed_es_instant1_max_slice = max(ed_es_instant1_max_slice, s)
    
        written = '{0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10} {11} {12} {13} {14} {15} {16}\n'\
            .format(eid, has_sa, has_gt_sa, \
                    rows, columns, slices, \
                    times, ed_es_instant0, ed_es_instant1, \
                    ed_es_instant0_min_slice, ed_es_instant0_max_slice, ed_es_instant1_min_slice,\
                    ed_es_instant1_max_slice, spacing_x, spacing_y, \
                    spacing_z, spacing_t)

        statistics.write(written)

    statistics.close()

    print('useful_eid_count = {}'.format(useful_eid_count) )   

  


if __name__ == '__main__':
    statistics()
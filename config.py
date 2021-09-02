#!/usr/bin/env python

# Directory of the UK Biobank data
data_root = 'D:\\acdc_training'

# Directory of the CardiacSegmentationPropagation project
code_root = 'C:\\Users\\mpnau\\Documents\\ml_programs\\CardiacSegmentationPropagation'


# ROI-net
roi_net_initial_lr = 1e-4
roi_net_decay_rate = 1.0
roi_net_batch_size = 16
roi_net_imput_img_size = 128
roi_net_epochs = 50


# LVRV-net
lvrv_net_initial_lr = 1e-4
lvrv_net_decay_rate = 1.0
lvrv_net_batch_size = 16
lvrv_net_imput_img_size = 192
lvrv_net_epochs = 80


# LV-net
lv_net_initial_lr = 1e-4
lv_net_decay_rate = 1.0
lv_net_batch_size = 16
lv_net_imput_img_size = 192
lv_net_epochs = 80



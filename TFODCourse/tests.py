import os

CUSTOM_MODEL_NAME = 'my_ssd_mobnet' 
PRETRAINED_MODEL_NAME = 'ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8'
PRETRAINED_MODEL_URL = 'http://download.tensorflow.org/models/object_detection/tf2/20200711/ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8.tar.gz'
TF_RECORD_SCRIPT_NAME = 'generate_tfrecord.py'
LABEL_MAP_NAME = 'label_map.pbtxt'

paths = {
    'WORKSPACE_PATH': os.path.join('Tensorflow', 'workspace'),
    'SCRIPTS_PATH': os.path.join('Tensorflow','scripts'),
    'APIMODEL_PATH': os.path.join('Tensorflow','models'),
    'ANNOTATION_PATH': os.path.join('Tensorflow', 'workspace','annotations'),
    #'IMAGE_PATH': os.path.join('Tensorflow', 'workspace','images'),
    'IMAGE_PATH':'C:\\Users\\User\\Documents\\GitHub\\AntiAir-Balloon-Detection-AI\\TFODCourse\\Tensorflow\\workspace\\images',
    'MODEL_PATH': os.path.join('Tensorflow', 'workspace','models'),
    'PRETRAINED_MODEL_PATH': os.path.join('Tensorflow', 'workspace','pre-trained-models'),
    'CHECKPOINT_PATH': os.path.join('TFODCourse', 'Tensorflow', 'workspace','models',CUSTOM_MODEL_NAME), 
    'OUTPUT_PATH': os.path.join('Tensorflow', 'workspace','models',CUSTOM_MODEL_NAME, 'export'), 
    'TFJS_PATH':os.path.join('Tensorflow', 'workspace','models',CUSTOM_MODEL_NAME, 'tfjsexport'), 
    'TFLITE_PATH':os.path.join('Tensorflow', 'workspace','models',CUSTOM_MODEL_NAME, 'tfliteexport'), 
    'PROTOC_PATH':os.path.join('Tensorflow','protoc')
 }

files = {
    #'PIPELINE_CONFIG':os.path.join('Tensorflow', 'workspace','models', CUSTOM_MODEL_NAME, 'pipeline.config'),
    'PIPELINE_CONFIG':"C:\\Users\\User\\Documents\\GitHub\\AntiAir-Balloon-Detection-AI\\TFODCourse\\Tensorflow\\workspace\\models\\my_ssd_mobnet\\pipeline.config",
    'TF_RECORD_SCRIPT': os.path.join(paths['SCRIPTS_PATH'], TF_RECORD_SCRIPT_NAME), 
    #'LABELMAP': os.path.join(paths['ANNOTATION_PATH'], LABEL_MAP_NAME)
    'LABELMAP':'C:\\Users\\User\\Documents\\GitHub\\AntiAir-Balloon-Detection-AI\\TFODCourse\\Tensorflow\\workspace\\annotations\\label_map.pbtxt'
}

import sys
# needs to be changed manually - path to models
path = "C:\\Users\\User\\Documents\\GitHub\\AntiAir-Balloon-Detection-AI\\TFODCourse\\models"
os.environ['Path'] += path
sys.path.append(path)

import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util

# Load pipeline config and build a detection model
configs = config_util.get_configs_from_pipeline_file(files['PIPELINE_CONFIG'])
detection_model = model_builder.build(model_config=configs['model'], is_training=False)

# Restore checkpoint
ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
ckpt.restore(os.path.join(paths['CHECKPOINT_PATH'], 'ckpt-11')).expect_partial()

@tf.function
def detect_fn(image):
    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)
    return detections

import cv2 
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from object_detection.utils import label_map_util, visualization_utils as viz_utils
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')

category_index = label_map_util.create_category_index_from_labelmap(files['LABELMAP'])

IMAGE_PATH = os.path.join(paths['IMAGE_PATH'], 'test', '219.png')

tf.config.run_functions_eagerly(True)

# Load the image and convert to numpy array
img = cv2.imread(IMAGE_PATH)
image_np = np.array(img)

# Run object detection on the image
input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
detections = detect_fn(input_tensor)

# Process the detection results
num_detections = int(detections.pop('num_detections'))
detections = {key: value[0, :num_detections].numpy()
              for key, value in detections.items()}
detections['num_detections'] = num_detections
detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

# Add labels to the detected objects
# Needs to be changed manually
label_map_path = 'C:\\Users\\User\\Documents\\GitHub\\AntiAir-Balloon-Detection-AI\\TFODCourse\\models\\research\\object_detection\\data\\mscoco_label_map.pbtxt'
label_map = label_map_util.load_labelmap(label_map_path)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=90, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# Visualize the detected objects on the image
viz_utils.visualize_boxes_and_labels_on_image_array(
            image_np,
            detections['detection_boxes'],
            detections['detection_classes']+1,
            detections['detection_scores'],
            category_index,
            use_normalized_coordinates=True,
            max_boxes_to_draw=1,
            min_score_thresh=.1,
            agnostic_mode=True)

# Show the image with the detected objects
plt.imshow(cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB))
plt.show()

# Print the coordinates of the first detected object
bbox = detections['detection_boxes'][0]
height, width, _ = image_np.shape
xmin, xmax, ymin, ymax = bbox
xmin = xmin * width; xmax = xmax * width
ymin = ymin * height; ymax = ymax * height
bbox = (xmin, ymax, xmax, ymin)
print('Bbox coordinates:', bbox)
#!/usr/bin/env python3


from tensorflow import keras
from keras_retinanet import models
from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image
from keras_retinanet.utils.visualization import draw_box, draw_caption
from keras_retinanet.utils.colors import label_color
import matplotlib.pyplot as plt
import cv2
import os
import numpy as np
import time
import matplotlib.pyplot as plt


class RetinaNet:
    def __init__(self, model_dir_path, weight_file_name):

        self.predictions = []

        self.model_dir_path = model_dir_path
        self.weight_file_name = weight_file_name
        
        self.labels_to_names = self.load_classes()
        self.build_model()  

    def build_model(self) :

        try :
            self.model_path = os.path.join(self.model_dir_path, self.weight_file_name)
            self.model = models.load_model(self.model_path, backbone_name='resnet50')

        except :
            raise Exception("Error loading given model from path: {}. Maybe the file doesn't exist?".format(self.model_path))


    def load_classes(self):
        self.class_list = []
        with open(self.model_dir_path + "/classes.txt", "r") as f:
            self.class_list = [cname.strip() for cname in f.readlines()]
        return self.class_list
    
    def create_predictions_list(self, class_ids, confidences, boxes):
        for i in range(len(class_ids)):
            obj_dict = {
                "class_id": class_ids[i],
                "confidence": confidences[i],
                "box": boxes[i]
            }

            self.predictions.append(obj_dict)
        

    def get_predictions(self, cv_image):      

        # copy to draw on
        self.frame = cv_image.copy()
        # preprocess image for network
        input = preprocess_image(cv_image)
        input, scale = resize_image(input)

        # process image
        start = time.time()
        boxes, scores, labels = self.model.predict_on_batch(np.expand_dims(input, axis=0))
        print("processing time: ", time.time() - start)

        # correct for image scale
        boxes /= scale

        self.create_predictions_list(labels, scores, boxes)

        # visualize detections
        for box, score, label in zip(boxes[0], scores[0], labels[0]):
            # scores are sorted so we can break
            if score < 0.5:
                break
                
            color = label_color(label)
            
            b = box.astype(int)
            draw_box(self.frame, b, color=color)
            
            caption = "{} {:.3f}".format(self.labels_to_names[label], score)
            print(self.labels_to_names[label])
            draw_caption(self.frame, b, caption)

        return (self.predictions,self.frame)
              
        
        

if __name__ == '__main__' :
    

    ok = RetinaNet()
        

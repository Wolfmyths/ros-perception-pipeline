import cv2
from ultralytics import YOLO
import os

class YOLOv8:
  def __init__(self, model_dir_path, weight_file_name, conf_threshold = 0.7, score_threshold = 0.4, nms_threshold = 0.25):
    # Load model 
    self.model_dir_path = model_dir_path
    self.weight_file_name = weight_file_name

    
    self.conf_threshold = conf_threshold
    self.predictions = []
    self.build_model()
    self.load_classes()


  def build_model(self) :

    try :
      model_path = os.path.join(self.model_dir_path, self.weight_file_name)
      self.model = YOLO(model_path)
    
    except :
      raise Exception("Error loading given model from path: {}. Maybe the file doesn't exist?".format(model_path))
  
  def load_classes(self):

    self.class_list = []

    with open(self.model_dir_path + "/classes.txt", "r") as f:
        self.class_list = [cname.strip() for cname in f.readlines()]

    return self.class_list

  # create list of dictionary containing predictions
  def create_predictions_list(self, class_ids, confidences, boxes):  
    
    for i in range(len(class_ids)):
        obj_dict = {
            "class_id": class_ids[i],
            "confidence": confidences[i],
            "box": boxes[i]
        }
        self.predictions.append(obj_dict)

  def get_predictions(self, cv_image):
    
    class_id = []
    confidence = []
    bb = []
    result = self.model.predict(cv_image, conf = self.conf_threshold) # Perform object detection on image
    row = result[0].boxes

    for box in row:
      class_id.append(box.cls)
      confidence.append(box.conf)
      bb.append(box.xyxy)
      
    self.create_predictions_list(class_id,confidence,bb)
    result = self.model.predict(cv_image, conf = self.conf_threshold)
    bb_result = result[0].plot()                  # Frame with bounding boxes

    return self.predictions,bb_result
 
# Code for running YOLO image detection and segmentation algorithm
# Written by Walter Stark

from ultralytics import YOLO
import cv2
from ultralytics.utils.ops import scale_image # THis might be an issue, removed ".ops" after utils
import numpy as np
# Note: maybe want to train YOLO model on household items

model = YOLO('yolov8x-seg.pt') # load oficial segmenting model - model with low CPU usage


def  outputSegment (frame):
    
    #output = model.predict(source = frame, conf=0.5, show=True, device = 0) # Device is cuda
    
    # predict by YOLOv8
    #boxes, masks, cls, probs, result = predict_on_image(model, frame, conf=0.55)

    '''
    # overlay masks on original image
    image_with_masks = np.copy(frame)
    for mask_i in masks:
        image_with_masks = overlay(image_with_masks, mask_i, color=(0,255,0), alpha=0.3)
    '''

    result = model(frame, conf=0.2, device = 'cuda')
    image_with_masks = result[0].plot()



    return image_with_masks




# Code below not end up being used

# TWEAKED FROM ORIGINAL SOURCE:  https://github.com/ultralytics/ultralytics/issues/561
def overlay(image, mask, color, alpha, resize=None):
    """Combines image and its segmentation mask into a single image.
    https://www.kaggle.com/code/purplejester/showing-samples-with-segmentation-mask-overlay

    Params:
        image: Training image. np.ndarray,
        mask: Segmentation mask. np.ndarray,
        color: Color for segmentation mask rendering.  tuple[int, int, int] = (255, 0, 0)
        alpha: Segmentation mask's transparency. float = 0.5,
        resize: If provided, both image and its mask are resized before blending them together.
        tuple[int, int] = (1024, 1024))

    Returns:
        image_combined: The combined image. np.ndarray

    """
    color = color[::-1]
    colored_mask = np.expand_dims(mask, 0).repeat(3, axis=0)
    colored_mask = np.moveaxis(colored_mask, 0, -1)
    masked = np.ma.MaskedArray(image, mask=colored_mask, fill_value=color)
    image_overlay = masked.filled()

    if resize is not None:
        image = cv2.resize(image.transpose(1, 2, 0), resize)
        image_overlay = cv2.resize(image_overlay.transpose(1, 2, 0), resize)

    image_combined = cv2.addWeighted(image, 1 - alpha, image_overlay, alpha, 0)


    return image_combined

# TWEAKED FROM ORIGINAL SOURCE: https://github.com/ultralytics/ultralytics/issues/561
def predict_on_image(model, img, conf):
    result = model(img, conf=conf)[0]

    # detection
    # result.boxes.xyxy   # box with xyxy format, (N, 4)
    cls = result.boxes.cls.cpu().numpy()    # cls, (N, 1)
    probs = result.boxes.conf.cpu().numpy()  # confidence score, (N, 1)
    boxes = result.boxes.xyxy.cpu().numpy()   # box with xyxy format, (N, 4)

    # segmentation
    masks = result.masks.masks.cpu().numpy()     # masks, (N, H, W)
    masks = np.moveaxis(masks, 0, -1) # masks, (H, W, N)
    # rescale masks to original image
    masks = scale_image(masks.shape[:2], masks, result.masks.orig_shape)
    masks = np.moveaxis(masks, -1, 0) # masks, (N, H, W)

    return boxes, masks, cls, probs, result

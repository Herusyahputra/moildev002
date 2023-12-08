import os
import sys

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from moildev import Moildev
import cv2

#  Specify the size of window show image
w, h = 400, 300

# original image as input
image = cv2.imread("front.png")
image_colon = cv2.imread("20221214_internal_thread.png")
image_colon = cv2.circle(image_colon, (1295, 1844), 25, (0, 255, 0), 25)
print(image.shape)
original_colon = cv2.resize(image_colon, (w, h))
cv2.imshow("original colon", original_colon)

original = cv2.resize(image, (w, h))
cv2.imshow("original", original)

# create moildev object
moildev = Moildev("camera_parameters.json", "entaniya")

# test anypoint mode 1
map_x, map_y = moildev.maps_anypoint_mode1(90, 180, 2)
anypoint_m1_by_maps = cv2.remap(image_colon, map_x, map_y, cv2.INTER_CUBIC)
anypoint_m1_by_maps = cv2.resize(anypoint_m1_by_maps, (w, h))
cv2.imshow("anypoint mode 1 by maps", anypoint_m1_by_maps)

anypoint_m1 = moildev.anypoint_mode1(image_colon, 90, 180, 2)
anypoint_m1 = cv2.resize(anypoint_m1, (w, h))
cv2.imshow("anypoint mode 1", anypoint_m1)

# test anypoint mode 2 car
map_x, map_y = moildev.maps_anypoint_mode2(-90, 0, 0, 3)
anypoint_m2_by_maps = cv2.remap(image, map_x, map_y, cv2.INTER_CUBIC)
anypoint_m2_by_maps = cv2.resize(anypoint_m2_by_maps, (w, h))
cv2.imshow("anypoint mode 2 by maps", anypoint_m2_by_maps)

anypoint_m2 = moildev.anypoint_mode2(image, -90, 0, 0, 3)
anypoint_m2 = cv2.resize(anypoint_m2, (w, h))
cv2.imshow("anypoint mode 2", anypoint_m2)

# panorama tube
panorama_tube = moildev.panorama_tube(image_colon, 10, 110)
panorama_tube = cv2.resize(panorama_tube, (w, h))
cv2.imshow("panorama tube", panorama_tube)

# test panorama car
panorama_car = moildev.panorama_car(image, 110, 100, 0, 0.25, 0.75, 0, 1)
panorama_car = cv2.resize(panorama_car, (w * 2, h))
cv2.imshow("panorama car", panorama_car)

recenter = moildev.recenter(image, 110, 25, 10)
recenter = cv2.resize(recenter, (w, h))
cv2.imshow("recenter", recenter)

cv2.waitKey(0)

import os
import sys
import cv2

from moildev import Moildev

# this is to resize image show
w = 400
h = 300

image_1 = cv2.imread("/home/heru-demo/PycharmProjects/test_moildev/moildev/unitest/front.png")
image_11 = cv2.imread("/home/heru-demo/PycharmProjects/test_moildev/moildev/unitest/20221214_internal_thread.png")
image_2 = cv2.circle(image_11, (1295, 1844), 25, (0, 255, 255), 25)
ori_image_1 = cv2.resize(image_1, (w, h))
ori_image_2 = cv2.resize(image_2, (w, h))

cv2.imshow("original image 1", ori_image_1)
cv2.imshow("original image 2", ori_image_2)

moildev = Moildev("/home/heru-demo/PycharmProjects/test_moildev/moildev/unitest/camera_parameters.json", "entaniya")

# anypoint maps mode 1
map_X, map_Y = moildev.maps_anypoint_mode1(90, 180, 2)
anypoint_maps_m1 = cv2.remap(image_2, map_X, map_Y, cv2.INTER_LINEAR)
anypoint_maps_m1 = cv2.resize(anypoint_maps_m1, (w, h))
cv2.imshow("anypoint maps mode 1", anypoint_maps_m1)

# anypoint mode 1
anypoint_m1 = moildev.anypoint_mode1(image_2, 90, 180, 2)
anypoint_m1 = cv2.resize(anypoint_m1, (w, h))
cv2.imshow("anypoint made 1", anypoint_m1)

# anypoint maps mode 2
map_X, map_Y = moildev.maps_anypoint_mode2(-90, 0, 0, 2)
anypoint_maps_m2 = cv2.remap(image_1, map_X, map_Y, cv2.INTER_CUBIC)
anypoint_maps_m2 = cv2.resize(anypoint_maps_m2, (w, h))
cv2.imshow("anypoint maps mode 2", anypoint_maps_m2)

# anypoint mode 2
anypoint_m2 = moildev.anypoint_mode2(image_1, -90, 0, 0, 2)
anypoint_m2 = cv2.resize(anypoint_m2, (w, h))
cv2.imshow("anypoint mode 2", anypoint_m2)

# panorama tube
panorama_tube = moildev.panorama_tube(image_2, 10, 110)
panorama_tube = cv2.resize(panorama_tube, (w, h))
cv2.imshow("panorama tube", panorama_tube)

# panorama car
panorama_car = moildev.panorama_car(image_1, 110, 80, 0, 0.25, 0.75, 0, 1)
panorama_car = cv2.resize(panorama_car, (w * 2, h))
cv2.imshow("panorama car", panorama_car)

# recenter image
recenter = moildev.recenter(image_1, 110, 25, 10)
recenter = cv2.resize(recenter, (w, h))
cv2.imshow("recenter 2", recenter)

recenter = moildev.recenter(image_1, 90, 0, 10)
# recenter_pano = moildev.panorama_tube(recenter, 10, 110)
recenter_pano = cv2.resize(recenter, (w, h))
cv2.imshow("recenter", recenter_pano)

alpha, beta = moildev.get_alpha_beta(401, 894, 1)
print(alpha, beta)
map_X, map_Y = moildev.maps_anypoint_mode1(alpha, beta, 2)
get_alpha_beta = cv2.remap(image_1, map_X, map_Y, cv2.INTER_CUBIC)
get_alpha_beta = cv2.resize(get_alpha_beta, (w, h))
cv2.imshow("alpha_beta", get_alpha_beta)

test_rho = moildev.get_alpha_from_rho(891)
test_alpha = moildev.get_rho_from_alpha(90)
print(test_rho, test_alpha)

alpha, beta = moildev.get_alpha_beta(1944, 842.4, 1)
map_X, map_Y = moildev.maps_anypoint_mode1(alpha, beta, 2)
get_alpha_b = cv2.remap(image_1, map_X, map_Y, cv2.INTER_LINEAR)
get_alpha_b = cv2.resize(get_alpha_b, (w, h))
cv2.imshow("get_alpha_beta", get_alpha_b)
cv2.waitKey(0)


# moildev method can implementation by myself
#=============================================
# moildev.maps_anypoint_mode1(alpha, beta, zoom)
# moildev.maps_anypoint_mode2(pitch, yaw, roll, zoom)
# moildev.anypoint_mode1(image_1, alpha, beta, zoom)
# moildev.anypoint_mode2(image_1, pitch, yaw, roll, zoom)
# moildev.panorama_tube(image_1, alpha_min, alpha_max)
# moildev.panorama_car(image_1, alpha_max, alpha, beta, left, right, top, bottom)
# moildev.recenter(image_1, Ic_alpha, Ic_beta)
# moildev.get_alpha_beta(coordinateX, coordinateY, mode)
# moildev.icx, moildev.icy
# moildev.get_rho_from_alpha()
# moildev.get_alpha+from_rho()


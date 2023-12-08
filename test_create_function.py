import os
import sys
import cv2
from moildev import Moildev

class Main():
    # this is to resize image show
    def __init__(self):
        self.w = 400
        self.h = 300

        self.image_1 = cv2.imread("/home/heru-demo/PycharmProjects/test_moildev/moildev/unitest/front.png")
        self.image_11 = cv2.imread("/home/heru-demo/PycharmProjects/test_moildev/moildev/unitest/20221214_internal_thread.png")
        self.image_2 = cv2.circle(self.image_11, (1295, 1844), 25, (0, 255, 255), 25)
        ori_image_1 = cv2.resize(self.image_1, (self.w, self.h))
        ori_image_2 = cv2.resize(self.image_2, (self.w, self.h))

        # cv2.imshow("original image 1", ori_image_1)
        # cv2.imshow("original image 2", ori_image_2)

        self.moildev = Moildev("/home/heru-demo/PycharmProjects/test_moildev/moildev/unitest/camera_parameters.json", "entaniya")

    def anypoint_maps_m1(self):
        # anypoint maps mode 1
        map_X, map_Y = self.moildev.maps_anypoint_mode1(90, 180, 2)
        anypoint_maps_m1 = cv2.remap(self.image_2, map_X, map_Y, cv2.INTER_LINEAR)
        anypoint_maps_m1 = cv2.resize(anypoint_maps_m1, (self.w, self.h))
        # cv2.imshow("anypoint maps mode 1", anypoint_maps_m1)
        return anypoint_maps_m1

    def anypoint_m1(self):
        # anypoint mode 1
        anypoint_m1 = self.moildev.anypoint_mode1(self.image_2, 90, 180, 2)
        anypoint_m1 = cv2.resize(anypoint_m1, (self.w, self.h))
        # cv2.imshow("anypoint made 1", anypoint_m1)
        return anypoint_m1

    def anypoint_maps_m2(self):
        # anypoint maps mode 2
        map_X, map_Y = self.moildev.maps_anypoint_mode2(-90, 0, 0, 2)
        anypoint_maps_m2 = cv2.remap(self.image_1, map_X, map_Y, cv2.INTER_CUBIC)
        anypoint_maps_m2 = cv2.resize(anypoint_maps_m2, (self.w, self.h))
        # cv2.imshow("anypoint maps mode 2", anypoint_maps_m2)
        return anypoint_maps_m2

    def anypoint_m2(self):
        # anypoint mode 2
        anypoint_m2 = self.moildev.anypoint_mode2(self.image_1, -90, 0, 0, 2)
        anypoint_m2 = cv2.resize(anypoint_m2, (self.w, self.h))
        # cv2.imshow("anypoint mode 2", anypoint_m2)
        return anypoint_m2

    def panorama_tube(self):
        # panorama tube
        panorama_tube = self.moildev.panorama_tube(self.image_2, 10, 110)
        panorama_tube = cv2.resize(panorama_tube, (self.w, self.h))
        # cv2.imshow("panorama tube", panorama_tube)
        return panorama_tube

    def panorama_car(self):
        # panorama car
        panorama_car = self.moildev.panorama_car(self.image_1, 110, 80, 0, 0.25, 0.75, 0, 1)
        panorama_car = cv2.resize(panorama_car, (self.w * 2, self.h))
        # cv2.imshow("panorama car", panorama_car)
        return panorama_car

    def recenter(self):
        # recenter image
        recenter = self.moildev.recenter(self.image_2, 110, 25, 10)
        recenter = cv2.resize(recenter, (self.h))
        # cv2.imshow("recenter 2", recenter)
        return recenter

    def show_image(self):
        image = self.image_1.copy()
        # image = moildev.


# recenter = moildev.recenter(image_2, 90, 0, 10)
# # recenter_pano = moildev.panorama_tube(recenter, 10, 110)
# recenter_pano = cv2.resize(recenter, (w, h))
# cv2.imshow("recenter", recenter_pano)
#
# alpha, beta = moildev.get_alpha_beta(401, 894, 1)
# print(alpha, beta)
# map_X, map_Y = moildev.maps_anypoint_mode1(alpha, beta, 2)
# get_alpha_beta = cv2.remap(image_1, map_X, map_Y, cv2.INTER_CUBIC)
# get_alpha_beta = cv2.resize(get_alpha_beta, (w, h))
# cv2.imshow("alpha_beta", get_alpha_beta)

# cv2.waitKey(0)

# moildev.maps_anypoint_mode1(alpha, beta, zoom)
# moildev.maps_anypoint_mode2(pitch, yaw, roll, zoom)
# moildev.anypoint_mode1(image_1, alpha, beta, zoom)
# moildev.anypoint_mode2(image_1, pitch, yaw, roll, zoom)
# moildev.panorama_tube(image_1, alpha_min, alpha_max)
# moildev.panorama_car(image_1, alpha_max, alpha, beta, left, right, top, bottom)
# moildev.recenter(image_1, Ic_alpha, Ic_beta)
# moildev.get_alpha_beta(coordinateX, coordinateY, mode)
# moildev.icx, moildev.icy


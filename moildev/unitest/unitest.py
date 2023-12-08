# testing file for Moildev sdk
import unittest
import json
from inspect import getmembers, isfunction
import sys, os

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from moildev import Moildev
import numpy as np
import cv2

print("Version Moildev:")
Moildev.version()
print("\n\n")

print("This is the function available in Moildev SDK \n"
      "Function with (__) symbol is private function.\n"
      "==================================================")

for name, _ in getmembers(Moildev, isfunction):
    print("Function Name: ", name)

print("\nDocstring for every function in Moildev SDK\n"
      "==================================================")
for name, _ in getmembers(Moildev, isfunction):
    help(getattr(Moildev, name))


class TestMoildev(unittest.TestCase):
    image = "front.png"
    camera_parameter = 'camera_parameters.json'
    camera_type = "Raspi"
    with open(camera_parameter) as f:
        data = json.load(f)
        if camera_type in data.keys():
            camera_name = data[camera_type]["cameraName"]
            camera_fov = data[camera_type]["cameraFov"]
            sensor_width = data[camera_type]['cameraSensorWidth']
            sensor_height = data[camera_type]['cameraSensorHeight']
            icx = data[camera_type]['iCx']
            icy = data[camera_type]['iCy']
            ratio = data[camera_type]['ratio']
            image_width = data[camera_type]['imageWidth']
            image_height = data[camera_type]['imageHeight']
            calibrationRatio = data[camera_type]['calibrationRatio']
            parameter0 = data[camera_type]['parameter0']
            parameter1 = data[camera_type]['parameter1']
            parameter2 = data[camera_type]['parameter2']
            parameter3 = data[camera_type]['parameter3']
            parameter4 = data[camera_type]['parameter4']
            parameter5 = data[camera_type]['parameter5']

    moildev = Moildev(camera_parameter, camera_type)
    maps = np.zeros((image_height, image_width), dtype=np.float32)
    image = cv2.imread(image)

    def version(self):
        self.moildev.version()
        self.assertTrue(True)

    def test_get_camera_name(self):
        self.assertEqual(self.moildev.camera_name, self.camera_name)

    def test_get_camera_fov(self):
        self.assertEqual(self.moildev.camera_fov, self.camera_fov)

    def test_get_icx(self):
        self.assertEqual(self.moildev.icx, self.icx)

    def test_get_icy(self):
        self.assertEqual(self.moildev.icy, self.icy)

    def test_image_width(self):
        self.assertEqual(self.moildev.image_width, self.image_width)

    def test_image_height(self):
        self.assertEqual(self.moildev.image_height, self.image_height)

    def test_get_param_0(self):
        self.assertEqual(self.moildev.param_0, self.parameter0)

    def test_get_param_1(self):
        self.assertEqual(self.moildev.param_1, self.parameter1)

    def test_get_param_2(self):
        self.assertEqual(self.moildev.param_2, self.parameter2)

    def test_get_param_3(self):
        self.assertEqual(self.moildev.param_3, self.parameter3)

    def test_get_param_4(self):
        self.assertEqual(self.moildev.param_4, self.parameter4)

    def test_get_param_5(self):
        self.assertEqual(self.moildev.param_5, self.parameter5)

    def test_maps_anypoint(self):
        maps_x, _ = self.moildev.maps_anypoint_mode1(10, 5, 4)
        self.assertNotEqual(maps_x.all(), self.maps.all())

    def test_maps_anypoint_car(self):
        maps_x, _ = self.moildev.maps_anypoint_mode2(10, 5, 4, 2)
        self.assertNotEqual(maps_x.all(), self.maps.all())

    def test_maps_panorama_car(self):
        maps_x, _ = self.moildev.maps_panorama_car(110, 140, -6, 0, 1)
        self.assertEqual(maps_x.all(), self.maps.all())

    def test_maps_recenter_optical_point(self):
        maps_x, _ = self.moildev.maps_recenter(110, 20)
        self.assertEqual(maps_x.all(), self.maps.all())

    def test_maps_panorama_tube(self):
        maps_x, _ = self.moildev.maps_panorama_tube(20, 110)
        self.assertEqual(maps_x.all(), self.maps.all())

    def test_anypoint_mode1_image(self):
        img = self.image.copy()
        image_anypoint_car = self.moildev.anypoint_mode1(img, 0, 0, 4)
        self.assertEqual(image_anypoint_car.all(), img.all())

    def test_anypoint_mode2_image(self):
        img = self.image.copy()
        image_anypoint_car = self.moildev.anypoint_mode2(img, 0, 0, 10, 4)
        self.assertEqual(image_anypoint_car.all(), img.all())

    def test_panorama_car(self):
        img = self.image.copy()
        image_anypoint_car = self.moildev.panorama_car(img, 1100, 0, 0, 0,1,0,1)
        self.assertEqual(image_anypoint_car.all(), img.all())

    def test_panorama_tube(self):
        img = self.image.copy()
        image_anypoint_car = self.moildev.panorama_tube(img, 20, 110)
        self.assertEqual(image_anypoint_car.all(), img.all())

    def test_recenter(self):
        img = self.image.copy()
        image_anypoint_car = self.moildev.recenter(img, 110, 0,0)
        self.assertEqual(image_anypoint_car.all(), img.all())

    def test_getAlphabeta(self):
        alpha, beta = self.moildev.get_alpha_beta(500, 500, 2)
        self.assertTrue(alpha is not None)

    def test_alpha_from_rho(self):
        alpha = self.moildev.get_alpha_from_rho(200)
        self.assertTrue(alpha is not None)

    def test_rho_from_alpha(self):
        rho = self.moildev.get_rho_from_alpha(20)
        self.assertTrue(rho is not None)


if __name__ == '__main__':
    unittest.main()

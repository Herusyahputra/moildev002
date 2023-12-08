import math
import json
import cv2
import numpy as np
from .dll import MoilCV
import warnings


class Moildev(object):
    def __init__(self, file_camera_parameter=None, camera_type=None, **kwarg):
        """
        Before the ensuing functions can function properly,
        the camera parameter must be configured at the start of the program.
        The camera parameter is the outcome of the MOIL laboratory's calibration camera.

        Args:
            file_camera_parameter: *.json file
            camera_type : the name of the camera type used (use if yore pass the parameter using *.json file)
            cameraName : the name of the camera used
            cameraFov : camera field of view (FOV)
            sensor_width : size of sensor width
            sensor_height : size of sensor height
            Icx : center image in x-axis
            Icy : center image in y-axis
            ratio : the value of the ratio image
            imageWidth : the size of width image
            imageHeight : the size of height image
            calibrationRatio : the value of calibration ratio
            parameter0 .. parameter5 : intrinsic fisheye camera parameter get from calibration

        .. code-block :: markdown

            for more detail, please reference https://github.com/perseverance-tech-tw/moildev
        """
        super(Moildev, self).__init__()
        self.__alpha_to_rho_table = []
        self.__rho_to_alpha_table = []

        self.__camera_name = None
        self.__camera_fov = None
        self.__sensor_width = None
        self.__sensor_height = None
        self.__icx = None
        self.__icy = None
        self.__ratio = None
        self.__image_width = None
        self.__image_height = None
        self.__calibration_ratio = None
        self.__parameter_0 = None
        self.__parameter_1 = None
        self.__parameter_2 = None
        self.__parameter_3 = None
        self.__parameter_4 = None
        self.__parameter_5 = None

        if file_camera_parameter is None:
            if kwarg == {}:
                print("Pass the argument with camera parameter file with json extension (*.json),\n"
                      "see detail documentation here https://github.com/perseverance-tech-tw/moildev")

            else:
                for key, value in kwarg.items():
                    if key == "camera_name":
                        self.__camera_name = value
                    elif key == "camera_fov":
                        self.__camera_fov = value
                    elif key == "sensor_width":
                        self.__sensor_width = value
                    elif key == "sensor_height":
                        self.__sensor_height = value
                    elif key == "icx":
                        self.__icx = value
                    elif key == "icy":
                        self.__icy = value
                    elif key == "ratio":
                        self.__ratio = value
                    elif key == "image_width":
                        self.__image_width = value
                    elif key == "image_height":
                        self.__image_height = value
                    elif key == "calibration_ratio":
                        self.__calibration_ratio = value
                    elif key == "parameter_0":
                        self.__parameter_0 = value
                    elif key == "parameter_1":
                        self.__parameter_1 = value
                    elif key == "parameter_2":
                        self.__parameter_2 = value
                    elif key == "parameter_3":
                        self.__parameter_3 = value
                    elif key == "parameter_4":
                        self.__parameter_4 = value
                    elif key == "parameter_5":
                        self.__parameter_5 = value

                if self.__camera_name is None or \
                        self.__camera_fov is None or \
                        self.__sensor_width is None or \
                        self.__sensor_height is None or \
                        self.__icx is None or \
                        self.__icy is None or \
                        self.__ratio is None or \
                        self.__image_width is None or \
                        self.__image_height is None or \
                        self.__calibration_ratio is None or \
                        self.__parameter_0 is None or \
                        self.__parameter_1 is None or \
                        self.__parameter_2 is None or \
                        self.__parameter_3 is None or \
                        self.__parameter_4 is None or \
                        self.__parameter_5 is None:
                    warnings.warn("You're not passing the complete parameter. please refer to the documentation here "
                                  "https://github.com/perseverance-tech-tw/moildev ")

                else:
                    self.__init_alpha_rho_table()
                    self.__import_moildev()
        else:
            self.__setCamera_parameter(file_camera_parameter, camera_type)
            if self.__camera_name is not None:
                self.__init_alpha_rho_table()
                self.__import_moildev()

    def __setCamera_parameter(self, parameter, cameraType):
        """
        Set up the configuration of the camera parameter

        Args:
            parameter: the *.json file
            cameraType: type of the camera

        Returns:
            None
        """
        with open(parameter) as f:
            data = json.load(f)
            if cameraType in data.keys():
                self.__camera_name = data[cameraType]["cameraName"]
                self.__camera_fov = data[cameraType]["cameraFov"] if "cameraFov" in data[cameraType].keys() else 220
                self.__sensor_width = data[cameraType]['cameraSensorWidth']
                self.__sensor_height = data[cameraType]['cameraSensorHeight']
                self.__icx = data[cameraType]['iCx']
                self.__icy = data[cameraType]['iCy']
                self.__ratio = data[cameraType]['ratio']
                self.__image_width = data[cameraType]['imageWidth']
                self.__image_height = data[cameraType]['imageHeight']
                self.__calibration_ratio = data[cameraType]['calibrationRatio']
                self.__parameter_0 = data[cameraType]['parameter0']
                self.__parameter_1 = data[cameraType]['parameter1']
                self.__parameter_2 = data[cameraType]['parameter2']
                self.__parameter_3 = data[cameraType]['parameter3']
                self.__parameter_4 = data[cameraType]['parameter4']
                self.__parameter_5 = data[cameraType]['parameter5']

            else:
                if "cameraName" in data.keys() and cameraType is None:
                    with open(parameter) as file:
                        data = json.load(file)
                        self.__camera_name = data["cameraName"]
                        self.__camera_fov = data["cameraFov"] if "cameraFov" in data.keys() else 220
                        self.__sensor_width = data['cameraSensorWidth']
                        self.__sensor_height = data['cameraSensorHeight']
                        self.__icx = data['iCx']
                        self.__icy = data['iCy']
                        self.__ratio = data['ratio']
                        self.__image_width = data['imageWidth']
                        self.__image_height = data['imageHeight']
                        self.__calibration_ratio = data['calibrationRatio']
                        self.__parameter_0 = data['parameter0']
                        self.__parameter_1 = data['parameter1']
                        self.__parameter_2 = data['parameter2']
                        self.__parameter_3 = data['parameter3']
                        self.__parameter_4 = data['parameter4']
                        self.__parameter_5 = data['parameter5']

                else:
                    warnings.warn("Please Check your parameter file. \n"
                                  "If inside the file has multiple camera parameter, typing the name of camera!!\n"
                                  "see detail documentation here https://github.com/perseverance-tech-tw/moildev\n"
                                  "or you can email to 'perseverance.tech.tw@gmail.com'")

    def __init_alpha_rho_table(self):
        """
        Create list for initial corresponding alpha to rho(height image).

        Returns:
            Initial alpha and rho table.
        """
        for i in range(1800):
            alpha = i / 10 * math.pi / 180
            self.__alpha_to_rho_table.append(
                (self.__parameter_0 * alpha * alpha * alpha * alpha * alpha * alpha +
                 self.__parameter_1 * alpha * alpha * alpha * alpha * alpha +
                 self.__parameter_2 * alpha * alpha * alpha * alpha +
                 self.__parameter_3 * alpha * alpha * alpha +
                 self.__parameter_4 * alpha * alpha +
                 self.__parameter_5 * alpha) * self.__calibration_ratio)
            i += 1

        i = 0
        index = 0
        while i < 1800:
            while index < self.__alpha_to_rho_table[i]:
                self.__rho_to_alpha_table.append(i)
                index += 1
            i += 1

        while index < 3600:
            self.__rho_to_alpha_table.append(i)
            index += 1

    def __import_moildev(self):
        """
        Create moildev instance from Moildev SDK share object library.

        Returns:
            Moildev object (private attribute for this class)
        """
        self.__create_maps()
        self.__moildev = MoilCV.MoilCV(
            self.__camera_name,
            self.__sensor_width,
            self.__sensor_height,
            self.__icx,
            self.__icy,
            self.__ratio,
            self.__image_width,
            self.__image_height,
            self.__calibration_ratio,
            self.__parameter_0,
            self.__parameter_1,
            self.__parameter_2,
            self.__parameter_3,
            self.__parameter_4,
            self.__parameter_5)

    def __create_maps(self):
        """
        Create Maps image from zeroes matrix.

        Returns:
            Zeroes matrix same size with original image.
        """
        self.__map_x = np.zeros((self.__image_height, self.__image_width), dtype=np.float32)
        self.__map_y = np.zeros((self.__image_height, self.__image_width), dtype=np.float32)
        size = self.__image_height, self.__image_width, 3
        self.__res = np.zeros(size, dtype=np.uint8)

    @classmethod
    def version(cls):
        """
        Showing the information of the version moildev library.

        Returns:
            Moildev version information
        """
        MoilCV.version()

    @property
    def camera_name(self):
        """
        Get camera name used.

        Returns:
            Camera name (string)
        """
        return self.__camera_name

    @property
    def camera_fov(self):
        """
        Get Field of View (FoV) from camera used.

        Returns:
            FoV camera (int)
        """
        return self.__camera_fov

    @property
    def icx(self):
        """
        Get center image x-axis from camera used.

        Returns:
            Image center X (int)
        """
        return self.__icx

    @property
    def icy(self):
        """
        Get center image y-axis from camera used.

        Returns:
            Image center Y(int)
        """
        if self.__icy is not None:
            return self.__icy

    @property
    def image_width(self):
        """
        Get the width of the image used.

        Returns:
            image width(int)
        """
        return self.__image_width

    @property
    def image_height(self):
        """
        Get the height of the image used.

        Returns:
            image height(int)
        """
        return self.__image_height

    @property
    def param_0(self):
        """
        Get the value of calibration parameter_0 from camera used.

        Returns:
            Parameter_0 (float)
        """
        return self.__parameter_0

    @property
    def param_1(self):
        """
        Get the value of calibration parameter_1 from camera used.

        Returns:
            Parameter_1 (float)
        """
        return self.__parameter_1

    @property
    def param_2(self):
        """
        Get the value of calibration parameter_2 from camera used.

        Returns:
            Parameter_2 (float)
        """
        return self.__parameter_2

    @property
    def param_3(self):
        """
        Get the value of calibration parameter_3 from camera used.

        Returns:
            Parameter_3 (float)
        """
        return self.__parameter_3

    @property
    def param_4(self):
        """
        Get the value of calibration parameter_4 from camera used.

        Returns:
            Parameter_4 (float)
        """
        return self.__parameter_4

    @property
    def param_5(self):
        """
        Get the value of calibration parameter_5 from camera used.

        Returns:
            Parameter_5 (float)
        """
        return self.__parameter_5

    def maps_anypoint_mode1(self, alpha, beta, zoom):
        """
        Generate a pair of X-Y Maps for the specified alpha, beta and zoom parameters,
        and then utilize the resulting X-Y Maps to remap the original fisheye image to the target angle image.
        This function has 2 mode to generate maps anypoint, mode 1 is for tube application and
        mode 2 usually for car application

        Args:
            alpha: value of zenith distance(float).
            beta: value of azimuthal distance based on cartography system(float)
            zoom: value of zoom(float)

        Returns:
            mapX: the mapping matrices X
            mapY: the mapping matrices Y

        .. code-block :: markdown

            please reference: https://github.com/perseverance-tech-tw/moildev
        """
        if beta < 0:
            beta = beta + 360
        if alpha < -110 or alpha > 110 or beta < 0 or beta > 360:
            alpha = 0
            beta = 0

        else:
            alpha = -110 if alpha < -110 else alpha
            alpha = 110 if alpha > 110 else alpha
            beta = 0 if beta < 0 else beta
            beta = 360 if beta > 360 else beta
        self.__moildev.AnypointM(self.__map_x, self.__map_y, alpha, beta, zoom)
        return self.__map_x, self.__map_y

    def maps_anypoint_mode2(self, pitch, yaw, roll, zoom):
        """
        Generate a pair of X-Y Maps for the specified pitch, yaw, and roll also zoom parameters,
        and then utilize the resulting X-Y Maps to remap the original fisheye image to the target image.

        Args:
            pitch: pitch rotation (from -110 to 110 degree)
            yaw: yaw rotation (from -110 to 110 degree)
            roll: roll rotation (from -110 to 110 degree)
            zoom: zoom scale (1 - 20)

        Returns:
            mapX: the mapping matrices X
            mapY: the mapping matrices Y
        """
        if pitch < - 110 or pitch > 110 or yaw < -110 or yaw > 110 or roll < -110 or roll > 110:
            pitch = 0
            yaw = 0
            roll = 0

        else:
            pitch = -110 if pitch < -110 else pitch
            pitch = 110 if pitch > 110 else pitch
            yaw = -110 if yaw < -110 else yaw
            yaw = 110 if yaw > 110 else yaw
            roll = 110 if roll > 110 else roll
            roll = 110 if roll > 110 else roll
        self.__moildev.AnypointCar(self.__map_x, self.__map_y, pitch, yaw, roll, zoom)
        return self.__map_x, self.__map_y

    def maps_panorama_tube(self, alpha_min, alpha_max):
        """
        To generate a pair of X-Y Maps for alpha within 0 ... alpha_max degree, the result X-Y Maps can be used later
        to generate a panorama image from the original fisheye image.

        Args:
            alpha_min: the minimum alpha degree given
            alpha_max: the maximum alpha degree given. The recommended value is half of camera FOV. For example, use
                        90 for a 180 degree fisheye images and use 110 for a 220 degree fisheye images.

        Returns:
            mapX: the mapping matrices X
            mapY: the mapping matrices Y

        .. code-block :: markdown

            please reference: https://github.com/perseverance-tech-tw/moildev
        """
        if alpha_min < 5:
            alpha_min = 5
        self.__moildev.PanoramaTube(self.__map_x, self.__map_y, alpha_min, alpha_max)
        return self.__map_x, self.__map_y

    def maps_panorama_car(self, alpha_max, iC_alpha_degree, iC_beta_degree, p_alpha_from, p_alpha_end):
        """
        To generate a pair of X-Y Maps for alpha within 0 alpha_max degree, the result X-Y Maps can be used later
        to generate a panorama image from the original fisheye image. The panorama image centered at the 3D
        direction with alpha = iC_alpha_degree and beta = iC_beta_degree.

        Args:
            alpha_max : max of alpha. The recommended value is half of camera FOV. For example, use
                        90 for a 180 degree fisheye images and use 110 for a 220 degree fisheye images.
            iC_alpha_degree : alpha angle of panorama center.
            iC_beta_degree : beta angle of panorama center.
            p_alpha_end:
            p_alpha_from:

        Returns:
            mapX
            mapY

        .. code-block :: markdown

            please reference: https://github.com/perseverance-tech-tw/moildev
        """
        self.__moildev.PanoramaCar(self.__map_x, self.__map_y, alpha_max, iC_alpha_degree,
                                   iC_beta_degree, p_alpha_from, p_alpha_end)
        return self.__map_x, self.__map_y

    def maps_panorama_rt(self, alpha_max, iC_alpha_degree, iC_beta_degree):
        """
        To generate a pair of X-Y Maps for alpha within 0..alpha_max degree, the result X-Y Maps can be used later
        to generate a panorama image from the original fisheye image. The panorama image centered at the 3D
        direction with alpha = iC_alpha_degree and beta = iC_beta_degree.

        Args:
            alpha_max : max of alpha. The recommended value is half of camera FOV. For example, use
                        90 for a 180 degree fisheye images and use 110 for a 220 degree fisheye images.
            iC_alpha_degree : alpha angle of panorama center.
            iC_beta_degree : beta angle of panorama center.

        Returns:
            mapX
            mapY

        .. code-block :: markdown

            please reference: https://github.com/perseverance-tech-tw/moildev
        """
        self.__moildev.PanoramaM_Rt(self.__map_x, self.__map_y, alpha_max, iC_alpha_degree, iC_beta_degree)
        return self.__map_x, self.__map_y

    def maps_recenter(self, alpha_max, beta_degree):
        """
        Create maps for reverse image. this can work using input panorama rotation image

        Args:
            alpha_max: max of alpha. The recommended value is half of camera FOV. For example, use
                        90 for a 180 degree fisheye images and use 110 for a 220 degree fisheye images.
            beta_degree : beta angle.

        Returns:
            maps_x_reverse, maps_y_reverse
        """
        self.__moildev.revPanoramaMaps(self.__map_x, self.__map_y, alpha_max, beta_degree)
        return self.__map_x, self.__map_y

    def anypoint_mode1(self, image, alpha, beta, zoom):
        """
        Generate anypoint view image. for mode 1, the result rotation is betaOffset degree rotation around the
        Z-axis(roll) after alphaOffset degree rotation around the X-axis(pitch). for mode 2, The result rotation
        is thetaY degree rotation around the Y-axis(yaw) after thetaX degree rotation around the X-axis(pitch).

        Args:
            image: source image given
            alpha: the alpha offset that corespondent to the pitch rotation
            beta: the beta offset that corespondent to the yaw rotation
            zoom: decimal zoom factor, normally 1..12
            mode: the mode view selected

        Returns:
            anypoint image

        .. code-block :: markdown

            please reference: https://github.com/perseverance-tech-tw/moildev
        """
        map_x, map_y = self.maps_anypoint_mode1(alpha, beta, zoom)
        image = cv2.remap(image, map_x, map_y, cv2.INTER_CUBIC)
        return image

    def anypoint_mode2(self, image, pitch, yaw, roll, zoom):
        """
        Generate anypoint view image. for mode 1, the result rotation is betaOffset degree rotation around the
        Z-axis(roll) after alphaOffset degree rotation around the X-axis(pitch). for mode 2, The result rotation
        is thetaY degree rotation around the Y-axis(yaw) after thetaX degree rotation around the X-axis(pitch).

        Args:
            image: source image given
            pitch: the alpha offset that corespondent to the pitch rotation
            yaw: the beta offset that corespondent to the yaw rotation
            roll: the beta offset that corespondent to the yaw rotation
            zoom: decimal zoom factor, normally 1..12


        Returns:
            anypoint image

        .. code-block :: markdown

            please reference: https://github.com/perseverance-tech-tw/moildev
        """
        map_x, map_y = self.maps_anypoint_mode2(pitch, yaw, roll, zoom)
        image = cv2.remap(image, map_x, map_y, cv2.INTER_CUBIC)
        return image

    def panorama_tube(self, image, alpha_min, alpha_max):
        """
        The panorama image

        Args:
            image: image source given
            alpha_min:
            alpha_max:

        Returns:
            Panorama view image

        .. code-block :: markdown

            please reference: https://github.com/perseverance-tech-tw/moildev
        """
        map_x, map_y = self.maps_panorama_tube(alpha_min, alpha_max)
        image = cv2.remap(image, map_x, map_y, cv2.INTER_CUBIC)
        return image

    def panorama_car(self, image, alpha_max, alpha, beta, left, right, top, bottom):
        """
        The function that generate a moil dash panorama image from fisheye camera.
        the image can control by alpha to change the pitch direction and beta for yaw direction.
        in order to select the roi, we can control by the parameter such as left, right, top, and bottom.

        Args:
            image: input fisheye image
            alpha_max:
            alpha: change the pitch direction(0 ~ 180)
            beta: change the yaw direction(-90 ~ 90)
            left: crop the left image by scale(0 ~ 1)
            right: crop the right image by scale(0 ~ 1)
            top: crop the top image by scale(0 ~ 1)
            bottom: crop the bottom image by scale(0 ~ 1)

        Returns:
            Panorama image
        """
        map_x, map_y = self.maps_panorama_car(alpha_max, alpha, beta, 0, 1)
        image = cv2.resize(cv2.remap(image, map_x, map_y, cv2.INTER_CUBIC),
                           (image.shape[1] * 2, image.shape[0]))
        image = image[round(image.shape[0] * (top + 0.3)):round(image.shape[0] * (top + 0.3)) +
                                                          round(image.shape[0] * (bottom - 0.3)),
                round(image.shape[1] * left):
                round(image.shape[1] * left) + round(image.shape[1] * (right - left))]

        return image

    def recenter(self, image, alpha_max, iC_alpha_degree, iC_beta_degree):
        """
        Change the optical point of fisheye image.

        Args:
            image: input image
            alpha_max: max of alpha. The recommended value is half of camera FOV. For example, use
                    90 for a 180 degree fisheye images and use 110 for a 220 degree fisheye images.
            iC_alpha_degree: alpha angle of panorama center
            iC_beta_degree: beta angle of panorama center

        Returns:
            reverse image
        """
        self.__moildev.PanoramaM_Rt(self.__map_x, self.__map_y, alpha_max, iC_alpha_degree, iC_beta_degree)
        result = cv2.remap(image, self.__map_x, self.__map_y, cv2.INTER_CUBIC)
        self.__moildev.revPanorama(result, self.__res, alpha_max, iC_beta_degree)
        return self.__res

    def get_alpha_from_rho(self, rho):
        """
        Get the alpha from rho image.

        Args:
            rho: the value of rho given

        Returns:
            alpha
        """
        if rho >= 0:
            return self.__rho_to_alpha_table[rho] / 10
        else:
            return -self.__rho_to_alpha_table[-rho] / 10

    def get_rho_from_alpha(self, alpha):
        """
        Get rho image from alpha given.

        Args:
            alpha: the value of alpha given

        Returns:
            rho image
        """
        return self.__alpha_to_rho_table[round(alpha * 10)]

    def get_alpha_beta(self, coordinateX, coordinateY, mode=1):
        """
        Get the alpha beta from specific coordinate image.

        Args:
            coordinateX:
            coordinateY:
            mode:

        Returns:
            alpha, beta (if you get none, the coordinate is out of range that can cover)

        .. code-block :: markdown

            please reference: https://github.com/perseverance-tech-tw/moildev
        """
        delta_x = coordinateX - self.__icx
        delta_y = -(coordinateY - self.__icy)
        range_left = coordinateX - (self.__icx - self.get_rho_from_alpha(110) - 4)
        range_right = self.image_width - (self.__icx - self.get_rho_from_alpha(110) + 4)
        if range_left >= 0 and coordinateX <= range_right:
            if mode == 1:
                r = round(math.sqrt(math.pow(delta_x, 2) + math.pow(delta_y, 2)))
                alpha = self.get_alpha_from_rho(r)
                if coordinateX == self.__icy:
                    angle = 0
                else:
                    angle = (math.atan2(delta_y, delta_x) * 180) / math.pi
                beta = 90 - angle
            else:
                alpha = self.get_alpha_from_rho(delta_y)
                beta = self.get_alpha_from_rho(delta_x)

        else:
            alpha, beta = None, None

        return alpha, beta

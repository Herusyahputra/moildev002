# Moildev Release-4.0
Moildev Library is a collection of functions support python to developments fisheye image applications.

============================================================================

## 1. How to install
There are two ways to use moildev. The first way is by visiting the moildev library, now available in the pypi 
distribution. The second way is cloning from GitHub repository.

```commandline
$ pip install Moildev
```
```commandline
$ git clone https://github.com/McutOIL/moildev.git
```

## 2. Import Library

import moildev library:

```
>> from moildev import Moildev
```

## 3. Application Programming Interface (API) Reference
### 3.1 Attention before create object
To create the object from Moildev, you have to provide the parameter. The camera parameter is the result from 
calibration camera by MOIL laboratory that will store on **.json** file.
```
moildev = Moildev("Camera_Parameter_Path")
```
**Parameter:**

Camera_Parameter_Path : The path of the *.json* file that stored the camera parameter from calibration result.

**Example:**
```
moildev = Moildev("camera_parameters.json", "entaniya")
```

**Load Image**
```commandline
image = cv2.imread("Image_Path in your computer")
```

### 3.2 Create anypoint maps mode 1
Purpose:

Generate a pair of X-Y Maps for the specified alpha, beta and zoom parameters,
and then utilize the resulting X-Y Maps to remap the original fisheye image to the target angle image.
This function has 2 mode to generate maps anypoint, mode 1 is for tube application and
mode 2 usually for car application.
```commandline
map_X, map_Y = moildev.maps_anypoint_mode1(alpha, beta, zoom)
```
Example
```commandline
map_X, map_Y = moildev.maps_anypoint_mode1(90, 180, 2)
anypoint_maps_m1 = cv2.remap(image, map_X, map_Y, cv2.INTER_CUBIC)
anypoint_maps_m1 = cv2.resize(anypoint_maps_m1, (400, 300))
cv2.imshow("anypoint maps mode 1", anypoint_maps_m1)
```

### 3.3 Create anypoint mode 1
Purpose:

Generate anypoint view image. for mode 1, the result rotation is betaOffset degree rotation around the
Z-axis(roll) after alphaOffset degree rotation around the X-axis(pitch). for mode 2, The result rotation
is thetaY degree rotation around the Y-axis(yaw) after thetaX degree rotation around the X-axis(pitch).

```commandline
anypoint_m1 = moildev.anypoint_mode1(image, alpha, beta, zoom)
```
Example
```commandline
anypoint_m1 = moildev.anypoint_mode1(image, 90, 180, 2)
anypoint_m1 = cv2.resize(anypoint_m1, (400, 300))
cv2.imshow("anypoint made 1", anypoint_m1)
```

### 3.4 Create anypoint maps mode 2
Purpose:

Generate a pair of X-Y Maps for the specified pitch, yaw, and roll also zoom parameters,
and then utilize the resulting X-Y Maps to remap the original fisheye image to the target image.
```commandline
map_X, map_Y = moildev.maps_anypoint_mode2(pitch, yaw, roll, zoom)
```
Example
```commandline
map_X, map_Y = moildev.maps_anypoint_mode2(-90, 0, 0, 2)
anypoint_maps_m2 = cv2.remap(image, map_X, map_Y, cv2.INTER_CUBIC)
anypoint_maps_m2 = cv2.resize(anypoint, (400, 300))
cv2.imshow("anypoint maps mode 2" anypoint_maps_m2)
```

### 3.5 Create anypoint mode 2
Purpose:

Generate anypoint view image. for mode 1, the result rotation is betaOffset degree rotation around the
Z-axis(roll) after alphaOffset degree rotation around the X-axis(pitch). for mode 2, The result rotation
is thetaY degree rotation around the Y-axis(yaw) after thetaX degree rotation around the X-axis(pitch).
```commandline
anypoint_m2 = moildev.anypoint_mode2(image, pitch, yaw, roll, zoom)
```
Example
```commandline
anypoint_m2 = moildev.anypoint_mode2(image, -90, 0, 0, 2)
anypoint_m2 = cv2.resize(anypoint_m2, (400, 300))
cv2.imshow("anypoint mode 2", anypoint_m2)
```

### 3.6 Create panorama tube
Purpose:

To create an image with a panoramic view
```commandline
panorama_tube = moildev.panorama_tube(image, alpha_min, alpha_max)
```
Example
```commandline
panorama_tube = moildev.panorama_tube(image, 10, 110)
panorama_tube = cv2.resize(panorama_tube, (400, 300))
cv2.imshow("panorama tube", panorama_tube)
```
### 3.7 Create panorama car
Purpose:

The function that generate a moil dash panorama image from fisheye camera.
the image can control by alpha to change the pitch direction and beta for yaw direction.
in order to select the roi, we can control by the parameter such as left, right, top, and bottom.

```commandline
panorama_car = moildev.panorama_car(image, alpha_max, alpha, beta, left, right, top, bottom)
```
Example
```commandline
panorama_car = moildev.panorama_car(image, 110, 80, 0, 0.25, 0.75, 0, 1)
panorama_car = cv2.resize(panorama_car, (400, 300))
cv2.imshow("panorama car", panorama_car) 
```

### 3.8 Create recenter
Purpose:

Function to change the optical point of the fisheye image.
```commandline
recenter = moildev(image, alpha_max, IC_alpha_degree, IC_beta_degree)
```
Example
```commandline
recenter = moildev.recenter(image, 110, 25, 10)
recenter = cv2.resize(recenter, (400, 300))
cv2.imshow("show recenter", recenter)
```


Ming-Chi Omni-directional, Surveillance, and Imaging laboratory (MOIL-Lab), Ming Chi University of Technology, Taiwan

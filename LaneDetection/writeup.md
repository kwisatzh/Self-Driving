

 ## Advanced Lane Finding Project

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./output_images/undistort_chess.png "Undistorted"
[image2]: ./output_images/undistort.png "Road Transformed"
[image3]: ./output_images/s_threshold_img "S-threshold result"
[image4]: ./output_images/sobel_combo "Sobel result"
[image5]: ./output_images/thresholded_combination_1.png "Binary output after thresholding"
[image6]: ./output_images/warped_test.png "Warp test example"
[image7]: ./output_images/fitted_lines_rectangles.png "Fitted lanes with ROC"
[image8]: ./output_images/output_test.png "Output"
[video1]: ./project_video.mp4 "Video"


---

### Writeup / README


### Camera Calibration


The code for this step is contained in the first code cell of the IPython notebook located in "./examples/example.ipynb".

I start by preparing "object points", which will be the (x, y, z) coordinates of the chessboard corners in the world. Here I am assuming the chessboard is fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image.  Thus, `objp` is just a replicated array of coordinates, and `objpoints` will be appended with a copy of it every time I successfully detect all chessboard corners in a test image.  `imgpoints` will be appended with the (x, y) pixel position of each of the corners in the image plane with each successful chessboard detection.  

I then used the output `objpoints` and `imgpoints` to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.  I applied this distortion correction to the test image using the `cv2.undistort()` function and obtained this result: 

![alt text][image1]

### Pipeline (single images)


To demonstrate this step, I will describe how I apply the distortion correction to one of the test images and the result is attached:
![alt text][image2]


I used a combination of color (HSV space, with the S-channel being thresholded) and gradient thresholds (using the Sobel operator) to generate a binary image (Steps 3.1, 3.2 in the example.ipy). I used the max threshold to produce a binary image. 
 
The output from thresholding in HSV space is as follows:
![alt text][image3]

The output from thresholding after applying the Sobel operator is as follows:
![alt text][image4]

The final binary output from thresholding after applying the Sobel operator is as follows:
![alt text][image5]




The code for my perspective transform includes a function called `perspective_transform()`, which appears in Step 4 of my IPython notebook `example.ipy`.  The function has hardcoded values for source (`src`) and destination (`dst`) points.  The following points were chosen, with the intention that this would be one-time affair, and then reused in the pipeline. These points were chosen by using the formula.

| Source        | Destination   | 
|:-------------:|:-------------:| 
| 325, 650      | 300, 670        | 
| 990, 650      | 1000, 670      |
| 420, 580     | 300, 600      |
| 880, 580      | 985, 600        |

I verified that my perspective transform was working as expected by drawing the `src` and `dst` points onto a test image and its warped counterpart to verify that the lines appear parallel in the warped image.

![alt text][image6]

#### Identifying lane pixels

The process to do this is in function find_lanes() and the helper function fit_poly_line() in Step 5.2, 5.3 in the IPython notebook. 
I used convolution. The basic idea is as follows: 
Given that we are operating on a binary image, we use a square window template and slide it across the image from left to right and then bottom to top, all the while summing any overlapping values. 
The peak of the convolved signal is where there was the highest overlap of pixels and the most likely position for the lane marker is, hence, we keep track of the maximum and store it for both the left and right lanes. Once the best points are chosen, we fit a 2nd order polynomial to form a line. In order to incorporate smoothing to ensure no sudden jumps, we keep track of the coefficients of the fitted polynomials for the respective lanes, and use an average to filter out noise. In addition, if there is a sudden change of values 
in coefficients, we also check for outliers by using standard deviations and rejecting any outlier cofficients that are beyond 1.3 standard deviations. These values are based on experimentation. 
 
The result can be seen in the test image:
 
![alt text][image7]

#### Calculate the radius of curvature of the lane and the position of the vehicle with respect to center.

The code for calucalting the ROC and is in the function find_lanes() in Step 5.3 of my IPython notebook. The code is utilized twice, once for the left lane, and once for the right lane. 

The final output image on the test is as follows: 

![alt text][image8]

---

### Pipeline (video)


Here's a [link to my video result](./examples/output_video.mp4)

---


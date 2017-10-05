##Writeup Template
###You can use this file as a template for your writeup if you want to submit it as a markdown file, but feel free to use some other method and submit a pdf if you prefer.

---

**Vehicle Detection Project**

The goals / steps of this project are the following:

* Perform a Histogram of Oriented Gradients (HOG) feature extraction on a labeled training set of images and train a classifier Linear SVM classifier
* Optionally, you can also apply a color transform and append binned color features, as well as histograms of color, to your HOG feature vector. 
* Note: for those first two steps don't forget to normalize your features and randomize a selection for training and testing.
* Implement a sliding-window technique and use your trained classifier to search for vehicles in images.
* Run your pipeline on a video stream (start with the test_video.mp4 and later implement on full project_video.mp4) and create a heat map of recurring detections frame by frame to reject outliers and follow detected vehicles.
* Estimate a bounding box for vehicles detected.

[//]: # (Image References)
[image1]: ./output_images/car_not_car.png
[image2]: ./output_images/classifier_output.png
[image3]: ./output_images/hog_subsampling.png
[image4]: ./examples/heatmap.png
[video1]: ./project_video.mp4

## [Rubric](https://review.udacity.com/#!/rubrics/513/view) Points
###Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---
###Writeup / README

####1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.  [Here](https://github.com/udacity/CarND-Vehicle-Detection/blob/master/writeup_template.md) is a template writeup for this project you can use as a guide and a starting point.  

You're reading it!

###Histogram of Oriented Gradients (HOG)

####1. Explain how (and identify where in your code) you extracted HOG features from the training images.

The code is provided in the IPython notebook solution.ipynb under the section: "HOG Extraction". Before performing the extraction, 
I started by reading in all the `vehicle` and `non-vehicle` images.  Here is an example of one of each of the `vehicle` and `non-vehicle` classes:

![alt text][image1]

I then explored different color spaces and different `skimage.hog()` parameters (`orientations`, `pixels_per_cell`, and `cells_per_block`).  The code I used was provided by Udacity.

####2. Explain how you settled on your final choice of HOG parameters.

I tried various combinations of parameters and ended up with color space: YUV, with pixels per channel to be 8, orientations to be 9, and cells per block to be 2. I used all HOG channels. These parameters were decided to give the best perofmance on the classifier, as well after consulting the forums. 

In addition to the HOG channels, I also used spatial binning of color as well as histograms of color as 
additional features. 

####3. Describe how (and identify where in your code) you trained a classifier using your selected HOG features (and color features if you used them).

The classifier is described in the section: "Create Classifier". I implemented the linear SVM as well as a Random Forest classifier (an ensemble) to explore if RFs can give better results. Indeed, Random Forests did provide a slightly better classifier accuracy on the test accuracy and that's what I ended up using. 

Upon experimentation, we decided to use HOG and spatial binning of color as features; histogram of colors didn't provide a better result. 

An example result is:

![alt text][image2]

###Sliding Window Search

####1. Describe how (and identify where in your code) you implemented a sliding window search.  How did you decide what scales to search and how much to overlap windows?

The sliding window search, which is based on HOG sub-sampling window search, is provided in HOG Subsampling window search section header as well as sliding windows section header. 
The scales as well as the overlap was decided after experimentation, as well as referring the forums for good parameters. 

####2. Show some examples of test images to demonstrate how your pipeline is working.  What did you do to optimize the performance of your classifier?

The final set of params were chosen to improve the accuracy of the classifier. The RF was giving a better accuracy than SVM Linear, so used that. The params were chosen after experimentation. 


![alt text][image2]


### Video Implementation

####1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (somewhat wobbly or unstable bounding boxes are ok as long as you are identifying the vehicles most of the time with minimal false positives.)
Here's a [link to my video result](./output_video.mp4)


####2. Describe how (and identify where in your code) you implemented some kind of filter for false positives and some method for combining overlapping bounding boxes.

I used the HOG Subsampling method to make the window search to be efficient. However, the output of the sampling led to
false-positives and duplicates like the following:

![alt text][image3]
 
In order to deal with these, I sued the heatmap method as provided in the lessons and is coded in the section:"Deal with duplicates and false positives". 

I recorded the positions of positive detections in each frame of the video.  From the positive detections I created a heatmap and then thresholded that map to identify vehicle positions, aiding in reducing false positives.  
I then used `scipy.ndimage.measurements.label()` to identify individual blobs in the heatmap.  I then assumed each blob corresponded to a vehicle and used that to detect duplicates.  I constructed bounding boxes to cover the area of each blob detected.  
Here's an example result showing the heatmap from an example image, using the labels and then creating the bounding boxes. 

![alt text][image4]



---

###Discussion

####1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

Most of the code for this project was taken from the provided code by Udacity, with some minor changes. 
The main challenge was to tune the different parameters. There were many false-positives, perhaps a better classifier could have helped. 

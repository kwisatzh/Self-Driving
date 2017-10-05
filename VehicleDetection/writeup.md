

## Vehicle Detection Project 

[//]: # (Image References)
[image1]: ./output_images/car_not_car.png
[image2]: ./output_images/classifier_output.png
[image3]: ./output_images/hog_subsampling.png
[image4]: ./examples/heatmap.png
[video1]: ./project_video.mp4


### Histogram of Oriented Gradients (HOG)

The code is provided in the IPython notebook solution.ipynb under the section: "HOG Extraction". Before performing the extraction, 
I started by reading in all the `vehicle` and `non-vehicle` images.  Here is an example of one of each of the `vehicle` and `non-vehicle` classes:

![alt text][image1]

I then explored different color spaces and different `skimage.hog()` parameters (`orientations`, `pixels_per_cell`, and `cells_per_block`).  

I tried various combinations of parameters and ended up with color space: YUV, with pixels per channel to be 8, orientations to be 9, and cells per block to be 2. I used all HOG channels. These parameters were decided to give the best perofmance on the classifier.

In addition to the HOG channels, I also used spatial binning of color as well as histograms of color as 
additional features. 

The classifier is described in the section: "Create Classifier". I implemented the linear SVM as well as a Random Forest classifier (an ensemble) to explore if RFs can give better results. Indeed, Random Forests did provide a slightly better classifier accuracy on the test accuracy and that's what I ended up using. 

Upon experimentation, we decided to use HOG and spatial binning of color as features; histogram of colors didn't provide a better result. 

An example result is:

![alt text][image2]


The sliding window search, which is based on HOG sub-sampling window search, is provided in HOG Subsampling window search section header as well as sliding windows section header. 
The scales as well as the overlap was decided after experimentation. 

The final set of params were chosen to improve the accuracy of the classifier. The RF was giving a better accuracy than SVM Linear, so used that. The params were chosen after experimentation. 


![alt text][image2]

Here's a [link to my video result](./output_video.mp4)


I used the HOG Subsampling method to make the window search to be efficient. However, the output of the sampling led to
false-positives and duplicates like the following:

![alt text][image3]
 
In order to deal with these, I used the heatmap method that is coded in the section:"Deal with duplicates and false positives". 

I recorded the positions of positive detections in each frame of the video.  From the positive detections I created a heatmap and then thresholded that map to identify vehicle positions, aiding in reducing false positives.  
I then used `scipy.ndimage.measurements.label()` to identify individual blobs in the heatmap.  I then assumed each blob corresponded to a vehicle and used that to detect duplicates.  I constructed bounding boxes to cover the area of each blob detected.  
Here's an example result showing the heatmap from an example image, using the labels and then creating the bounding boxes. 

![alt text][image4]


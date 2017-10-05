## Behavioral Cloning Project 

The goals / steps of this project are the following:
* Use the simulator to collect data of good driving behavior
* Build, a convolution neural network in Keras that predicts steering angles from images
* Train and validate the model with a training and validation set
* Test that the model successfully drives around track one without leaving the road




My project includes the following files:
* model.py containing the script to create and train the model
* drive.py for driving the car in autonomous mode
* model.h5 containing a trained convolution neural network 
* writeup_report.md summarizing the results

Using the provided simulator and my drive.py file, the car can be driven autonomously around the track by executing 
```sh
python drive.py model.h5
```


The model.py file contains the code for training and saving the convolution neural network. The file shows the pipeline I used for training and validating the model, and it contains comments to explain how the code works.

### Model Details

My model consists of a convolution neural network with 5x5 filter sizes and depths between 32 and 128 (model.py lines 88-93) 

The model includes RELU layers to introduce nonlinearity (code lines 88,90,92), and the data is normalized 
in the model using a Keras lambda layer (code line 85). In addition, I also cropped the images (code line 86) to get better results. 

The conv layers were followed by two dense layers, starting with size 200, then 100, and finally the last layer of size 1 that provides the output. The activation function RELU was used for the first two dense/full layers.

The model contains dropout layers in order to reduce overfitting (model.py lines 98, 100). The factor of 0.2 
was chosen as it gave the best performance.   

The model was trained and validated on different data sets to ensure that the model was not overfitting (data details follow). The model was tested by running it through the simulator and ensuring that the vehicle could stay on the track.
The model used an adam optimizer, so the learning rate was not tuned manually (model.py line 25).

Training data was chosen to keep the vehicle driving on the road. I used a combination of center lane driving, recovering from the left and right sides of the road as well as counter clock-wise driving. 
For details about how I created the training data, see the next section. 

### Model Architecture and Training Strategy

The overall strategy for deriving a model architecture was to first try out the simple LeNet model, and then increase complexity to improve perfomance. 

My first step was to use a convolution neural network with two conv layers and two full layers. However, I wasn't getting good driving performance. So in addition to improving the data (below), I added another conv layer.
Hence, the total number of conv layers are 3, with RELU activation to introduce non-linearity. 

In order to gauge how well the model was working, I split my image and steering angle data into a training and validation set. I found that few epochs did the job, with more epochs increasing the validation error. 

To combat the overfitting, I modified the model to include maxpooling and dropout layers. In addition, the data was also diverse. 

The final step was to run the simulator to see how well the car was driving around track one. There were a few spots where the vehicle fell off the track, and reading the forums, it was suggested that the input may be a problem; I was training on BGR data, whereas the output drive.py was operating on BGR image files. 
I did the BGR to RGB conversion, and started getting good results. 
At the end of the process, the vehicle is able to drive autonomously around the track without leaving the road.

#### Final Model Architecture

The final model architecture (model.py lines 88-101) consisted of a convolution neural network with the following layers and layer sizes:
Layer 1: 32 with filter 5x5, activation RELU
Layer 2: Max Pooling.
Layer 3: 64 with filter 5x5, activation RELU
Layer 4: Max Pooling
Layer 5: 128 with filter 5x5, activation RELU

Layer 6: Dense layer of size 200, activation RELU
Layer 7: Dropout layer
Layer 8: Dense layer of size 100, activation RELU
Layer 9: Dropout layer
Layer 10: Output Layer
####3. Creation of the Training Set & Training Process

To capture good driving behavior, I first recorded two laps on track one using center lane driving. 

I then recorded the vehicle driving counter-clockwise. 

To augment the data sat, I also flipped images and angles thinking that this would add mroe data points. 
I also filtered the images were the angle didn't change much. 

After the collection process, I had 11604 number of data points. 
I then preprocessed this data by normalizing and cropping. 
I finally randomly shuffled the data set and put 20% of the data into a validation set. 

I used this training data for training the model. The validation set helped determine if the model was over or under fitting. The ideal number of epochs was 3. I used an adam optimizer so that manually training the learning rate wasn't necessary.

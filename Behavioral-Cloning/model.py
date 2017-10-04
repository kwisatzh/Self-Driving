##Script to build model of steering angle, and using the model to predict
##Uses: Keras, openCV, numpy, csv
##Model: 3 Conv layers, followed by 3 dense layers
##
######
import csv
import cv2
import numpy as np
from keras.models import Sequential
from keras.layers import Flatten, Dense, Lambda, Cropping2D
from keras.layers import Convolution2D, Dropout
from keras.layers.pooling import MaxPooling2D

lines = []
images = []
measurements = []

#read in lines
with open('../driving_log.csv') as csvfile:
  reader = csv.reader(csvfile)
  for line in reader:
    lines.append(line)

# read in images, center as well as from left/right camera
# also perform data cleaning/pre-processing
for line in lines:
  source_path = line[0]
  filename = source_path.split('/')[-1]
  current_path = '../IMG/'+filename
  image = cv2.imread(current_path)
  image = image[:,:,::-1] ##input via imread is BGR, convert to RGB
  measurement = float(line[3])

  #with prob 2/3, discard data that corresponds to straight line
  if measurement > -0.001 and measurement < 0.001:
    if np.random.randint(0,3) is not 0:
      continue
  
  images.append(image)
  measurements.append(measurement)
  #augment data by flipping the center image and adding it
  images.append(cv2.flip(image,1))
  measurements.append(measurement*-1.0)

  # don't add data from left/right cameras if steering angle is too small
  if measurement > -0.001 and measurement < 0.001:
    continue

  #left
  source_path = line[1]
  filename = source_path.split('/')[-1]  
  current_path = '../IMG/'+filename
  image_left = cv2.imread(current_path)
  image_left = image_left[:,:,::-1]
  images.append(image_left)
  measurements.append(measurement-0.15)

  #right
  source_path = line[2]
  filename = source_path.split('/')[-1]  
  current_path = '../IMG/'+filename
  image_right = cv2.imread(current_path)
  image_right = image_right[:,:,::-1]
  images.append(image_right)
  measurements.append(measurement+0.15)


print("Number of images", len(images))
print("Image dimension", images[0].shape)

## Tried flipping the left/right images as well, but was getting poor results.
## Hence just flipped the center image (above, line 42)
augmented_images, augmented_measurements = [],[]
for image, measurement in zip(images,measurements):
  augmented_images.append(image)
  augmented_measurements.append(measurement)
  #augmented_images.append(cv2.flip(image,1))
  #augmented_measurements.append(measurement*-1.0)

#training data
X_train = np.array(augmented_images)
y_train = np.array(augmented_measurements)

#build model
model = Sequential()
#pre-process data via normalization and cropping
model.add(Lambda(lambda x:x/255.0-0.5, input_shape=(160,320,3)))
model.add(Cropping2D(cropping=((50,25), (0,0))))
#three conv layers
model.add(Convolution2D(32,5,5, activation="relu"))
model.add(MaxPooling2D())
model.add(Convolution2D(64,5,5, activation="relu"))
model.add(MaxPooling2D())
model.add(Convolution2D(128,5,5, activation="relu"))
model.add(MaxPooling2D())

#two full layers, with dropout 
model.add(Flatten())
model.add(Dense(200,activation="relu"))
model.add(Dropout(0.3))
model.add(Dense(100,activation="relu"))
model.add(Dropout(0.3))
model.add(Dense(1))

#use ADAM, and mse as loss function as this is regression
model.compile(loss = 'mse',optimizer = 'adam')
model.fit(X_train, y_train, batch_size=64, validation_split=0.2,shuffle=True,nb_epoch=3)

#save model
model.save('model.h5')


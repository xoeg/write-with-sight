---
layout: default
---

**The Challenge**: 
I saw a job position at Tobii, for an "Algorithm Developer", and while I have developed plenty of algorithms to process images and time series, I have never worked in computer vision. So I thought: what if I write my _cover letter_ by developing an algorithm that can track my eyesight to write letters down? After all, how hard could it be?

> TLDR: **Very hard**.

After 2 days of work, this is as far as I got:

![tobii_pp](/assets/tobii_pp.jpg)

# The Algorithm
I constrained myself to work for at most 2 days in this project. During the scoping phase I decided to divide the workflow into four parts:
1. **Scope**: Decide how the algorithm will work.
2. **Data**: Develop program to gather data.
3. **Model**: Use that data to train a neural network.
4. **Deployment**: Used the trained model to write letters. 

I iterated this process about 15 times until I settled on the following. 

## Scope
A quick online search for pixelated alphabets showed that I can write any letter in a grid of 5 rows and 4 columns:

![abc_pix](/assets/abc_pix.jpg)

Hence, I settled on a 5 x 4 grid.
The remaining task was to develop an algorithm that can track my eyesight and highlight or paint each cell. Therefore, I needed two things:
* An image of where I am looking at.
* A model that can recognize where I am looking at.

For the modelling part, I knew from the start that I was going to use a convolutional neural network (CNN), because they are very good at dealing with image classification. The main problem was that to train these models, one usually requires a large dataset. 

## Data
To gather the data I wrote the script called `wws_get_data.py`. 
I used wxPython to create a GUI which highlights a cell. 

![wws_get_data](/assets/wws_get_data.jpg)

Then upon clicking on the snap button it takes a picture and the highlighted cell changes location. 
Each picture taken was stored in a folder corresponding to the location of the highlighted cell.
In this way I could train the CNN later on. 

The picture taken was a snapshot from the webcam, but after many iterations, I found out that I could achieve the best accuracy in the model if the pictures only included my eyes. So, I developed a low cost technological device that helped me achieve the task:

![me_data](/assets/me_data.jpg)

I ended up takeing 620 pictures, 31 for each cell. 

## Model
I used TensorFlow to build and train the CNN you can see it in the jupyter notebook `train_model.ipynb`. Despite the seemingly huge dataset that I got, the loss and accuracy curves gave a clear indication of overfitting. I could have changed the model, or get more data, but it was a race against time, so I decided to proceed with a model that was accurate about 80% of the time. 

![curves](/assets/curves.jpg)

## Deployment 
The deployment takes place in the script called `wws_write.py`.
I again used wxPython to create a GUI which highlights a cell, the main difference is that this time it used the CNN to predict where I am looking at, based on the input from the camera. 

![vid_me](/assets/vid_me.gif)
![vid_b](/assets/vid_b.gif)

In the end, at least I managed to write this:

![tobii_pp](/assets/tobii_pp.jpg)

* * *
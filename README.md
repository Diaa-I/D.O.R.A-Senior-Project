<div align="center">
    <img src = 'public\utils\logo.png' width=100%>
</div>

# Dynamic Object Recognition and Annotation (DORA)

## Overview
Over the past few years, Artificial Intelligence (AI) has been used to solve different kinds of problems in many fields. Supervised learning requires data to be annotated manually. The manual annotation process is time-consuming and prone to error. Thus, there is a growing demand for automated annotation solutions that can accurately and efficiently label data. The project's objective is to develop a system that can automatically annotate images with high accuracy, speed, and efficiency, while also improving its performance through reinforcement learning.

We believe this project can significantly impact the field of semi-automated video annotation. By combining the strengths of object detection and reinforcement learning, our system can overcome the limitations of traditional annotation methods and provide a more efficient and effective solution.

## Project Summary

Our project is mainly about facilitating the annotation process, which is an essential part of any supervised learning process. This project will provide an easy-to-use web application that will make the annotation process much faster. The idea is to use a small part of the video to build an initial model which will be used to suggest the annotation of the following frames. The user will be able to accept or reject the suggested annotations by using reinforcement learning which will improve the model performance using the user feedback as well as retraining. The aim of the project is not to replace human annotators, but to significantly speed up their work.

## Installation
### `Step 1` - Clone the repository
```bash
git clone https://github.com/Diaa-I/Junior-Project.git
```
### `Step 2` - Cd in the repository
```bash
cd Junior-Project
```
### `Step 3` - Install requirements
```bash
pip install -r requirements.txt
npm install
pip install
```
### `Step 4` - Install MongoDB
```bash
Make sure to install MongoDB
```
### `Step 5` - Run the application
```bash
python app.py
```
### `Step 6` - Access the application

Open a web browser and navigate to [http://localhost:5000](http://localhost:5000)

## Libraries used
### Python:
os
shutil
sys
cv2
yaml
flask
natsort
flask_pymongo
json
bson
flask_cors
glob
Path

### Npm:
react
axios
react-router-dom
react-bootstrap
react-icons


## Contributors

- [Diaa Nasr](https://www.linkedin.com/in/diaa-nasr/)

- [Anas Khaled](https://www.linkedin.com/in/anaskhaled/)

- [Seba Al Mokdad](https://www.linkedin.com/in/seba-al-mokdad/)



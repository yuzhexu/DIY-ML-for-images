# DIY-ML-for-images
DIY Machine Learning is an easy-to-use REST API that allows users to easily train image classification models and create inference requests. This project was completed Spring 2024 for EC530 Software Engineering Principles @ Boston University.

# Features
This project showcases the following features:

  - User Authentication 
  - Upload/delete images
  - Train image classification models with Vision Transformer (ViT) model
  - Create inference requests
  - Get inference results
  - Relation database with PostgreSQL
  - Task queues with Redis

# Installation Instructions
### runing local
1. Prerequisites: PostgreSQL and Redis running on default ports, remeber replace database URL
2. Clone the repository `git clone https://github.com/yuzhexu/DIY-ML-for-images.git`
3. `cd` into the repo, create and activate a virtual environment, and run `python3 -m pip install -r requirements.txt`
4. Start the actual API-serving Flask app with `python3 run.py`
5. Start a (or maore) Redis worker(s) with `python3 worker.py`
6. See <a href =https://app.swaggerhub.com/apis/YuzheXu/DIY_ML_api/1.0 target="_blank"> API documentation</a>for usage.
### install and run by docker
1. Simply pull the image from docker `docker pull yuzhexu/flask_app:1.0.0`
2. if pulled image, run `docker run -p 5000:5000 yuzhexu/flask_app:1.0.0`
3. if clone from github, run `docker compose up --build`, no need `--build` if already have image
4. See <a href =https://app.swaggerhub.com/apis/YuzheXu/DIY_ML_api/1.0 target="_blank"> API documentation</a>for usage.
# Demos
- Task Queue Implementation

![截屏2024-05-04 下午4 57 53](https://github.com/yuzhexu/DIY-ML-for-images/assets/112592362/581432ca-a2e7-4227-b7b8-4f3089252405)

- Containerization
  
<img width="1264" alt="截屏2024-05-04 下午4 57 14" src="https://github.com/yuzhexu/DIY-ML-for-images/assets/112592362/e0ae1d8e-1f16-4e65-a6e1-6c8bcc75e5c2">

# Models
check swagger under /app/schema/api swagger

<img width="646" alt="截屏2024-03-06 下午7 13 07" src="https://github.com/yuzhexu/DIY-ML-for-images/assets/112592362/e7b77182-2220-451a-b327-9dff063a598d">

# database schema
![98405cae-dc70-48df-8a20-5f3d7e25e262](https://github.com/yuzhexu/DIY-ML-for-images/assets/112592362/74d3d200-6657-401f-879e-2ba1f9e49f9f)

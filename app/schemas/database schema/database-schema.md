
1.Users

user_id (Primary Key, Integer, Auto-Increment)
username (VARCHAR, Unique)
email (VARCHAR, Unique)
password_hash (VARCHAR)

2.Projects

project_id (Primary Key, Integer, Auto-Increment)
user_id (Foreign Key, Integer, references Users)
name (VARCHAR)
type (VARCHAR) - e.g., "Image Classification", "Object Detection"
created_at (TIMESTAMP)
updated_at (TIMESTAMP)

3.DataUploads

upload_id (Primary Key, Integer, Auto-Increment)
project_id (Foreign Key, Integer, references Projects)
filename (VARCHAR)
upload_date (TIMESTAMP)
Labels

label_id (Primary Key, Integer, Auto-Increment)
upload_id (Foreign Key, Integer, references DataUploads)
label (VARCHAR)

4.TrainingSessions

session_id (Primary Key, Integer, Auto-Increment)
project_id (Foreign Key, Integer, references Projects)
status (VARCHAR) - e.g., "Pending", "Completed"
start_time (TIMESTAMP)
end_time (TIMESTAMP)
parameters (JSON) - Stores configurable parameters for training

5.TrainingStats

stats_id (Primary Key, Integer, Auto-Increment)
session_id (Foreign Key, Integer, references TrainingSessions)
accuracy (FLOAT)
loss (FLOAT)
other_metrics (JSON) - Can store additional metrics like precision, recall


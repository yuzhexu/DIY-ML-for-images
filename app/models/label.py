from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Label(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=False)
    label_name = db.Column(db.String(255), nullable=False)
    # 其他与标签相关的字段

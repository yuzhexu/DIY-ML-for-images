from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'  # 确保这与数据库中的表名匹配

    userid = db.Column(db.Integer, primary_key=True)  # 修改此行
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    passwordhash = db.Column(db.String(256))  # 也建议修改此行以符合 Python 的命名习惯


    def set_password(self, password):

        self.passwordhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passwordhash, password)
    def get_id(self):
        return str(self.userid)  # Ensure this returns a string

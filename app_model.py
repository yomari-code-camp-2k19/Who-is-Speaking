from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class features(db.Model):
    __tablename__ = 'features'

    uid = db.Column(db.Integer, primary_key=True)
    contact_name = db.Column(db.String(100))
    contact_number = db.Column(db.BigInteger, unique=True, nullable=False)
    mfcc_path = db.Column(db.Text())
    # audio_path = db.Column(db.Text(100))

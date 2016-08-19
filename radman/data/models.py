from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

db = SQLAlchemy()

class Instance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sop_iuid = db.Column(db.String(255),unique=True)
    sop_ciuid = db.Column(db.String(255))
    filepath = db.Column(db.String(255))
    number = db.Column(db.Integer)
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'))
    series = db.relationship('Series',
                             backref=db.backref('instances', lazy='joined'))

    def __init__(self, sop_iuid, sop_ciuid, number):
        self.sop_iuid = sop_iuid
        self.sop_ciuid = sop_ciuid
        self.number = number

    def __repr__(self):
        return '<Instance %r>' % (self.id)

class Series(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    iuid = db.Column(db.String(255),unique=True)
    number = db.Column(db.Integer)
    description = db.Column(db.String(255))
    modality = db.Column(db.String(255))
    station_name = db.Column(db.String(255))
    performing_physician = db.Column(db.String(255))
    study_id = db.Column(db.Integer, db.ForeignKey('study.id'))
    study = db.relationship('Study',
                             backref=db.backref('series', lazy='joined'))

    def __init__(self, iuid, study, number=None, description=None,
                 modality=None,station_name=None,performing_physician=None):
        self.iuid = iuid
        self.study = study
        self.number = number
        self.description = description
        self.modality = modality
        self.station_name = station_name
        self.performing_physician = performing_physician

    def __repr__(self):
        return '<Series %r>' % (self.id)


class Study(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    iuid = db.Column(db.String(255), unique=True)
    datetime = db.Column(db.DateTime)
    description = db.Column(db.String(255))
    accession_number = db.Column(db.String(255))
    study_id=db.Column(db.String(255))
    patient_id=db.Column(db.String(255))
    patient_name=db.Column(db.String(255))
    referring_physician=db.Column(db.String(255))

    def __init__(self, iuid, datetime, description=None, accession_number=None,study_id=None,
                 patient_id=None,patient_name=None,referring_physician=None):
        self.iuid = iuid
        self.datetime = datetime
        self.description = description
        self.accession_number = accession_number
        self.study_id = study_id
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.referring_physician = referring_physician

    def __repr__(self):
        return '<Study %r>' % (self.id)


roles_users = db.Table('roles_users', \
db.Column('user_id', db.Integer(), db.ForeignKey('user.id')), \
db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Role %r>' % (self.name)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __init__(self, email, password, active, roles):
        self.email = email
        self.password = password
        self.active = active
        self.roles = roles

    def __repr__(self):
        return '<User %r>' % (self.email)

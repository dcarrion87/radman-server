from radman import app
from radman.data.models import db, Study, Series, Instance
from flask_security.utils import encrypt_password
import datetime


def create_roles(data_store):
    data_store.create_role(name='admin')
    data_store.commit()


def create_study_series_instance(db):
    study1 = Study('1.2.1',datetime.datetime.now())
    study2 = Study('1.2.2', datetime.datetime.now())
    study3 = Study('1.2.3', datetime.datetime.now())
    series1 = Series('1.2.3.1',study1)
    series2 = Series('1.2.3.2', study2)
    series3 = Series('1.2.3.3', study3)
    instance1 = Instance('1.2.3.4.1',series1,'1.2.3.4', 1)
    instance2 = Instance('1.2.3.4.2',series1,'1.2.3.4', 1)
    instance3 = Instance('1.2.3.4.3',series1,'1.2.3.4', 1)
    instance4 = Instance('1.2.3.4.4',series2,'1.2.3.4', 1)
    instance5 = Instance('1.2.3.4.5',series2,'1.2.3.4', 1)
    instance6 = Instance('1.2.3.4.6',series2,'1.2.3.4', 1)
    instance7 = Instance('1.2.3.4.7',series3,'1.2.3.4', 1)
    instance8 = Instance('1.2.3.4.8',series3,'1.2.3.4', 1)
    instance9 = Instance('1.2.3.4.9',series3,'1.2.3.4', 1)
    db.session.add(study1)
    db.session.add(study2)
    db.session.add(study3)
    db.session.add(series1)
    db.session.add(series2)
    db.session.add(series3)
    db.session.add(instance1)
    db.session.add(instance2)
    db.session.add(instance3)
    db.session.add(instance4)
    db.session.add(instance5)
    db.session.add(instance6)
    db.session.add(instance7)
    db.session.add(instance8)
    db.session.add(instance9)
    db.session.commit()


def create_users(data_store):
    users = [('admin@test.com', 'admin', 'Password1', ['admin'], True)]
    for user in users:
        email = user[0]
        username = user[1]
        password = user[2]
        is_active = user[4]
        if password is not None:
            password = encrypt_password(password)
        roles = [data_store.find_or_create_role(rn) for rn in user[3]]
        data_store.commit()
        user = data_store.create_user(email=email, password=password, active=is_active)
        data_store.commit()
        for role in roles:
            data_store.add_role_to_user(user, role)
        data_store.commit()

data_store = app.security.datastore
with app.app_context():
    db.drop_all()
    db.create_all()
    create_roles(data_store)
    create_users(data_store)
    create_study_series_instance(db)

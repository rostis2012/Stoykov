"""
Making html page from DB
"""
from flask import Flask, render_template, abort
from peewee import *
from playhouse.shortcuts import model_to_dict


DB_NAME = 'people.db'

app = Flask(__name__)
db = SqliteDatabase(DB_NAME)
db.connect()


class BaseModel(Model):
    class Meta:
        database = db


class PersonModel(BaseModel):
    crew_id = CharField()
    name = CharField()


class EnterModel(BaseModel):
    person = ForeignKeyField(PersonModel)
    date = CharField()
    time = CharField()


class ExitModel(BaseModel):
    person = ForeignKeyField(PersonModel)
    date = CharField()
    time = CharField()


def get_data(person_id: str) -> dict:
    """
    Print person data from db
    :param person_id: str
    :return: None
    """
    persons = PersonModel.select().where(PersonModel.crew_id == person_id)
    temp_list = []
    for person_obj in persons:
        date_time_dict = {}
        for enter_date in person_obj.entermodel_set.select():
            enter_dict = model_to_dict(enter_date, recurse=False)
            for exit_date in person_obj.exitmodel_set.select():
                exit_dict = model_to_dict(exit_date, recurse=False)
                if enter_dict.get('id') != exit_dict.get('id'):
                    continue
                if date_time_dict.get(enter_dict.get("date")) is None:
                    temp_list.clear()
                temp_list.append([enter_dict.get("time"), exit_dict.get("time")])
                date_time_dict[enter_dict.get("date")] = temp_list
                break
        return date_time_dict


# url
@app.route('/persons/')
def index():
    persons = [person for person in PersonModel.select()]
    return render_template('persons.html', persons=persons)


@app.route('/persons/<person_id>')
def person_date_info(person_id):
    res = PersonModel.select().where(PersonModel.id == person_id)
    if len(res) != 1:
        abort(404)
    person = res[0]
    visits = list(get_data(person.crew_id).items())
    person_ = {
        'name': person.name,
        'crew_id': person.crew_id,
        'visits': visits
    }
    return render_template('person_profile.html', person=person_)
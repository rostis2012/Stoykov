"""
Making dictionary stuff entrance / exit
"""
from pathlib import Path
from peewee import *
from pprint import pprint
from playhouse.shortcuts import model_to_dict

PATH = "data"

CREW_FILENAME = 'crew.txt'
ENTRANCE_FILENAME = 'entrance.log'
EXIT_FILENAME = 'exit.log'

db = SqliteDatabase('people.db')


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


def read_files(path: str) -> tuple:
    """
    Read and write files to variables
    :param path: str
    :return: tuple
    """
    path = Path(Path.cwd().parent.parent, PATH)

    try:
        with open(path / CREW_FILENAME) as cf, \
                open(path / ENTRANCE_FILENAME) as enf, \
                open(path / EXIT_FILENAME) as exf:
            crew = cf.readlines()
            enter = enf.readlines()
            exit_ = exf.readlines()
    except:
        raise FileNotFoundError(f'Got a wrong path "{path}"!')
    return crew, enter, exit_


def parsing_data_to_dict(data_to_parsing: list) -> dict:
    """
    Format receiving data to dict
    :param data_to_parsing: list
    :return: dict
    """
    parsed_data_to_dict = {**dict(tuple(filter(None, map(str.strip, str(item).split('|')))
                                        for item in data_to_parsing))}
    return parsed_data_to_dict


def db_datatime_feel(data: list, key_id: str, ModelDb: object, person_obj: object) -> None:
    """
    Feel db from received value
    :param data: list
    :param key_id: str
    :param ModelDb: db object
    :param person_obj: db object
    :return: None
    """
    for item in data:
        for key, value in parsing_data_to_dict([item]).items():
            if key == key_id:
                date, time = value.split()
                ModelDb.create(person=person_obj, date=date, time=time)


def get_data(person_id: str) -> dict:
    """
    Print person data from db
    :param person_id: str
    :return: dict
    """
    db.connect()
    if person_id:
        persons = PersonModel.select().where(PersonModel.crew_id == person_id)
    else:
        persons = PersonModel.select()
    temp_list = []
    for person_obj in persons:
        pprint(model_to_dict(person_obj))
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
    db.close()
    return date_time_dict



def main(path: str) -> bool:
    """
    Parsing data and save to db if db not exist
    :param path: str
    :return: bool
    """
    if not isinstance(path, str):
        raise TypeError(f'Got {type(path)}, expected string')

    if not Path('people.db').is_file():
        db.connect()
        db.create_tables([PersonModel, EnterModel, ExitModel])
        print(f'create db_file')
        with db.atomic():
            crew, enter, exit = read_files(PATH)
            for person in crew:
                for key, value in parsing_data_to_dict([person]).items():
                    person_obj = PersonModel.create(crew_id=key, name=value)
                    db_datatime_feel(enter, key, EnterModel, person_obj)
                    db_datatime_feel(exit, key, ExitModel, person_obj)
        db.close()
        return False
    else:
        print(f'db_file is exist')
        return True


if __name__ == '__main__':
    if main(PATH):
        pprint(get_data('052XL7D4'))

"""
SELECT pm.*, emm.datetime as enter_time, exm.datetime as exit_time
FROM `personmodel` as pm
JOIN `entermodel` as emm ON emm.person_id = pm.id
JOIN `exitmodel` as exm ON exm.person_id = pm.id # exm.id = emm.id при такому запису виводить коректно, але не ясно чи можна так
WHERE pm.crew_id = "052XL7D4"
"""

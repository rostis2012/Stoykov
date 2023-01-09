"""
Створення словника входу / вихіду персоналу
"""
import pathlib

from pprint import pprint

PATH = '../data'

CREW_FILENAME = 'crew.txt'
ENTRANCE_FILENAME = 'entrance.log'
EXIT_FILENAME = 'exit.log'


def read_files(path: str) -> tuple:
    """
    Функція читання файлів у змінні
    :param path: str
    :return: tuple
    """
    path = pathlib.Path(path).resolve()
    with open(path / CREW_FILENAME) as cf, \
            open(path / ENTRANCE_FILENAME) as enf, \
            open(path / EXIT_FILENAME) as exf:
        crew = cf.readlines()
        enter = enf.readlines()
        exit_ = exf.readlines()
    return crew, enter, exit_


def made_person_info(person_id: str, entranse: list, exit: list) -> dict:
    """
    Функція створює словник з даних входу та виходу для отриманого ID
    :param person_id: str
    :param entranse: list
    :param exit: list
    :return: dict
    """
    visiter_dic = {}
    _temp = zip(entranse, exit)
    for in_, out in _temp:
        id_into_in, date_into_in, time_into_in = in_
        id_into_out, date_into_out, time_into_out = out

        if id_into_in != person_id:
            continue
        _time_in_out = [time_into_in, time_into_out]

        if visiter_dic.get(date_into_in) is None:
            visiter_dic.update({date_into_in: [_time_in_out]})
        else:
            visiter_dic[date_into_in].append(_time_in_out)
    return visiter_dic


def main(path: str) -> dict:
    """
    Парсінг даніх та збереження у словник
    :param path:
    :return: dict
    """
    res = {}
    crew, enter, exit_ = read_files(path)
    parsed_crew_data = {**dict(tuple(map(str.strip, str(item).split('|')) for item in crew))}
    parsed_enter_data = \
        sorted([*(tuple((filter(None, map(str.strip, item.replace('|', '').split())))) for item in enter)])
    parsed_exit_data = \
        sorted([*(tuple(filter(None, map(str.strip, item.replace('|', '').split()))) for item in exit_)])

    for person_id, name in parsed_crew_data.items():
        res.update({
            person_id: {
                'name': name,
                'visits': made_person_info(person_id, parsed_enter_data, parsed_exit_data)
            }
        })
    return res


if __name__ == '__main__':
    pprint(main(PATH), width=100)

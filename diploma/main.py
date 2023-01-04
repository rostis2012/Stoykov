"""
Створення словника входу / вихіду персоналу
"""
import pathlib

PATH = '../data'

CREW_FILENAME = 'crew.txt'
ENTRANCE_FILENAME = 'entrance.log'
EXIT_FILENAME = 'exit.log'


def read_files(path: str) -> tuple:
    """
    Читання файлів у змінні
    :param path:
    :return: tuple
    """
    path = pathlib.Path(path)
    with open(path / CREW_FILENAME) as cf, \
            open(path / ENTRANCE_FILENAME) as enf, \
            open(path / EXIT_FILENAME) as exf:
        crew = cf.readlines()
        enter = enf.readlines()
        exit_ = exf.readlines()
    return crew, enter, exit_


def main(path: str) -> dict:
    """
    Парсінг даніх та збереження у словник
    :param path:
    :return: dict
    """
    res = {}
    crew, enter, exit_ = read_files(path)

    for values in crew:
        dict_visit = {}
        id_, fio_ = values.strip().split(' | ')
        res[id_] = {"name": fio_, "visits": dict_visit}
        vhod_1 = []
        vhod_2 = []

        for ent_ in enter:
            ent_id, date_time_in = ent_.strip().split(' | ')
            date, time_in = str(date_time_in).split()
            if ent_id == id_:
                if dict_visit.get(date) is None:
                    vhod_1 = []
                    vhod_2 = []
                    vhod_1.append(time_in)
                    dict_visit[date] = [vhod_1, vhod_2]
                else:
                    vhod_2.append(time_in)
                    dict_visit[date] = [vhod_1, vhod_2]
                    _switch = True

                    for ex_ in exit_:
                        ex_id, date_time_ex = ex_.strip().split(' | ')
                        date_ex, time_ex = str(date_time_ex).split()
                        if ex_id == id_:
                            if date_ex == date:
                                if _switch:
                                    vhod_1.append(time_ex)
                                    _switch = False
                                else:
                                    vhod_2.append(time_ex)
    return res


if __name__ == '__main__':
    from pprint import pprint

    pprint(main(PATH), width=100)

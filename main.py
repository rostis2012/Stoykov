"""
Making dictionary stuff entrance / exit
"""
import pathlib

from pprint import pprint

PATH = '../data'

CREW_FILENAME = 'crew.txt'
ENTRANCE_FILENAME = 'entrance.log'
EXIT_FILENAME = 'exit.log'


def read_files(path: str) -> tuple:
    """
    Read and write files to variables
    :param path: str
    :return: tuple
    """
    path = pathlib.Path(path).resolve()
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


def parsing_data_to_list(data_to_parsing: list) -> list:
    """
    Format and sort receiving data to dict
    :param data_to_parsing: list
    :return: list
    """
    parsed_data_to_list = list(filter(None, ((tuple(map(str.strip, item.replace('|', '').split()))
                                              for item in data_to_parsing))))
    return sorted(parsed_data_to_list)


def make_person_info(person_id: str, entranse: list, exit: list) -> dict:
    """
    Make entrance / exit dict for received ID
    :param person_id: str
    :param entranse: list
    :param exit: list
    :return: dict
    """
    visiter_dic = {}
    for (id_into_in, date_into_in, time_into_in), (id_into_out, date_into_out, time_into_out) in zip(entranse, exit):
        if id_into_in != person_id:
            continue
        time_in_out = [time_into_in, time_into_out]
        if visiter_dic.get(date_into_in) is None:
            visiter_dic.update({date_into_in: [time_in_out]})
        else:
            visiter_dic[date_into_in].append(time_in_out)
    return visiter_dic


def main(path: str) -> dict:
    """
    Parsing data and save to dict
    :param path:
    :return: dict
    """
    if not isinstance(path, str):
        raise TypeError(f'Got {type(path)}, expected string')
    res = {}
    crew, enter, exit_ = read_files(path)
    parsed_crew_data = parsing_data_to_dict(crew)
    parsed_enter_data = parsing_data_to_list(enter)
    parsed_exit_data = parsing_data_to_list(exit_)

    for person_id, name in parsed_crew_data.items():
        res.update({
            person_id: {
                'name': name,
                'visits': make_person_info(person_id, parsed_enter_data, parsed_exit_data)
            }
        })
    return res


if __name__ == '__main__':
    pprint(main(PATH), width=100)

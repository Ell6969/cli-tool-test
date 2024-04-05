#!/usr/bin/env python3
import json

import itertools
import fire
import requests
from typing import Dict, List, Tuple
from packaging.version import parse
import pprint

URL = "https://rdb.altlinux.org/api"

branch_sisi = [{'name': 'i586-zlib-devel-static', 'epoch': 0, 'version': '1.3.1', 'release': 'alt1', 'arch': 'x86_64-i586', 'disttag': 'sisyphus+342532.100.1.1', 'buildtime': 1710232619, 'source': ''}, {'name': 'i586-zlib-ng-devel', 'epoch': 0, 'version': '2.1.6', 'release': 'alt1', 'arch': 'x86_64-i586', 'disttag': 'sisyphus+338936.100.1.1', 'buildtime': 1706169829, 'source': ''}, {'name': 'i586-zlib-ng-devel-static', 'epoch': 0, 'version': '2.1.6', 'release': 'alt1', 'arch': 'x86_64-i586', 'disttag': 'sisyphus+338936.100.1.1', 'buildtime': 1706169831, 'source': ''}, {'name': 'i586-zmusic-devel', 'epoch': 0, 'version': '1.1.12', 'release': 'alt1', 'arch': 'x86_64-i586', 'disttag': 'sisyphus+324576.100.1.1', 'buildtime': 1688980650, 'source': ''}, {'name': 'i586-zsh', 'epoch': 1, 'version': '5.9', 'release': 'alt2', 'arch': 'x86_64-i586', 'disttag': 'sisyphus+327286.6500.14.1', 'buildtime': 1711550531, 'source': ''}, {'name': 'i586-zyn-fusion', 'epoch': 0, 'version': '3.0.6', 'release': 'alt3', 'arch': 'x86_64-i586', 'disttag': 'sisyphus+343228.100.1.1', 'buildtime': 1711009644, 'source': ''}, {'name': 'i586-zynaddsubfx', 'epoch': 0, 'version': '3.0.6', 'release': 'alt4', 'arch': 'x86_64-i586', 'disttag': 'sisyphus+328262.100.1.1', 'buildtime': 1693393020, 'source': ''}, {'name': 'i586-zziplib', 'epoch': 0, 'version': '0.13.72', 'release': 'alt1', 'arch': 'x86_64-i586', 'disttag': 'sisyphus+278032.100.1.2', 'buildtime': 1625982255, 'source': ''}, {'name': 'i586-zziplib-devel', 'epoch': 0, 'version': '0.13.72', 'release': 'alt1', 'arch': 'x86_64-i586', 'disttag': 'sisyphus+278032.100.1.2', 'buildtime': 1625982256, 'source': ''}, {'name': 'i586-zzuf', 'epoch': 0, 'version': '0.15', 'release': 'alt1_10', 'arch': 'x86_64-i586', 'disttag': 'sisyphus+225100.100.1.1', 'buildtime': 1552687303, 'source': ''}]
branch_p10 = [{'name': 'i586-zathura-djvu', 'epoch': 0, 'version': '0.2.9', 'release': 'alt1', 'arch': 'x86_64-i586', 'disttag': 'sisyphus+244005.300.1.3', 'buildtime': 1578594339, 'source': ''}, {'name': 'i586-zathura-pdf-poppler', 'epoch': 0, 'version': '0.3.0', 'release': 'alt1', 'arch': 'x86_64-i586', 'disttag': 'sisyphus+244005.400.1.3', 'buildtime': 1578594341, 'source': ''}, {'name': 'i586-zathura-ps', 'epoch': 0, 'version': '0.2.7', 'release': 'alt1', 'arch': 'x86_64-i586', 'disttag': 'sisyphus+278951.400.1.2', 'buildtime': 1626302661, 'source': ''}, {'name': 'i586-zchunk-devel', 'epoch': 0, 'version': '1.1.15', 'release': 'alt1_1', 'arch': 'x86_64-i586', 'disttag': 'sisyphus+278120.100.1.1', 'buildtime': 1626030287, 'source': ''}, {'name': 'i586-zchunk-libs', 'epoch': 0, 'version': '1.1.15', 'release': 'alt1_1', 'arch': 'x86_64-i586', 'disttag': 'sisyphus+278120.100.1.1', 'buildtime': 1626030289, 'source': ''}, {'name': 'i586-zinnia-perl', 'epoch': 0, 'version': '0.06', 'release': 'alt1_60', 'arch': 'x86_64-i586', 'disttag': 'p10+323904.340.7.1', 'buildtime': 1689695494, 'source': ''}, {'name': 'i586-zint', 'epoch': 0, 'version': '2.9.1', 'release': 'alt2', 'arch': 'x86_64-i586', 'disttag': 'sisyphus+277670.100.1.1', 'buildtime': 1625735340, 'source': ''}, {'name': 'i586-zint-devel', 'epoch': 0, 'version': '2.9.1', 'release': 'alt2', 'arch': 'x86_64-i586', 'disttag': 'sisyphus+277670.100.1.1', 'buildtime': 1625735342, 'source': ''}, {'name': 'i586-zint-qt', 'epoch': 0, 'version': '2.9.1', 'release': 'alt2', 'arch': 'x86_64-i586', 'disttag': 'sisyphus+277670.100.1.1', 'buildtime': 1625735344, 'source': ''}, {'name': 'i586-zint-qt-devel', 'epoch': 0, 'version': '2.9.1', 'release': 'alt2', 'arch': 'x86_64-i586', 'disttag': 'sisyphus+277670.100.1.1', 'buildtime': 1625735345, 'source': ''}, {'name': 'i586-zipios++', 'epoch': 0, 'version': '0.1.5.9', 'release': 'alt2_20', 'arch': 'x86_64-i586', 'disttag': '', 'buildtime': 1527355679, 'source': ''}]
br = {
    "sisyphus": branch_sisi,
    "p10": branch_p10,
}
print(
    f'{len(br["sisyphus"])} sisy, "\n" {len(br["p10"])} p10'
)

class MyJsonerCompare:
    """
    делает сравнение полученных списков пакетов и выводит JSON (структуру нужно придумать),
    в котором будет отображено:
    - все пакеты, которые есть в p10 но нет в sisyphus                -> zad_1
    - все пакеты, которые есть в sisyphus но их нет в p10             -> zad_2
    - все пакеты, version-release которых больше в sisyphus чем в p10 -> zad_3

    __json_structure = {'branch': {
        'max_version': '0.0.0',
        'arch': {
            'pack': [],
        }
    }
    }
    """

    def __init__(self, packeges: Dict[str, List[Dict]]):
        self.packeges = packeges
        self.__json_structure = {}
        self.__arch = []
        self.__prepare_json_structure(packeges)

    @staticmethod
    def compare_version(version_1: str, version_2: str):
        """
        Compare two version and return True if version_1 > version_2
        """
        ver_1 = parse(version_1)
        ver_2 = parse(version_2)
        return ver_1 > ver_2

    def __prepare_json_structure(self, packeges: Dict[str, List[Dict]]) -> None:
        """
        Create a suitable structure for the future returned object JSON

        Parameters:
            branches (Dict): A dictionary containing branches

        Returns:
            None
        """
        for branch in packeges.keys():
            self.__json_structure[branch] = {}
            self.__json_structure[branch]['max_version'] = '0.0.0'
            for d in self.packeges[branch]:
                if self.compare_version(d['version'], self.__json_structure[branch]['max_version']):
                    self.__json_structure[branch]['max_version'] = d['version']
                if d['arch'] not in self.__json_structure[branch].keys():
                    self.__arch.append(d['arch'])
                    self.__json_structure[branch][d['arch']] = {
                        'pack': [],
                    }
                self.__json_structure[branch][d['arch']]['pack'].append(d)



    def finish_task_json(self):
        """
        - все пакеты, которые есть в p10 но нет в sisyphus                -> zad_1
        - все пакеты, которые есть в sisyphus но их нет в p10             -> zad_2
        - все пакеты, version-release которых больше в sisyphus чем в p10 -> zad_3
        {
        'arch': {
            'zad_1': [],
            'zad_2': [],
            'zad_3': [],
            }
        }
        """
        res = dict.fromkeys(self.__arch, {
            'zad_1': [],
            'zad_2': [],
            'zad_3': [],
        })
        dd = {'p10': set(), 'sisyphus': set()}
        for arch in res:
            for p in self.__json_structure['p10'][arch]['pack']:
                if p not in self.__json_structure['sisyphus'][arch]['pack']:
                    res[arch]['zad_1'].append(p)
                dd['p10'].add(p['version'])
            for p in self.__json_structure['sisyphus'][arch]['pack']:
                if p not in self.__json_structure['p10'][arch]['pack']:
                    res[arch]['zad_2'].append(p)
                if self.compare_version(p['version'], self.__json_structure['p10']['max_version']):
                    res[arch]['zad_3'].append(p)
                dd['sisyphus'].add(p['version'])
        result_json = json.dumps(res)
        print(len(res['x86_64-i586']['zad_1']))
        print(len(res['x86_64-i586']['zad_2']))
        print(len(res['x86_64-i586']['zad_3']))
        print(dd)
        return res




class TestCli:
    """
    Blabla
    """

    def __init__(self, url=URL):
        self.api_url = url
        self.branches = ("sisyphus", "p10")
        self.api_methods = {
            1: '/export/branch_binary_packages/{branch}',
        }
        self.choice_api_method = 1

    @property
    def get_api_url(self) -> str:
        """
        Getter method for retrieving the api_url attribute.
        Returns:
        str: The URL of the API.
        """
        return self.api_url
    @property
    def get_api_methods(self) -> Dict[int, str]:
        """
        Return the dictionary of API methods available.
        Dict[index, method]
        """
        return self.api_methods

    @property
    def get_branches(self) -> Tuple:
        """
        Getter method for retrieving the branches attribute.
        Returns:
        Tuple: A tuple containing the branches.
        """
        return self.branches

    def update_api_method(self, num_method: int) -> None:
        """
        Update the choice_api method attribute with the index of the selected method.
        Args:
        num_method (int): The index of the selected method.
        """
        self.choice_api_method = num_method

    def take_packages_from_branches(self) -> Dict[str, List[Dict]]:
        """
        Take packages from branches and return a dictionary where keys are branch names
        and values are lists of dictionaries containing packages.
        :return
        dict[str_branch: list[packages]]
        """
        ready_url_with_branch = self.api_url + self.api_methods[self.choice_api_method]
        dict_of_branch_pack = {
            branch: requests.get(ready_url_with_branch.format(branch=branch)).json()['packages']
            for branch in self.branches
        }
        return dict_of_branch_pack

    def main(self):
        pass


if __name__ == '__main__':
    # fire.Fire(TestCli())
    a = TestCli()
    res = MyJsonerCompare(br)
    pprint.pprint(res.finish_task_json())







































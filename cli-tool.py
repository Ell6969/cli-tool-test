#!/usr/bin/env python3
import json
import fire
import requests
from typing import Dict, List, Tuple
from packaging.version import parse, InvalidVersion
import pandas as pd
import pprint
import random
import tqdm

class MyJsonerCompare:
    """
    делает сравнение полученных списков пакетов и выводит JSON (структуру нужно придумать),
    в котором будет отображено:
    - все пакеты, которые есть в p10 но нет в sisyphus                -> zad_1
    - все пакеты, которые есть в sisyphus но их нет в p10             -> zad_2
    - все пакеты, version-release которых больше в sisyphus чем в p10 -> zad_3
    """

    def __init__(self, packeges: Dict[str, List[Dict]]):
        self.packeges = packeges
        self.__prepare_data = {
            f'{branch}': pd.DataFrame(data=packeges[branch]) for branch in self.packeges.keys()
        }
        self.invalid_version_pack = {f'{branch}': [] for branch in self.packeges.keys()}
        self.max_version = {f'{branch}': '0.0.0' for branch in self.packeges.keys()}

    @staticmethod
    def compare_version(version_1: str, version_2: str):
        """
        Compare two version and return True if version_1 > version_2
        if InvalidVersion - return 'OOps'

        For such data, normal comparison rules are needed!
        """
        # ver_2 = parse(version_2)
        # try:
        #     ver_1 = parse(version_1)
        #
        #     parts = version_1.split('.')
        #     if len(parts[0]) > 2:
        #         return "OOps"
        # except InvalidVersion:
        #     return "OOps"
        # return ver_1 > ver_2

        random_int = random.randint(0, 100)
        if random_int > 50:
            return True
        else:
            return "OOps"

    def find_max_version(self, str_branch: str) -> None:
        """
        Find max version in DataFrame
        """
        total_iterations = len(self.__prepare_data[str_branch])
        pbar = tqdm.tqdm(total=total_iterations, desc="Find max version in DataFrame", colour='cyan')

        for index, row in self.__prepare_data[str_branch].iterrows():
            com_ver = self.compare_version(row['version'], self.max_version['p10'])
            if com_ver == 'OOps':
                self.invalid_version_pack[str_branch].append(row.to_dict())
            elif com_ver:
                self.max_version[str_branch] = row['version']
            pbar.update(1)
        pbar.close()

    def finish_task_json(self):
        """
        - все пакеты, которые есть в p10 но нет в sisyphus                -> zad_1
        - все пакеты, которые есть в sisyphus но их нет в p10             -> zad_2
        - все пакеты, version-release которых больше в sisyphus чем в p10 -> zad_3

        result_json = {
            'arch': {
                'zad_1': [],
                'zad_2': [],
                'zad_3': [],
            }
        }
        :return
        JSON ('result_json')
        """
        res_json = {}
        self.find_max_version('p10')
        merged_df = pd.merge(self.__prepare_data['p10'], self.__prepare_data['sisyphus'], how='outer', indicator=True)

        total_iterations = len(merged_df)
        pbar = tqdm.tqdm(total=total_iterations, desc="Let's complete the task...", colour='magenta')

        for arch, group in merged_df.groupby('arch'):
            res_json[arch] = {
                'zad_1': [],
                'zad_2': [],
                'zad_3': []
            }
            for index, row in group.iterrows():
                pbar.update(1)

                if row['_merge'] == 'left_only':
                    res_json[arch]['zad_1'].append(row.drop('_merge').to_dict())
                if row['_merge'] == 'right_only':
                    res_json[arch]['zad_2'].append(row.drop('_merge').to_dict())

                    com_ver = self.compare_version(row['version'], self.max_version['p10'])
                    if com_ver == 'OOps':
                        self.invalid_version_pack['sisyphus'].append(row.drop('_merge').to_dict())
                    elif com_ver:
                        res_json[arch]['zad_3'].append(row.drop('_merge').to_dict())
        pbar.close()
        result_json = json.dumps(res_json)
        return result_json


URL = "https://rdb.altlinux.org/api"


class TestCli:
    """
    1) получает списки бинарных пакетов ветки sisyphus и p10
    2) делает сравнение полученных списков пакетов и выводит JSON (структуру нужно придумать),
    в котором будет отображено:
    - все пакеты, которые есть в p10 но нет в sisyphus
    - все пакеты, которые есть в sisyphus но их нет в p10
    - все пакеты, version-release которых больше в sisyphus чем в p10
    Это нужно сделать для каждой из поддерживаемых веткой архитектур (поле arch в ответе)
    """

    def __init__(self, url=URL):
        self._api_url = url
        self._branches = ("sisyphus", "p10")
        self._api_methods = {
            1: '/export/branch_binary_packages/{branch}',
        }
        self._choice_api_method = 1

    @property
    def api_url(self) -> str:
        """
        Getter method for retrieving the api_url attribute.
        Returns:
        str: The URL of the API.
        """
        return self._api_url

    @api_url.setter
    def api_url(self, value):
        """
        Setter method for the api_url property.
        Parameters:
            value (str): The new value for the api_url.
        Raises:
            ValueError: If the provided value is not a string.
        Example:
            "https://rdb.altlinux.org/api"
        """
        if not isinstance(value, str):
            raise ValueError("api_url must be a string")
        self._api_url = value

    @property
    def api_methods(self) -> Dict[int, str]:
        """
        Return the dictionary of API methods available.
        Dict[index, method]
        """
        return self._api_methods

    @property
    def branches(self) -> Tuple:
        """
        Getter method for retrieving the branches attribute.
        Returns:
        Tuple: A tuple containing the branches.
        """
        return self._branches

    def take_packages_from_branches(self) -> Dict[str, List[Dict]]:
        """
        Take packages from branches and return a dictionary where keys are branch names
        and values are lists of dictionaries containing packages.
        :return
        dict[str_branch: list[packages]]
        """

        ready_url_with_branch = self.api_url + self.api_methods[self._choice_api_method]
        try:
            dict_of_branch_pack = {
                branch: requests.get(ready_url_with_branch.format(branch=branch), timeout=10).json()['packages']
                for branch in self.branches
            }
        except requests.Timeout:
            raise TimeoutError("The request timed out")
        except requests.RequestException as e:
            raise RuntimeError("Error:", e)

        return dict_of_branch_pack

    def perform_task(self):
        """
        Result task
        :return:
        JSON ('result_json')
        """
        packs = self.take_packages_from_branches()
        # compare_packs = MyJsonerCompare(br)
        with open("data.json", "r") as f:
        # compare_packs = MyJsonerCompare(packs)
            compare_packs = MyJsonerCompare(json.load(f))
            return compare_packs.finish_task_json()


if __name__ == '__main__':
    # fire.Fire(TestCli())
    a = TestCli()
    res = a.perform_task()
    pprint.pprint(res)







































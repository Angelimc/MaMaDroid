import sys
import ast
import os
import json
from collections import OrderedDict
from collections import Counter


# text_files_dir = '/data/Armaan/Malware2017_001/mamadroid/GPMalware2018/'
# local test:
text_files_dir = '/Users/angeli/My_Documents/mamadroid/'


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


def create_mapping_in_json(package_file, graph_file):
    caller_callee_package_map = {}

    with open(package_file, 'r') as f:
        caller_callee_packages_list = f.readlines()
    with open(graph_file, 'r') as f:
        caller_callee_methods_list = f.readlines()

    if len(caller_callee_packages_list) != len(caller_callee_methods_list):
        raise Exception('Length of caller callee packages list: {} does not match length of caller callee methods list:'
                        ' {}'.format(len(caller_callee_packages_list), len(caller_callee_methods_list)))

    for i, caller_callee_packages in enumerate(caller_callee_packages_list):
        if i <= 2:
            callee_packages = caller_callee_packages.split()
            caller_package = callee_packages.pop(0)
            print "caller_package: ", caller_package
            print "callee_packages: ", callee_packages

            caller_callee_methods = caller_callee_methods_list[i].split(" ==> ")
            caller_method = caller_callee_methods[0]
            callee_methods = ast.literal_eval(caller_callee_methods[1])
            print "caller_method: ", caller_method
            print "callee_methods: ", callee_methods

            if len(callee_packages) != len(callee_methods):
                raise Exception('Length of callee packages: {} for {} does not match length of callee methods: {} for '
                                '{} in line {}'.format(len(callee_packages), caller_package, len(callee_methods),
                                                       caller_method, i))

            for j, callee_package in enumerate(callee_packages):
                key = caller_package + ' -> ' + callee_package
                method_pair = caller_method + ' -> ' + callee_methods[j]
                default_value = {"num_method_pairs": 0, "method_pairs": []}
                caller_callee_package_map.setdefault(key, default_value)
                caller_callee_package_map[key]["method_pairs"].append(method_pair)
                caller_callee_package_map[key]["num_method_pairs"] += 1

    return caller_callee_package_map


def order_and_count_method_pairs(caller_callee_package_map):
    pass


def order_by_num_method_pairs(caller_callee_package_map):
    return OrderedDict(sorted(caller_callee_package_map.items(), key=lambda t: int(t[1]['num_method_pairs']), reverse=True))


def main(apk_name):
    """
    Outputs json file with mapping of key: "caller package -> callee package pair" to a set of "caller method -> list of
    callee methods" pairs for a given apk.

    :param apk_name: the apk to process
    :return:
    """
    package_file = text_files_dir + 'package/' + apk_name + '.txt'
    graph_file = text_files_dir + 'graphs/' + apk_name + '.txt'

    if not os.path.exists(package_file):
        raise Exception('Package file: {} does not exist'.format(package_file))
    if not os.path.exists(graph_file):
        raise Exception('Graphs file: {} does not exist'.format(package_file))

    caller_callee_package_map = create_mapping_in_json(package_file, graph_file)
    order_and_count_method_pairs(caller_callee_package_map)
    caller_callee_package_map = order_by_num_method_pairs(caller_callee_package_map)
    with open('caller_callee_package_map/' + apk_name + '.json', 'w') as f:
        json.dump(caller_callee_package_map, f, ensure_ascii=False, indent=4, default=set_default)


if __name__ == '__main__':
    apk = sys.argv[1]
    print(apk)
    main(apk)

import json
from .graph import Graph


def get_dependencies(attr_name):
    data = sanitize_json_and_store("modules/static/modules_dependency.json")
    generate_dot(data)
    g = generate_dependency_matrix(data)
    graph = Graph(g)
    return find_all_dependency_paths_from_module(graph, attr_name)


def get_dependents(attr_name):
    data = sanitize_json_and_store("modules/static/modules_dependency.json")
    generate_dot(data)
    g = generate_dependency_matrix(data)
    graph = Graph(g)
    return find_all_dependent_paths_to_module(graph, attr_name)


def get_num_dependencies(attr_name):
    # print(attr_name)
    data = sanitize_json_and_store("modules/static/modules_dependency.json")
    generate_dot(data)
    g = generate_dependency_matrix(data)
    graph = Graph(g)

    try:
        from_module = len(find_all_dependency_paths_from_module(graph, attr_name)['path'])
    except:
        from_module = -1

    try:
        to_module = len(find_all_dependent_paths_to_module(graph, attr_name)['path'])
    except:
        to_module = -1

    return {"dependencies": from_module, "dependents": to_module}


def sanitize_json_and_store(file):
    """sanitizes the module dependency json data,
        store it to data_file.json and return the sanitized data.
    """
    with open(file, 'r') as read_file:
        data = json.load(read_file)
    data.pop('numberOfModules', None)
    data['children'] = data.pop('modules')
    for module in data['children']:
        module.pop('SDF', None)
        module.pop('viewModule', None)
        module.pop('dependents', None)
        module.pop('moduleApolloPackageName', None)
        module.pop('SDFApolloPackageName', None)
        module['children'] = module.pop('dependencies')
        dep_list = []
        for dep_module in module['children']:
            dep_module_dict = {'name': dep_module}
            dep_list.append(dep_module_dict)
        module['children'] = dep_list
    with open("data_file.json", 'w') as write_file:
        json.dump(data, write_file)
    return data


def generate_dot(data):
    """generate a dot file from the json data provided and
        store it in module_dependency.dot file.
        This dot can be used to visualize graph in a software.
    """
    dependency_dot = 'digraph module_dependencies {\n'
    for module in data['children']:
        if not module['children']:
            dependency_dot = dependency_dot + module['name'] + ';\n'
        else:
            for dep_module in module['children']:
                dependency_dot = dependency_dot + module['name'] + " -> " + dep_module['name'] + ';\n'
    dependency_dot = dependency_dot + '}'
    with open("module_dependency.dot", 'w') as dependency_dot_file:
        dependency_dot_file.write(dependency_dot)


def generate_dependency_matrix(data):
    """generate dependency matrix from data,
        create a graph and return it.
    """
    graph = {}
    for module in data['children']:
        dep_list = module['children']
        list = []
        for dep_module in dep_list:
            list.append(dep_module['name'])
        graph[module['name']] = list
    return graph


def find_all_dependent_paths_to_module(graph, required_module):
    """print all the paths that are a dependent on a module
        and also print the unique modules in that path
    """
    dcs = {"path": [], "unique": None, "isComplex": None}
    if required_module:
        unique_dependent_modules = set()
        for path in graph.find_all_dependent_paths(required_module):
            path.pop(len(path) - 1)
            if len(path) > 0:
                dcs['path'].append(path)
            for module in path:
                unique_dependent_modules.add(module)
        dcs['unique'] = list(unique_dependent_modules)
        safe_limit = 50
        dcs['isComplex'] = True if len(dcs['path']) > safe_limit else False
    return dcs


def find_all_dependency_paths_from_module(graph, required_module):
    """print all the paths that are a module depends on
        and also print the unique modules in that path
    """
    dcs = {"path": [], "unique": None, "isComplex": None}
    if required_module:
        unique_dependency_modules = set()
        for path in graph.find_all_dependency_paths(required_module):
            path.pop(0)
            dcs['path'].append(path)
            for module in path:
                unique_dependency_modules.add(module)
        dcs['unique'] = list(unique_dependency_modules)
        safe_limit = 50
        dcs['isComplex'] = True if len(dcs['path']) > safe_limit else False
    return dcs

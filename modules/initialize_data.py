import pandas
import modules.dependencies as dcs
from modules.models import Module, Attribute


def load_data():
    df = pandas.read_excel('modules/static/data.xlsx')
    data = create_dictionary(df.values)
    create_db(data)


def create_db(data):
    for module in data:
        module_name = module['name'] if len(module['name']) < 400 else module['name'][:400]
        m = Module(name=module_name, attr_count=len(module['attributes']))
        m.save()
        for attr in module['attributes']:
            a = Attribute(name=attr['attrName'], data_repo=attr['dataRepo'], java_class=attr['javaClass'],
                          cti=attr['cti'], module=m)
            a.save()
    attributes = Attribute.objects.all()
    for attr in attributes:
        attr.num_dependencies = dcs.get_num_dependencies(attr.name)['dependencies']
        attr.num_dependents = dcs.get_num_dependencies(attr.name)['dependents']
        attr.save()


def create_dictionary(data):
    final = []
    i = 0
    for row in range(len(data)):
        if data[row][0] != -1:
            module = {'id': i + 1, 'name': data[row][1], 'attributes': []}
            j = 1
            for next in range(row + 1, len(data)):
                if data[row][1] == data[next][1]:
                    data[next][0] = -1
                    cti = str(data[next][5]).replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace("'", '').split(",")
                    cti = [item.strip(' ') for item in cti]
                    attr = {'attrID': j,
                            'attrName': data[next][2],
                            'dataRepo': data[next][3],
                            'javaClass': data[next][4],
                            'cti': cti
                            }
                    module['attributes'].append(attr)
                    j += 1
            final.append(module)
            i += 1
    return final

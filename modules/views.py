# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
from django.shortcuts import render
from modules.models import Module, Attribute
from django.forms.models import model_to_dict
import modules.dependencies as ds
import collections


def index(request):
    """
    This function renders the index page containing information about every module.

    The load_data() function from modules.initialize_data is used to get data from the .csv file, filter it,
    make it usable and store it in the database so that page rendering time is reduced. This function should be
    called only once initially to store the data, and once data is ready there is no need to call this function.

    :param request:
    :return:
    """
    # id.load_data()

    modules = Module.objects.all()
    stats = dict(get_stats())
    count = 0
    for key, val in stats.items():
        count += val
    context = {'stats': stats, 'total_mod_count': count, 'modules': modules}
    return render(request, 'modules/index.html', context)


def module(request, module_id):
    module = Module.objects.filter(id=module_id)[0]
    attributes = Attribute.objects.filter(module=module)
    context = {"module": module, "attributes": attributes}
    return render(request, 'modules/show.html', context)


def dependency(request, attr_id):
    if attr_id.isdigit():
        attr_id = int(attr_id)
        attribute = Attribute.objects.filter(id=attr_id)[0]
    else:
        attribute = Attribute.objects.filter(name=attr_id)
        if len(attribute) < 1:
            context = {'attr_name': attr_id}
            return render(request, 'modules/module_error.html', context)
        else:
            attribute = attribute[0]

    attr_name = attribute.name
    dcs_from = ds.get_dependencies(attr_name)
    dcs_to = ds.get_dependents(attr_name)
    context = {"module_id": attribute.module.id, "attribute":  model_to_dict(attribute), "dcs_from": dcs_from, "dcs_to": dcs_to}
    return render(request, 'modules/dependency.html', context)


def dependency_ajax(request, attr_id):
    attribute = Attribute.objects.filter(id=int(attr_id))[0]
    attr_name = attribute.name
    dcs_from = ds.get_dependencies(attr_name)
    data = {"dcs_from": dcs_from, "attribute": model_to_dict(attribute)}
    return JsonResponse(data)


def dependent_ajax(request, attr_id):
    attribute = Attribute.objects.filter(id=int(attr_id))[0]
    attr_name = attribute.name
    dcs_to = ds.get_dependents(attr_name)
    data = {"dcs_to": dcs_to, "attribute": model_to_dict(attribute)}
    return JsonResponse(data)


def get_stats():
    col = [attr.data_repo for attr in Attribute.objects.all()]
    counter = collections.Counter(col)
    return dict(counter)



#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import json

GROUPS_NAME = 'stack'
FILENAME = "/etc/xlcloud-facts.json"

METRICS = {
    'time': 0,
    'data': {}
}

METRICS_CACHE_MAX = 5
LAST_METRICS = dict(METRICS)


def get_metrics():
    """Return all metrics."""

    global FILENAME, METRICS, LAST_METRICS
    if (time.time() - METRICS['time']) > METRICS_CACHE_MAX:
        with open(FILENAME) as f:
            facts = f.read()

        metrics = json.loads(facts)
        if 'stack_id' in metrics.keys():
            arn = metrics['stack_id']
            layer_arn = metrics['layer_id']

            metrics['tenant_id'] = arn.split(':')[4]

            metrics['stack_id'] = arn.split('/')[-1]
            metrics['arn'] = arn
            metrics['stack_name'] = arn.split(':')[5].split('/')[1]

            metrics['layer_id'] = layer_arn.split('/')[-1]
            metrics['arn_layer'] = layer_arn
            metrics['layer_name'] = layer_arn.split(':')[5].split('/')[1]

        LAST_METRICS = dict(METRICS)
        METRICS = {
            'time': time.time(),
            'data': metrics
        }

    return [METRICS, LAST_METRICS]


def get_value(name):
    try:
        metrics = get_metrics()[0]
        res = metrics['data'][name].replace('"', "'")
    except Exception:
        res = 0

    #print ">>>> %s" % str(res)
    return str(res)


def metric_init(params):
    """Initialize metric descriptors."""

    global FILENAME
    if 'facts_filename' in params:
        FILENAME = params['facts_filename']

    generators = []
    generators.append({
        'name': 'stack_id',
        'call_back': get_value,
        'time_max': 90,
        'value_type': 'string',
        'units': 'stackID',
        'slope': 'both',
        'format': '%s',
        'description': 'StackId of the Host',
        'groups': GROUPS_NAME
    })
    generators.append({
        'name': 'layer_id',
        'call_back': get_value,
        'time_max': 90,
        'value_type': 'string',
        'units': 'layerID',
        'slope': 'both',
        'format': '%s',
        'description': 'Layer ID of the Host',
        'groups': GROUPS_NAME
    })
    generators.append({
        'name': 'logical_resource_id',
        'call_back': get_value,
        'time_max': 90,
        'value_type': 'string',
        'units': 'logical ressource ID',
        'slope': 'both',
        'format': '%s',
        'description': 'Logical Resource ID of the Host',
        'groups': GROUPS_NAME
    })
    generators.append({
        'name': 'stack_name',
        'call_back': get_value,
        'time_max': 90,
        'value_type': 'string',
        'units': 'Stack Name',
        'slope': 'both',
        'format': '%s',
        'description': 'StackId of the Host',
        'groups': GROUPS_NAME
    })
    generators.append({
        'name': 'layer_name',
        'call_back': get_value,
        'time_max': 90,
        'value_type': 'string',
        'units': 'Layer Name',
        'slope': 'both',
        'format': '%s',
        'description': 'StackId of the Host',
        'groups': GROUPS_NAME
    })
    generators.append({
        'name': 'tenant_id',
        'call_back': get_value,
        'time_max': 90,
        'value_type': 'string',
        'units': 'Tenant ID',
        'slope': 'both',
        'format': '%s',
        'description': 'StackId of the Host',
        'groups': GROUPS_NAME
    })
    #generators.append({
    #    'name': 'arn',
    #    'call_back': get_value,
    #    'time_max': 90,
    #    'value_type': 'string',
    #    'units': 'stackID',
    #    'slope': 'both',
    #    'format': '%s',
    #    'description': 'StackId of the Host',
    #    'groups': GROUPS_NAME
    #})
    #generators.append({
    #    'name': 'arn_layer',
    #    'call_back': get_value,
    #    'time_max': 90,
    #    'value_type': 'string',
    #    'units': 'stackID',
    #    'slope': 'both',
    #    'format': '%s',
    #    'description': 'StackId of the Host',
    #    'groups': GROUPS_NAME
    #})
    return generators


def metric_cleanup():
    pass

if __name__ == '__main__':
    import eventlet
    descriptors = metric_init({})
    while True:
        for m in descriptors:
            v = m['call_back'](m['name'])
            print "get metrics : %s -> %s " % (m['name'], v)
            print ""
        eventlet.sleep(3)

# -*- coding: utf-8 -*-
"""$ python merge_yaml.py openapi.yaml part.yaml > out.yaml"""
import sys

import yaml


def merge(parent, child):
    """Update the `child` dictionary such that it inherits keys
    from the `parent` dict."""
    for k in parent:
        if k in child and isinstance(child[k], dict) and isinstance(parent[k], dict):
            merge(parent[k], child[k])
        else:
            child[k] = parent[k]


if __name__ == '__main__':
    _, parent, child = sys.argv

    with open(parent, 'r') as f:
        parent = yaml.load(f)

    with open(child, 'r') as f:
        child = yaml.load(f)

    merge(parent, child)
    sys.stdout.write(yaml.dump(child, default_flow_style=False))


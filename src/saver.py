import yaml
import os
import sys

def update(new_history, path):
    with open(path, 'w') as hsyml:
        yaml.dump(new_history, hsyml, default_flow_style=False)

# -*- coding:utf8 -*-
import os, sys
configs_folder = os.path.realpath(os.path.join(os.path.split(os.path.realpath(__file__))[0],'configs'))
if configs_folder not in sys.path:
    sys.path.insert(0, configs_folder)
# print configs_folder
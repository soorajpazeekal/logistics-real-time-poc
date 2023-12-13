import os, sys

config_ini_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "producer")
sys.path.append(config_ini_path)
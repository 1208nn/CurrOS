from os import name
from importlib import import_module

globals().update(import_module(f'.{name}', __package__).__dict__)

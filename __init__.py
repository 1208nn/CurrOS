from os import name

__all__ = ["appdata_path", "setProxy", "clearProxy"]

if name == "nt":
    from CurrOS.nt import *


else:
    from CurrOS.posix import *

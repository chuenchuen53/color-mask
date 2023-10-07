import ctypes
from platform import platform

import darkdetect as darkdetect

DARK_THEME_NAME = "darkly"
LIGHT_THEME_NAME = "litera"

scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100 if platform().startswith("Windows") else 1
theme_name = DARK_THEME_NAME if darkdetect.isDark() else LIGHT_THEME_NAME
app_title = "Color Mask"

import pathlib
import platform
from tkinter import filedialog

import darkdetect as darkdetect
import ttkbootstrap as ttk

from app_state import app_title, scale_factor, theme_name
from compare_imgs_frame import CompareImgsFrame
from hsv_label_frame import HsvLabelFrame


def _dark_title_bar_if_window_and_dark_mode(window: ttk.Window | ttk.Toplevel):
    if platform.platform().startswith("Windows") and darkdetect.isDark():
        import ctypes as ct

        window.update()
        dwmwa_use_immersive_dark_mode = 20
        set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
        get_parent = ct.windll.user32.GetParent
        hwnd = get_parent(window.winfo_id())
        rendering_policy = dwmwa_use_immersive_dark_mode
        value = ct.c_int(2)
        set_window_attribute(hwnd, rendering_policy, ct.byref(value), ct.sizeof(value))
        window.focus()


class App(ttk.Window):
    low_hsv_str_var: ttk.StringVar
    high_hsv_str_var: ttk.StringVar
    initialdir: pathlib.Path = pathlib.Path.home()

    def __init__(self):
        super().__init__(
            title=app_title, themename=theme_name, size=(int(1000 * scale_factor), int(600 * scale_factor))
        )
        _dark_title_bar_if_window_and_dark_mode(self)
        self.state("zoomed")

        self.low_hsv_str_var = ttk.StringVar(value="min: [0 0 0]")
        self.high_hsv_str_var = ttk.StringVar(value="max: [180 255 255]")

        self.img_frame = CompareImgsFrame(self, self.low_hsv_str_var, self.high_hsv_str_var)
        label_frame = HsvLabelFrame(self, self.low_hsv_str_var, self.high_hsv_str_var)
        open_image_btn = ttk.Button(self, text="Open Image", command=self.select_img)

        self.img_frame.pack(fill="both", expand=True)
        label_frame.pack(fill="both")
        open_image_btn.pack(side="left", padx=24, pady=24)

    def select_img(self):
        filetypes = (("image files", "*.jpg;*.png"), ("All files", "*.*"))
        file_path = filedialog.askopenfilename(title="Pick your image", initialdir=self.initialdir, filetypes=filetypes)
        if (file_path is None) or (file_path == ""):
            return
        self.img_frame.set_new_img(file_path)
        self.initialdir = pathlib.Path(file_path).parent


if __name__ == "__main__":
    App().mainloop()

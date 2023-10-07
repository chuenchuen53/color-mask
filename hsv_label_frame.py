import ttkbootstrap as ttk


class HsvLabelFrame(ttk.Frame):
    low_hsv_str_var: ttk.StringVar
    high_hsv_str_var: ttk.StringVar

    def __init__(self, parent, low_hsv_str_var, high_hsv_str_var):
        super().__init__(parent)
        self.low_hsv_str_var = low_hsv_str_var
        self.high_hsv_str_var = high_hsv_str_var
        min_hsv_label = ttk.Label(self, textvariable=self.low_hsv_str_var)
        max_hsv_label = ttk.Label(self, textvariable=self.high_hsv_str_var)
        min_hsv_label.pack(side="top", fill="x", padx=24, pady=8)
        max_hsv_label.pack(side="bottom", fill="x", padx=24, pady=8)

import cv2
import numpy as np
import ttkbootstrap as ttk
from PIL import Image, ImageTk

from app_state import scale_factor


class CompareImgsFrame(ttk.Frame):
    low_hsv_str_var: ttk.StringVar
    high_hsv_str_var: ttk.StringVar
    left_canvas: ttk.Canvas
    right_canvas: ttk.Canvas
    original_img: np.ndarray
    processed_img: np.ndarray
    photo_img_1: ImageTk.PhotoImage
    photo_img_2: ImageTk.PhotoImage
    mask_colors: list[np.ndarray] = []

    def __init__(self, parent, low_hsv_str_var, high_hsv_str_var):
        super().__init__(parent)

        self.low_hsv_str_var = low_hsv_str_var
        self.high_hsv_str_var = high_hsv_str_var

        canvas_size = min(parent.winfo_width() // 2, 700 * scale_factor) - 24 * scale_factor
        self.left_canvas = ttk.Canvas(self, width=canvas_size, height=canvas_size)
        self.right_canvas = ttk.Canvas(self, width=canvas_size, height=canvas_size)

        self.left_canvas.bind("<Button-1>", lambda e: self.append_color_and_update_processed_img(e))
        self.left_canvas.bind("<Button-3>", lambda e: self.remove_last_color_and_update_processed_img(e))
        self.right_canvas.bind("<Button-1>", lambda e: self.append_color_and_update_processed_img(e))
        self.right_canvas.bind("<Button-3>", lambda e: self.remove_last_color_and_update_processed_img(e))

        self.left_canvas.pack(side="left", fill="both", expand=True, padx=24, pady=24)
        self.right_canvas.pack(side="right", fill="both", expand=True, padx=24, pady=24)

        self.set_new_img("test-img/img1.jpg")

    def show_left_img(self):
        self.photo_img_1 = ImageTk.PhotoImage(image=Image.fromarray(self.original_img))
        self.left_canvas.create_image(0, 0, anchor="nw", image=self.photo_img_1)

    def show_right_img(self):
        self.right_canvas.delete("all")
        self.photo_img_2 = ImageTk.PhotoImage(image=Image.fromarray(self.processed_img))
        self.right_canvas.create_image(0, 0, anchor="nw", image=self.photo_img_2)

    def remove_last_color_and_update_processed_img(self, _event):
        if len(self.mask_colors) > 0:
            self.mask_colors.pop()
            self.update_processed_img()

    def append_color_and_update_processed_img(self, event):
        color = self.get_clicked_position_color(event)
        if color is not None:
            self.mask_colors.append(color)
            self.update_processed_img()

    def update_processed_img(self):
        if len(self.mask_colors) == 0:
            self.processed_img = self.original_img
            self.show_right_img()
            self.low_hsv_str_var.set("min: [0 0 0]")
            self.high_hsv_str_var.set("max: [180 255 255]")
            return

        h_list = [c[0] for c in self.mask_colors]
        s_list = [c[1] for c in self.mask_colors]
        v_list = [c[2] for c in self.mask_colors]
        min0, max0 = min(h_list), max(h_list)
        min1, max1 = min(s_list), max(s_list)
        min2, max2 = min(v_list), max(v_list)

        hsv_lower_offset = np.array([-5, -10, -10])
        hsv_upper_offset = np.array([5, 10, 10])
        min_hsv = np.array([min0, min1, min2]) + hsv_lower_offset
        max_hsv = np.array([max0, max1, max2]) + hsv_upper_offset
        self.low_hsv_str_var.set(f"min: {min_hsv}")
        self.high_hsv_str_var.set(f"max: {max_hsv}")

        hsv_img = cv2.cvtColor(self.original_img, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(hsv_img, min_hsv, max_hsv)
        masked = cv2.bitwise_and(hsv_img, hsv_img, mask=mask)
        self.processed_img = cv2.cvtColor(masked, cv2.COLOR_HSV2RGB)
        self.show_right_img()

    def get_clicked_position_color(self, event) -> np.ndarray | None:
        x, y = event.x, event.y
        if x > self.original_img.shape[1] or y > self.original_img.shape[0]:
            return None
        one_pixel_img = np.array([[self.original_img[y, x]]])
        hsv = cv2.cvtColor(one_pixel_img, cv2.COLOR_RGB2HSV)
        return hsv[0, 0]

    def resize_img(self, img, canvas):
        canvas_width = int(canvas.winfo_reqwidth())
        canvas_height = int(canvas.winfo_reqheight())
        img_h = img.shape[0]
        img_w = img.shape[1]
        if float(img_w / img_h) > float(canvas_width / canvas_height):
            img_cv = cv2.resize(img, (canvas_width, int(canvas_width * img_h / img_w)), interpolation=cv2.INTER_AREA)
        else:
            img_cv = cv2.resize(img, (int(canvas_height * img_w / img_h), canvas_height), interpolation=cv2.INTER_AREA)
        return cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

    def set_new_img(self, file_path):
        self.mask_colors = []
        self.original_img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
        self.processed_img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
        self.original_img = self.resize_img(self.original_img, self.left_canvas)
        self.processed_img = self.resize_img(self.processed_img, self.right_canvas)
        self.show_left_img()
        self.show_right_img()

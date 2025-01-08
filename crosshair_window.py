import customtkinter as ctk
from PIL import Image, ImageDraw, ImageTk

class CrosshairWindow(ctk.CTkToplevel):
    def __init__(self, settings_manager):
        super().__init__()
        self.settings_manager = settings_manager
        self.attributes("-fullscreen", True)
        self.attributes("-topmost", True)
        self.attributes("-transparentcolor", "white")
        self.configure(bg="white")
        self.canvas = ctk.CTkCanvas(self, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.update_crosshair()

    def update_crosshair(self):
        self.canvas.delete("all")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x, center_y = screen_width // 2, screen_height // 2

        settings = self.settings_manager.settings
        shape = settings["shape"]
        color = settings["color"]
        scale = settings["scale"]
        line_width = settings["line_width"]

        if shape == "stick_figure":
            self.draw_stick_figure(center_x, center_y, color, scale, line_width)
        elif shape == "simple_crosshair":
            self.draw_simple_cross(center_x, center_y, color, scale, line_width)
        elif shape == "circle_with_dot":
            self.draw_circle_with_dot(center_x, center_y, color, scale, line_width)

    def draw_stick_figure(self, center_x, center_y, color, scale, line_width):
        head_radius = int(15 * scale)
        body_height = int(60 * scale)
        arm_length = int(40 * scale)
        leg_length = int(30 * scale)

        self.canvas.create_oval(center_x - head_radius, center_y - head_radius,
                                center_x + head_radius, center_y + head_radius,
                                outline=color, width=line_width)
        self.canvas.create_line(center_x, center_y + head_radius,
                                center_x, center_y + head_radius + body_height,
                                fill=color, width=line_width)
        arm_y_start = center_y + head_radius + body_height // 4
        arm_x_offset = int(30 * scale)
        self.canvas.create_line(center_x, arm_y_start,
                                center_x - arm_x_offset, arm_y_start + int(20 * scale),
                                fill=color, width=line_width)
        self.canvas.create_line(center_x, arm_y_start,
                                center_x + arm_x_offset, arm_y_start + int(20 * scale),
                                fill=color, width=line_width)
        leg_y_start = center_y + head_radius + body_height
        leg_x_offset = int(20 * scale)
        self.canvas.create_line(center_x, leg_y_start,
                                center_x - leg_x_offset, leg_y_start + leg_length,
                                fill=color, width=line_width)
        self.canvas.create_line(center_x, leg_y_start,
                                center_x + leg_x_offset, leg_y_start + leg_length,
                                fill=color, width=line_width)

    def draw_simple_cross(self, center_x, center_y, color, scale, line_width):
        line_length = int(15 * scale)
        self.canvas.create_line(center_x - line_length, center_y,
                                center_x + line_length, center_y,
                                fill=color, width=line_width)
        self.canvas.create_line(center_x, center_y - line_length,
                                center_x, center_y + line_length,
                                fill=color, width=line_width)

    def draw_circle_with_dot(self, center_x, center_y, color, scale, line_width):
        radius = int(10 * scale)
        dot_radius = int(2 * scale)
        self.canvas.create_oval(center_x - radius, center_y - radius,
                                center_x + radius, center_y + radius,
                                outline=color, width=line_width)
        self.canvas.create_oval(center_x - dot_radius, center_y - dot_radius,
                                center_x + dot_radius, center_y + dot_radius,
                                fill=color, outline=color)
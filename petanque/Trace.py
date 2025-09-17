from math import sqrt, sin, atan2, cos


class Trace:
    def __init__(self, master, lancer):

        self.master = master

        self.start_x_px = self.master.start_xm * self.master.metre
        self.start_y_px = (self.master.dim_terrain[1] - self.master.start_ym) * self.master.metre
        self.line_id = None
        self.contact_point_id = None

        self.master.canvas.bind("<ButtonPress-1>", self.start_draw)
        self.master.canvas.bind("<B1-Motion>", self.update_line)
        self.master.canvas.bind("<ButtonRelease-1>", self.end_draw)

        self.x_final_m = None
        self.y_final_m = None
        self.coeff_lancer = lancer



    def start_draw(self, event):
        if self.master.jouer:
            self.line_id = self.master.canvas.create_line(self.start_x_px, self.start_y_px, event.x, event.y, fill="blue")

    def calc_speeds(self, event):

        self.x_final_m = event.x / self.master.metre
        self.y_final_m = (self.master.dim_terrain[1] - event.y / self.master.metre)

        angle_principal = atan2(self.x_final_m - self.master.start_xm, self.y_final_m - self.master.start_ym)

        speed_1 = (self.x_final_m - self.master.start_xm)
        speed_2 = (self.y_final_m - self.master.start_ym)

        speed = sqrt(speed_1 ** 2 + speed_2 ** 2) * self.coeff_lancer

        speed_x = sin(angle_principal) * speed * cos(self.master.drop_angle)
        speed_y = cos(angle_principal) * speed * cos(self.master.drop_angle)
        speed_z = speed * sin(self.master.drop_angle)

        return speed_x, speed_y, speed_z

    def update_line(self, event):

        if self.master.jouer:
            if self.line_id is None:
                self.line_id = self.master.canvas.create_line(self.start_x_px, self.start_y_px, event.x, event.y, fill="blue")

        if self.master.jouer:
            if self.line_id is not None:
                self.master.canvas.coords(self.line_id, self.start_x_px, self.start_y_px, event.x, event.y)

            speed_x, speed_y, speed_z = self.calc_speeds(event)

            discriminant = speed_z ** 2 + 2 * self.master.gravity * self.master.hauteur_bonhomme

            t_impact = (speed_z + sqrt(discriminant)) / self.master.gravity

            x_impact_m = self.master.start_xm + speed_x * t_impact
            y_impact_m = self.master.start_ym + speed_y * t_impact

            x_impact_px = x_impact_m * self.master.metre
            y_impact_px = (self.master.dim_terrain[1] - y_impact_m) * self.master.metre

            point_radius = 10

            if self.contact_point_id is None:
                self.contact_point_id = self.master.canvas.create_oval(x_impact_px - point_radius,
                                                                       y_impact_px - point_radius,
                                                                       x_impact_px + point_radius,
                                                                       y_impact_px + point_radius)
            else:
                self.master.canvas.coords(self.contact_point_id, x_impact_px - point_radius, y_impact_px - point_radius,
                                          x_impact_px + point_radius, y_impact_px + point_radius)

    def end_draw(self, event):
        if self.master.jouer:
            self.master.canvas.delete(self.line_id)
            self.master.canvas.delete(self.contact_point_id)
            self.line_id = None
            self.contact_point_id = None

            speed_x, speed_y, speed_z = self.calc_speeds(event)

            self.master.lancer_boule(speed_x, speed_y, speed_z)

            self.master.jouer = False

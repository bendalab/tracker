class ROI(object):
    def __init__(self, x_1, y_1, x_2, y_2):
            self.__x_1 = x_1
            self.__y_1 = y_1
            self.__x_2 = x_2
            self.__y_2 = y_2

    def import_cfg_values(self, cfg):
        self.x1 = cfg.getint('roi', 'x1')
        self.x2 = cfg.getint('roi', 'x2')
        self.y1 = cfg.getint('roi', 'y1')
        self.y2 = cfg.getint('roi', 'y2')


    @property
    def x1(self):
        return self.__x_1

    @x1.setter
    def x1(self, value):
        self.__x_1 = value

    @property
    def y1(self):
        return self.__y_1

    @y1.setter
    def y1(self, value):
        self.__y_1 = value

    @property
    def x2(self):
        return self.__x_2

    @x2.setter
    def x2(self, value):
        self.__x_2 = value

    @property
    def y2(self):
        return self.__y_2

    @y2.setter
    def y2(self, value):
        self.__y_2 = value

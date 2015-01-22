class ROI(object):
    def __init__(self, x_1, y_1, x_2, y_2):
        self.__x_1 = x_1
        self.__y_1 = y_1
        self.__x_2 = x_2
        self.__y_2 = y_2

    @property
    def x1(self):
        return self.__x_1

    @x1.setter
    def x1(self, x):
        self.__x_1 = x

    @property
    def y1(self):
        return self.__y_1

    @y1.setter
    def y1(self, x):
        self.__y_1 = x

    @property
    def x2(self):
        return self.__x_2

    @x2.setter
    def x2(self, x):
        self.__x_2 = x

    @property
    def y2(self):
        return self.__y_2

    @y2.setter
    def y2(self, x):
        self.__y_2 = x
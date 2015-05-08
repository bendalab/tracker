from ROI import ROI

class ROIManager(object):
    def __init__(self):
        self.roi_list = []

    def add_roi(self, x1, y1, x2, y2, name):
        self.roi_list.append(ROI(x1, y1, x2, y2, name))

    def set_roi(self, x1, y1, x2, y2, name):
        for entry in self.roi_list:
            if entry.name == name:
                entry.x1 = x1
                entry.y1 = y1
                entry.x2 = x2
                entry.y2 = y2
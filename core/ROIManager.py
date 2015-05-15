from ROI import ROI
import ConfigParser

class ROIManager(object):
    def __init__(self):
        self.roi_list = []

    def add_roi(self, x1, y1, x2, y2, name, controller=None):
        new_roi = ROI(x1, y1, x2, y2, name)
        if controller is not None:
            new_roi.import_cfg_values(controller.tracker.read_cfg)
        self.roi_list.append(new_roi)
        if controller is not None:
            controller.roi_added_to_tracker(new_roi)

    def get_roi(self, name):
        for entry in self.roi_list:
            if entry.name == name:
                return entry

    def set_roi(self, x1, y1, x2, y2, name):
        for entry in self.roi_list:
            if entry.name == name:
                entry.set_values(x1, y1, x2, y2)

    def add_cfg_values(self, cfg):
        for entry in self.roi_list:
            section = 'roi_{0:s}'.format(entry.name)
            cfg.add_section(section)
            cfg.set(section, "x1", str(entry.x1))
            cfg.set(section, "x2", str(entry.x2))
            cfg.set(section, "y1", str(entry.y1))
            cfg.set(section, "y2", str(entry.y2))

    def import_cfg_values(self, cfg):
        for entry in self.roi_list:
            entry.import_cfg_values(cfg)
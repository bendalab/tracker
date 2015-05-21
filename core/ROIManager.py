from ROI import ROI
import ConfigParser

class ROIManager(object):
    def __init__(self):
        self._roi_list = []

    def calc_roi_data(self, img):
        for entry in self._roi_list:
            entry.calc_all_data(img)

    def add_roi(self, x1, y1, x2, y2, name, controller=None):
        new_roi = ROI(x1, y1, x2, y2, name)
        if controller is not None:
            new_roi.import_cfg_values(controller.tracker.read_cfg)
        self._roi_list.append(new_roi)
        if controller is not None:
            controller.roi_added_to_tracker(new_roi)

    def remove_roi(self, name, controller=None):
        if name == "tracking_area" or name == "starting_area":
            print "can't remove tracking area or starting area!"
            return
        
        for i in range(len(self._roi_list)):
            if self._roi_list[i].name == name:
                self._roi_list.pop(i)
                print "removed roi from tracker"
                if controller is not None:
                    controller.roi_removed_from_tracker(name)
                break

    def get_roi(self, name):
        for entry in self._roi_list:
            if entry.name == name:
                return entry

    def set_roi(self, x1, y1, x2, y2, name):
        for entry in self._roi_list:
            if entry.name == name:
                entry.set_values(x1, y1, x2, y2)

    def add_cfg_values(self, cfg):
        for entry in self._roi_list:
            section = 'roi_{0:s}'.format(entry.name)
            cfg.add_section(section)
            cfg.set(section, "x1", str(entry.x1))
            cfg.set(section, "x2", str(entry.x2))
            cfg.set(section, "y1", str(entry.y1))
            cfg.set(section, "y2", str(entry.y2))

    def import_cfg_values(self, cfg):
        for entry in self._roi_list:
            entry.import_cfg_values(cfg)

    @property
    def roi_list(self):
        return self._roi_list
import ConfigParser

class MetaManager(object):
    def __init__(self):
        self._experimenter = ""
        self._fish_id = ""
        self._camera_model = ""
        self._camera_vendor = ""

    def import_cfg_values(self, cfg):
        self.experimenter = cfg.get("meta", "experimenter")
        self.fish_id = cfg.get("meta", "fish_id")

    def add_cfg_values(self, cfg):
        cfg.add_section("meta")
        cfg.set("meta", "experimenter", str(self.experimenter))
        cfg.set("meta", "fish_id", str(self.fish_id))

    @property
    def experimenter(self):
        return self._experimenter
    @experimenter.setter
    def experimenter(self, name):
        self._experimenter = name

    @property
    def fish_id(self):
        return self._fish_id
    @fish_id.setter
    def fish_id(self, object_id):
        self._fish_id = object_id

    @property
    def camera_model(self):
        return self._camera_model
    @camera_model.setter
    def camera_model(self, model):
        self._camera_model = model

    @property
    def camera_vendor(self):
        return self._camera_vendor
    @camera_vendor.setter
    def camera_vendor(self, vendor):
        self._camera_vendor = vendor

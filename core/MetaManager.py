import odml
import os
from MetaEntry import MetaEntry

class MetaManager(object):
    def __init__(self):
        self._meta_entries = []
        self.add_meta_entry("meta1", "/home/madai/Tracker/meta_templates/chripChamber_template.xml")
        self.add_meta_entry("video", "/home/madai/Videos/meta_test/2015-06-05/trial_0000.xml")

    def add_meta_entry(self, name, path, controller=None):
        self._meta_entries.append(MetaEntry(name, path))
        if controller is not None:
            controller.metadata_entry_added()

    @property
    def meta_entries(self):
        return self._meta_entries

    # def set_metadata_path(self, path, controller=None):
    #     self._metadata_path = path
    #     if controller is not None:
    #         controller.metadata_path_set()
    #
    # @property
    # def metadata_path(self):
    #     return self._metadata_path
    #
    # @metadata_path.setter
    # def metadata_path(self, path):
    #     if not os.path.exists(path):
    #         print "file doesn't exist (template), could not set template {0}".format(path)
    #         return
    #     self._metadata_path = path
    #
    # @property
    # def video_meta_path(self):
    #     return self._video_meta_path
    #
    # @video_meta_path.setter
    # def video_meta_path(self, path):
    #     if not os.path.exists(path):
    #         print "file doesn't exist (video template), could not set template {0}".format(path)
    #         return
    #     self._video_meta_path = path

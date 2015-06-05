import odml
import os

class MetaManager(object):
    def __init__(self):
        self._template_path = "/home/madai/Tracker/meta_templates/chripChamber_template.xml"

        self._video_meta_path = "/home/madai/Videos/meta_test/2015-06-05/trial_0000.xml"

    @property
    def template_path(self):
        return self._template_path

    @template_path.setter
    def template_path(self, path):
        if not os.path.exists(path):
            print "file doesn't exist (template), could not set template {0}".format(path)
            return
        self._template_path = path

    @property
    def video_meta_path(self):
        return self._video_meta_path

    @video_meta_path.setter
    def video_meta_path(self, path):
        if not os.path.exists(path):
            print "file doesn't exist (video template), could not set template {0}".format(path)
            return
        self._video_meta_path = path

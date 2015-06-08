import odml
import os
from MetaEntry import MetaEntry

class MetaManager(object):
    def __init__(self):
        self._meta_entries = []
        # self.add_meta_entry("meta1", "/home/madai/Tracker/meta_templates/chripChamber_template.xml")
        # self.add_meta_entry("video", "/home/madai/Videos/meta_test/2015-06-05/trial_0000.xml")

    def add_meta_entry(self, name, path, controller=None):
        if name not in [entry.name for entry in self._meta_entries]:
            new_meta_entry = MetaEntry(name, path)
            self._meta_entries.append(new_meta_entry)
            if controller is not None:
                controller.metadata_entry_added(new_meta_entry)
        else:
            print "name of meta entry must be unique! name already exists!"

    def remove_meta_entry(self, name, controller=None):
        for i in range(len(self._meta_entries)):
            print self._meta_entries[i].name
            if name == self._meta_entries[i].name:
                self._meta_entries.pop(i)
                if controller is not None:
                    controller.metadata_entry_removed(name)

    def add_cfg_values(self, cfg):
        cfg.add_section('metadata')
        for entry in self._meta_entries:
            cfg.set('metadata', entry.name, entry.path)

    def import_cfg_values(self, cfg, controller):
        try:
            cfg_entries = cfg.items('metadata')
        except Exception as e:
            print e
            return
        for entry in cfg_entries:
            self.add_meta_entry(entry[0], entry[1], controller)

    @property
    def meta_entries(self):
        return self._meta_entries

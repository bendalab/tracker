import collections
import numpy as np
import nix
import odml


class DataWriter(object):

    @staticmethod
    def time_to_seconds(time):
        if isinstance(time, collections.Iterable) and not isinstance(time, str):
            return map(DataWriter.time_to_seconds, time)
        else:
            ts = time.split(':')
            seconds = 0.
            seconds += float(ts[0]) * 3600
            seconds += float(ts[1]) * 60
            seconds += float(ts[-1])
        return seconds

    @staticmethod
    def save_trace(time, data, nix_block, name, nix_type, data_label, unit=None, set_labels=None):
        # get only those that are valid
        valid = []
        stamps = []
        for t, d in zip(time, data):
            if d is not None:
                valid.append(d)
                stamps.append(t)
        if len(valid) == 0:
            return
        # check if valid data is tuple
        if len(valid) > 0 and isinstance(valid[0], tuple):
            d = np.zeros((len(valid), len(valid[0])))
            for i, v in enumerate(valid):
                d[i, :] = list(v)
            array = nix_block.create_data_array(name, nix_type, data=d)
            array.label = data_label
            if unit is not None:
                array.unit = unit
            dim = array.append_range_dimension(stamps)
            dim.label = 'time'
            dim.unit = 's'
            dim = array.append_set_dimension()
            if set_labels is not None:
                dim.labels = set_labels

            return array
        else:
            d = np.asarray(valid)
            array = nix_block.create_data_array(name, nix_type, data=d)
            array.label = data_label
            if unit is not None:
                array.unit = unit
            dim = array.append_range_dimension(stamps)
            dim.label = 'time'
            dim.unit = 's'
            return array

    @staticmethod
    def append_sources(entity, sources):
        if entity is not None and hasattr(entity, "sources"):
            entity.sources.extend(sources)

    @staticmethod
    def write_nix(file_name, times, data_manager, roi_manager, meta_manager, parameters):
        name = file_name.split('/')[-1].split('.')[0]
        nix_file = nix.File.open(file_name, nix.FileMode.Overwrite)
        block = nix_file.create_block(name, 'nix.tracking')

        # some metadata
        tracker = nix_file.create_section('Tracker', 'software.tracker')
        tracker['Version'] = 1.5
        tracker['Source location'] = 'https://github.com/bendalab/tracker'
        settings = tracker.create_section('settings', 'software.settings')
        settings['Fish min size threshold'] = parameters['fish_min_size']
        settings['Fish max size threshold'] = parameters['fish_max_size']
        settings['Fish max size enabled'] = parameters['fish_max_size_enabled']
        settings['Erosion iterations'] = parameters['erosion_iterations']
        settings['Dilation iterations'] = parameters['dilation_iterations']
        settings['Erosion matrix value'] = parameters['erosion_matrix_value']
        settings['Dilation matrix value'] = parameters['dilation_matrix_value']
        settings['Start orientation'] = parameters['fish_start_orientation']

        for roi in roi_manager.roi_list:
            settings['ROI {0:s} X'.format(roi.name)] = roi.x1
            settings['ROI {0:s} Y'.format(roi.name)] = roi.y1
            settings['ROI {0:s} WIDTH'.format(roi.name)] = roi.x2 - roi.x1
            settings['ROI {0:s} HEIGHT'.format(roi.name)] = roi.y2 - roi.y1

        tracker_extracted_video_data = tracker.create_section('tracker_extracted_video_data', 'metadata.video')
        tracker_extracted_video_data['Video width'] = data_manager.video_resolution[0]
        tracker_extracted_video_data['Video height'] = data_manager.video_resolution[1]

        # write meta data to nix
        for entry in meta_manager.meta_entries:
            try:
                meta_odml = odml.tools.xmlparser.load(entry.path)
            except Exception as e:
                print e
                print "could not read meta file {0:s} from {1:s}".format(entry.name, entry.path)
                continue
            section = nix_file.create_section(entry.name, "metadata")
            DataWriter.save_subsections(section, meta_odml, "metadata")

        # save data
        time_stamps = np.asarray(DataWriter.time_to_seconds(times))
        DataWriter.save_trace(time_stamps, data_manager.all_pos_original, block, 'positions', 'nix.irregular_sampled.coordinates', data_label='position', set_labels=['x', 'y'])
        DataWriter.save_trace(time_stamps, data_manager.estimated_pos_original, block, 'estimated positions', 'nix.irregular_sampled.coordinates', data_label='position', set_labels=['x', 'y'])
        DataWriter.save_trace(time_stamps, data_manager.all_oris, block, 'orientations', 'nix.irregular_sampled', data_label='orientation', set_labels=['degree'])
        DataWriter.save_trace(time_stamps, data_manager.estimated_oris, block, 'estimated_orientations', 'nix.irregular_sampled', data_label='orientation', set_labels=['degree'])
        DataWriter.save_trace(time_stamps, data_manager.all_oris_ratio, block, 'orientation_ratios', 'nix.irregular_sampled', data_label='orientaion_ratio', set_labels=['front_to_back_ratio'])
        DataWriter.save_trace(time_stamps, data_manager.number_contours_per_frame, block, 'object count', 'nix.irregular_sampled', data_label='count', set_labels=['amount'])
        DataWriter.save_trace(time_stamps, data_manager.number_relevant_contours_per_frame, block, 'fish object count', 'nix.irregular_sampled', data_label='count', set_labels=['amount'])

        for roi in roi_manager.roi_list:
            DataWriter.save_trace(time_stamps, roi.frame_data["{0:s}_mean_colors".format(roi.name)], block, 'ROI {0:s} mean colors'.format(roi.name), 'nix.irregular_sampled', data_label='count', set_labels=['r', 'g', 'b'])

        nix_file.close()

    @staticmethod
    def save_subsections(nix_section, template_section, info_type):
        if template_section.sections is not None and len(template_section.sections) > 0:
            for s in template_section.sections:
                nix_subsection = nix_section.create_section(s.name, info_type)
                for p in s.properties:
                    if isinstance(p.value, list):
                        nix_subsection[p.name] = str(p.value)
                    elif isinstance(p.value.value, unicode):
                        nix_subsection[p.name] = str(p.value.value)
                    elif p.value.value is None:
                        nix_subsection[p.name] = ""
                    else:
                        nix_subsection[p.name] = p.value.value
                DataWriter.save_subsections(nix_subsection, s, info_type)

if __name__ == "__main__":
    from DataManager import DataManager
    from MetaManager import MetaManager
    from ROIManager import ROIManager

    dm = DataManager()
    mm = MetaManager()
    rm = ROIManager()
    file_name = "test_file_name"
    mm.metadata_path = "/home/madai/Tracker/meta_templates/chripChamber_template.xml"

    DataWriter.write_nix(file_name, None, dm, rm, mm, None)
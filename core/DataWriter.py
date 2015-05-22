import collections
import numpy as np
import nix


class DataWriter(object):

    # @staticmethod
    # def fill_spaces(file, string):
    #     file.write(" " * (20 - len(string)))
    #
    # @staticmethod
    # def print_none_to_file(file):
    #     file.write(" " * 16)
    #     file.write("None")
    #
    # @staticmethod
    # def write_position(p, out_file, spacing):
    #     if p is None:
    #         DataWriter.print_none_to_file(out_file)
    #         out_file.write(" " * spacing)
    #     else:
    #         p = str(round(p, 2))
    #         DataWriter.fill_spaces(out_file, p)
    #         out_file.write(p)
    #         out_file.write(" " * spacing)

    # @staticmethod
    # def write_ascii(file_name, times, position, orientation, est_position, est_orientation, object_count, fish_object_count, roi, frame_count, parameters):
    #     """
    #      save data to text file
    #     """
    #     spacing = 4
    #     # out_dir = '/'.join(file_name.split('/')[:-1])
    #     # if not os.path.exists(out_dir):
    #     #     os.makedirs(out_dir)
    #
    #     none_count = 0
    #     for p in position:
    #         if p is None:
    #             none_count += 1
    #
    #     output_file = open(file_name, 'w')
    #     output_file.write("# Tracking parameters:\n")
    #     output_file.write("#     Region of Interest X-Axis         : [" + str(roi.x1) + "," + str(roi.x2) + "]\n")
    #     output_file.write("#     Region of Interest Y-Axis         : [" + str(roi.y1) + "," + str(roi.y2) + "]\n")
    #     output_file.write("#     Fish size threshold               : " + str(parameters['fish size']) + "\n")
    #     output_file.write("#     Start orientation                 : " + str(parameters['start ori']) + "\n")
    #     output_file.write("#     Fish starting area X-Axis         : [" + str(parameters['starting area x1']) + "," + str(parameters['starting area x2']) + "]\n")
    #     output_file.write("#     Fish starting area Y-Axis         : [" + str(parameters['starting area y1']) + "," + str(parameters['starting area y2']) + "]\n")
    #     output_file.write("#\n")
    #     output_file.write("#     Orientation algorithm assumes that fish can not turn more than >> 90 << degrees from one frame to the next\n")
    #     if none_count > 0:
    #         output_file.write("#\n")
    #         output_file.write("#     WARNING: Fish was not detected in " + str(none_count) + " of " + str(len(times)) + " frames. Orientation data may be incorrect.\n")
    #
    #     output_file.write("\n#Key\n")
    #     output_file.write("#           frame_time               pos_roi_x               pos_roi_y           est_pos_roi_x           est_pos_roi_y          pos_original_x          pos_original_y      est_pos_original_x      est_pos_original_y            orientations        est_orientations           obj_per_frame       fishobj_per_frame\n")
    #
    #     for i, t in enumerate(times):
    #         output_file.write("  ")
    #         DataWriter.fill_spaces(output_file, t)
    #         output_file.write(t)
    #         output_file.write(" " * spacing)
    #
    #         if i >= frame_count:
    #             return
    #         DataWriter.write_position(position[i][0] - roi.x1 if position[i] is not None else None, output_file, spacing) # x position roi
    #         DataWriter.write_position(position[i][1] - roi.y1 if position[i] is not None else None, output_file, spacing) # y position roi
    #         DataWriter.write_position(est_position[i][0] - roi.x1 if est_position[i] is not None else None, output_file, spacing) # estimated x position roi
    #         DataWriter.write_position(est_position[i][1] - roi.y1 if est_position[i] is not None else None, output_file, spacing) # estimated y position roi
    #
    #         DataWriter.write_position(position[i][0] if position[i] is not None else None, output_file, spacing) # x position
    #         DataWriter.write_position(position[i][1] if position[i] is not None else None, output_file, spacing) # y position
    #         DataWriter.write_position(est_position[i][0] if est_position[i] is not None else None, output_file, spacing) # estimated x position
    #         DataWriter.write_position(est_position[i][1] if est_position[i] is not None else None, output_file, spacing) # estimated y position
    #
    #         DataWriter.write_position(orientation[i], output_file, spacing) # orientation
    #         DataWriter.write_position(est_orientation[i], output_file, spacing) # estimated orientation
    #
    #
    #         cnt_of_frame = str(object_count[i])
    #         DataWriter.fill_spaces(output_file, cnt_of_frame)
    #         output_file.write(cnt_of_frame)
    #         output_file.write(" " * spacing)
    #
    #         rel_cnt_of_frame = str(fish_object_count[i])
    #         DataWriter.fill_spaces(output_file, rel_cnt_of_frame)
    #         output_file.write(rel_cnt_of_frame)
    #
    #         output_file.write("\n")
    #     output_file.close()

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

    # TODO ajdust to rois!!!
    @staticmethod
    def write_nix(file_name, times, data_manager, roi_manager, meta_manager, parameters):
        name = file_name.split('/')[-1].split('.')[0]
        nix_file = nix.File.open(file_name, nix.FileMode.Overwrite)
        block = nix_file.create_block(name, 'nix.tracking')

        # some metadata
        recording = nix_file.create_section('recording', 'recording')
        recording['Date'] = name.split('_')[0]
        recording['Experimenter'] = meta_manager.experimenter

        tracker = nix_file.create_section('Tracker', 'software.tracker')
        tracker['Version'] = 1.5
        tracker['Source location'] = 'https://github.com/bendalab/tracker'
        settings = tracker.create_section('settings', 'software.settings')
        settings['Fish min size threshold'] = parameters['fish_min_size']
        settings['Fish max size threshold'] = parameters['fish_max_size']
        settings['Fish max size enabled'] = parameters['fish_max_size_enabled']
        settings['Start orientation'] = parameters['fish_start_orientation']

        for roi in roi_manager.roi_list:
            settings['ROI {0:s} X'.format(roi.name)] = roi.x1
            settings['ROI {0:s} Y'.format(roi.name)] = roi.y1
            settings['ROI {0:s} WIDTH'.format(roi.name)] = roi.x2 - roi.x1
            settings['ROI {0:s} HEIGHT'.format(roi.name)] = roi.y2 - roi.y1

        movie = nix_file.create_section('Movie', 'recording.movie')
        movie['Filename'] = parameters['source file']

        camera = movie.create_section('Camera', 'hardware.camera')
        # camera['Model'] = 'Guppy F-038B NIR'
        # camera['Vendor'] = 'Allied Vision Technologies'
        # camera['Model'] = 'NA'
        # camera['Vendor'] = 'NA'

        # create sources and link entities to metadata
        block.metadata = recording
        movie_source = block.create_source('Original movie', 'nix.source.movie')
        movie_source.metadata = movie
        tracking_source = block.create_source('Video tracking', 'nix.source.analysis')
        tracking_source.metadata = tracker

        # save data
        time_stamps = np.asarray(DataWriter.time_to_seconds(times))
        a = DataWriter.save_trace(time_stamps, data_manager.all_pos_original, block, 'positions', 'nix.irregular_sampled.coordinates', data_label='position', set_labels=['x', 'y'])
        DataWriter.append_sources(a, [movie_source, tracking_source])

        a = DataWriter.save_trace(time_stamps, data_manager.estimated_pos_original, block, 'estimated positions', 'nix.irregular_sampled.coordinates', data_label='position', set_labels=['x', 'y'])
        DataWriter.append_sources(a, [movie_source, tracking_source])

        a = DataWriter.save_trace(time_stamps, data_manager.all_oris, block, 'orientations', 'nix.irregular_sampled', data_label='orientation', set_labels=['degree'])
        DataWriter.append_sources(a, [movie_source, tracking_source])

        a = DataWriter.save_trace(time_stamps, data_manager.estimated_oris, block, 'estimated_orientations', 'nix.irregular_sampled', data_label='orientation', set_labels=['degree'])
        DataWriter.append_sources(a, [movie_source, tracking_source])

        a = DataWriter.save_trace(time_stamps, data_manager.number_contours_per_frame, block, 'object count', 'nix.irregular_sampled', data_label='count', set_labels=['amount'])
        DataWriter.append_sources(a, [movie_source, tracking_source])

        a = DataWriter.save_trace(time_stamps, data_manager.number_relevant_contours_per_frame, block, 'fish object count', 'nix.irregular_sampled', data_label='count', set_labels=['amount'])
        DataWriter.append_sources(a, [movie_source, tracking_source])

        for roi in roi_manager.roi_list:
            a = DataWriter.save_trace(time_stamps, roi.frame_data["{0:s}_mean_colors".format(roi.name)], block, 'ROI {0:s} mean colors'.format(roi.name), 'nix.irregular_sampled', data_label='count', set_labels=['r', 'g', 'b'])
            DataWriter.append_sources(a, [movie_source, tracking_source])

        # TODO import of recording metadata from file
        nix_file.close()

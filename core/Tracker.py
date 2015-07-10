#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import cv2
import math
import sys
import copy
import os
import argparse
import ConfigParser
from ROI import ROI
from RelROI import RelROI
from ROIManager import ROIManager
from DataWriter import DataWriter
from ContourManager import ContourManager
from DataManager import DataManager
from ImageManager import ImageManager
from MetaManager import MetaManager
from IPython import embed

try:
    import nix
except ImportError as e:
    print e
    print 'Unfortunately your system misses the NIX packages.'
    quit()

class Tracker(object):
    def __init__(self, path=None, wait_time=50, controller=None, batch_mode_on=False):
        # program data
        self.ui_mode_on = False
        self.batch_mode_on = batch_mode_on
        self.ui_abort_button_pressed = False
        
        if path is not None:
            self.video_file = path

        self.output_directory = ""
        self.output_path_isset = False
        
        self.cap = None

        self.save_frames = False
        if wait_time > 0:
            self.frame_waittime = wait_time
        else:
            self.frame_waittime = 50

        # self.frame_counter = 0

        self.controller = controller
        if controller is not None:
            self.controller.connect_to_tracker(self)
            self.ui_mode_on = True

        self.read_cfg = None
        self.config_file_present = True
        self.init_read_cfg()
        self.write_cfg = ConfigParser.SafeConfigParser()

        # image morphing data
        self._erosion_iterations = 1
        self._dilation_iterations = 4

        # morphing matrix values
        self._erosion_matrix_value = 2
        self._dilation_matrix_value = 2

        # fish size thresholds
        self._fish_size_threshold = 700
        self._fish_max_size_threshold = 4000
        self._enable_max_size_threshold = False

        # Managers
        self.cm = ContourManager()
        self.dm = DataManager()
        self.im = ImageManager()
        self.mm = MetaManager()

        self.roim = ROIManager()

        if self.controller is not None:
            self.roim.add_roi(160, 80, 700, 525, "tracking_area", self.controller)  # Isabel setup
            self.roim.add_roi(300, 150, 600, 350, "starting_area", self.controller)
        else:
            self.roim.add_roi(160, 80, 700, 525, "tracking_area")  # Isabel setup
            self.roim.add_roi(300, 150, 600, 350, "starting_area")
        self.fish_started = False
        # self.starting_area = RelROI(0.85, 0.30, 1.00, 0.70)

        self._start_ori = 270

        self.fish_not_detected_threshold = 50
        self.fish_not_detected_threshold_reached = False

        self.ellipse = None
        # self.line = None

        # import config file values
        self.import_config_values()

    def init_read_cfg(self):
        self.read_cfg = ConfigParser.ConfigParser()

        if self.ui_mode_on:
            cfg_path = "tracker.cnf"
        else:
            cfg_path = "../tracker.cnf"

        if not os.path.exists(cfg_path):
            print "Couldn't import config data from file - file doesn't exist. Config file will be created at first Tracking."
            self.config_file_present = False
            print "set to false"
            return

        if self.ui_mode_on:
            cfg_file = open('tracker.cnf')
        else:
            cfg_file = open('../tracker.cnf')
        self.read_cfg.readfp(cfg_file)

    def import_config_values(self):
        if not self.config_file_present:
            return

        # meta manager values
        if not self.batch_mode_on:
            self.mm.import_cfg_values(self.read_cfg, self.controller)

        # image manager values
        self.im.import_cfg_values(self.read_cfg)

        # import rois
        roi_sections = [sec for sec in self.read_cfg.sections() if "roi" == sec.split("_")[0]]
        for roi_sec in roi_sections:
            add_roi_name = "_".join(roi_sec.split("_")[1:])
            if add_roi_name not in [roi.name for roi in self.roim.roi_list]:
                x1 = self.read_cfg.getint(roi_sec, "x1")
                y1 = self.read_cfg.getint(roi_sec, "x2")
                x2 = self.read_cfg.getint(roi_sec, "y1")
                y2 = self.read_cfg.getint(roi_sec, "y2")
                self.roim.add_roi(x1, y1, x2, y2, add_roi_name, self.controller)
            else:
                self.roim.get_roi(add_roi_name).import_cfg_values(self.read_cfg)

        # tracker values
        self._erosion_iterations = self.read_cfg.getint('image_morphing', 'erosion_factor')
        self._dilation_iterations = self.read_cfg.getint('image_morphing', 'dilation_factor')
        try:
            self._erosion_matrix_value = self.read_cfg.getint('image_morphing', 'erosion_matrix_value')
            self._dilation_matrix_value = self.read_cfg.getint('image_morphing', 'dilation_matrix_value')
        except:
            print "no entry for erosion or dilation matrix value. will be created at next tracking"

        self._start_ori = self.read_cfg.getint('detection_values', 'start_orientation')
        self._fish_size_threshold = self.read_cfg.getint('detection_values', 'min_area_threshold')
        self._fish_max_size_threshold = self.read_cfg.getint('detection_values', 'max_area_threshold')
        self._enable_max_size_threshold = self.read_cfg.getboolean('detection_values', 'enable_max_size_threshold')

        self.frame_waittime = self.read_cfg.getint('system', 'frame_waittime')

        # self._erosion_iterations = self.read_cfg.getint('image_morphing', 'erosion_factor')
        # self._dilation_iterations = self.read_cfg.getint('image_morphing', 'dilation_factor')

    def write_config_file(self):
        cfg = ConfigParser.SafeConfigParser()

        self.mm.add_cfg_values(cfg)

        cfg.add_section('system')
        cfg.set('system', 'frame_waittime', str(self.frame_waittime))

        self.roim.add_cfg_values(cfg)

        cfg.add_section('detection_values')
        cfg.set('detection_values', 'start_orientation', str(self.start_ori))
        cfg.set('detection_values', 'min_area_threshold', str(self.fish_size_threshold))
        cfg.set('detection_values', 'max_area_threshold', str(self.fish_max_size_threshold))
        cfg.set('detection_values', 'enable_max_size_threshold', str(self.enable_max_size_threshold))
        cfg.add_section('image_morphing')
        cfg.set('image_morphing', 'erosion_factor', str(self.erosion_iterations))
        cfg.set('image_morphing', 'dilation_factor', str(self.dilation_iterations))
        cfg.set('image_morphing', 'erosion_matrix_value', str(self.erosion_matrix_value))
        cfg.set('image_morphing', 'dilation_matrix_value', str(self.dilation_matrix_value))

        self.im.add_cfg_values(cfg)

        with open("tracker.cnf", 'w') as cfg_file:
            cfg.write(cfg_file)

    # sets video file to terminal-attribute path to video file
    def set_video_file(self):
        if len(sys.argv) > 1:
            self.video_file = sys.argv[1]
        else:
            return

    def set_output_path(self, path):
        self.output_directory = path
        self.output_path_isset = True

    def unset_output_path(self):
        self.output_directory = ""
        self.output_path_isset = False

    def check_if_necessary_files_exist(self):
        if not os.path.exists(self.video_file):
            raise Exception("ERROR: Video File <<{0:s}>> does not exist - Tracking aborted".format(self.video_file))

    def extract_video_file_name_and_path(self):
        parts = self.video_file.split('/')
        filename = parts[-1].split('.')[0]
        path = '/'.join(parts[:-1])
        if len(path) > 0:
            path += '/'
        return filename, path

    def get_output_file_and_dir(self, file_name, file_directory):
        if not self.output_path_isset:
            output_file_name = file_directory + file_name + "/" + file_name
            out_dir = '/'.join(output_file_name.split('/')[:-1])
            return output_file_name, out_dir
        else:
            output_file_name = self.output_directory + file_name + "/" + file_name
            out_dir = '/'.join(output_file_name.split('/')[:-1])
            return output_file_name, out_dir

    # captures video defined by path stored in video file
    def set_video_capture(self):
        print self.video_file
        self.cap = cv2.VideoCapture(self.video_file)
        self.dm.video_resolution = (self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH), self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))

    # # morph given img by erosion/dilation
    def morph_img(self, img):
        # erode img
        er_kernel = np.ones((self._erosion_matrix_value, self._erosion_matrix_value), np.uint8)
        er_img = cv2.erode(img, er_kernel, iterations=self._erosion_iterations)
        # dilate img
        di_kernel = np.ones((self._dilation_matrix_value, self._dilation_matrix_value), np.uint8)
        di_img = cv2.dilate(er_img, di_kernel, iterations=self._dilation_iterations)
        # thresholding to black-white
        ret, morphed_img = cv2.threshold(di_img, 127, 255, cv2.THRESH_BINARY)
        return ret, morphed_img

    # check if fish started from the right side
    def check_if_fish_started(self):
        starting_area_x1 = self.roim.get_roi("starting_area").x1 - self.roim.get_roi("tracking_area").x1
        starting_area_x2 = self.roim.get_roi("starting_area").x2 - self.roim.get_roi("tracking_area").x1
        starting_area_y1 = self.roim.get_roi("starting_area").y1 - self.roim.get_roi("tracking_area").y1
        starting_area_y2 = self.roim.get_roi("starting_area").y2 - self.roim.get_roi("tracking_area").y1

        if self.cm.contour_list is not None:
            for i in range(0, len(self.cm.contour_list)):
                cnt = self.cm.contour_list[i]
                ellipse = cv2.fitEllipse(cnt)
                if starting_area_x1 < ellipse[0][0] < starting_area_x2 and starting_area_y1 < ellipse[0][1] < starting_area_y2:
                    self.fish_started = True

    # fitting ellipse onto contour
    def fit_ellipse_on_contour(self):
        if self.cm.contour_list is None or len(self.cm.contour_list) == 0:
            self.ellipse = None
        elif self.cm.contour_list is not None and len(self.cm.contour_list) > 0:
            if len(self.cm.contour_list) > 0:
                cnt = self.cm.contour_list[0]
                self.ellipse = cv2.fitEllipse(cnt)
                ## center: ellipse[0]
                ## size  : ellipse[1]
                ## angle : ellipse[2]

    def extract_data(self):
        # create BG subtractor
        # bg_sub = cv2.BackgroundSubtractorMOG(100, 5, 0.5, 0)
        bg_sub = cv2.BackgroundSubtractorMOG()

        self.roim.check_and_adjust_rois(self.cap, self.controller)

        roi = self.roim.get_roi("tracking_area")

        # main loop
        while self.cap.isOpened():
            ret, frame = self.cap.read()

            if frame is None:
                break

            self.im.current_frame = frame

            self.dm.frame_counter += 1

            # # TODO REMOVE AFTER TESTING
            # if self.dm.frame_counter < 400:
            #     continue

            # set region of interest ROI
            roi_img = copy.copy(frame[roi.y1:roi.y2, roi.x1:roi.x2])

            if self.dm.frame_counter == 1:
                self.im.overview_output = copy.copy(frame)

            # subtract background fro ROI
            self.im.current_bg_sub = bg_sub.apply(roi_img)

            # morph img
            ret, self.im.current_morphed = self.morph_img(self.im.current_bg_sub)

            # getting contours (of the morphed img)
            self.cm.contour_list, hierarchy = cv2.findContours(copy.copy(self.im.current_morphed), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

            # save amount of contours
            self.dm.save_number_of_contours(self.cm.contour_list, self.dm.number_contours_per_frame)

            # everything below fish_size_threshold is being ignored
            self.cm.del_small_contours(self.fish_size_threshold)

            # everything above fish_size_max_threshold is being ignored
            if self._enable_max_size_threshold:
                self.cm.del_oversized_contours(self.fish_max_size_threshold)

            # save number of remaining contours
            self.dm.save_number_of_contours(self.cm.contour_list, self.dm.number_relevant_contours_per_frame)

            # check if fish started
            if not self.fish_started:
                self.check_if_fish_started()

            # if fish hasn't started yet, delete all contours
            if not self.fish_started:
                self.cm.contour_list = []

            # keep only biggest contours
            self.cm.keep_biggest_contours()

            # if two or more contours (of same size) in list delete which is farthest away from last point
            if self.fish_started and self.cm.contour_list is not None and len(self.cm.contour_list) > 1:
                self.cm.keep_nearest_contour(self.dm.last_pos, self.roim.get_roi("tracking_area"))

            # fit ellipse on contour
            self.fit_ellipse_on_contour()

            # get line from ellipse
            if self.fish_started and self.ellipse is not None:
                self.im.get_line_from_ellipse(self.ellipse)

            # set last_pos to ellipse center
            self.dm.set_last_pos(self.cm.contour_list)
            # self.dm.set_last_mean_mid(self.ellipse, self.cm.contour_list, self.roim)

            # save fish positions
            self.dm.save_fish_positions(self.roim.get_roi("tracking_area"))

            # set last orientation
            self.dm.set_last_orientation(self.ellipse, self.fish_started, self.start_ori)

            self.dm.calc_ori_boxes(self.cm.contour_list, self.im)

            # save orientations
            self.dm.save_fish_orientations(self.ellipse, self.fish_started)

            # calculate roi data
            # self.roim.check_and_adjust_rois(self.cap, self.controller)
            self.roim.calc_roi_data(frame)

            # draw current preview
            self.im.draw_preview_img(self.ellipse, self.dm, self.fish_started, self.cm.contour_list, self.roim.get_roi("tracking_area"))

            # show all imgs
            self.im.show_imgs()

            # show output img
            # if not self.ui_mode_on:
            #     cv2.imshow("contours", roi_img)

            if self.controller is not None:
                self.controller.update_progress(self.cap, self.dm.frame_counter)

            if cv2.waitKey(self.frame_waittime) & 0xFF == 27:
                break
            if self.ui_abort_button_pressed:
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def load_frame_times(self, file_name):
        print "debug"
        print file_name
        # times_file = None
        if os.path.exists(file_name):
            print "exists oO"
        if not os.path.exists(file_name):
            print "doesnt exist oO"
            print "It seems that your times file is missing. It should be named [video_file_name]_times.dat.\n" \
                  "If you dont have such a file, you can approximate your frame times with the TimesApproximator.py\n" \
                  "in the tools folder."
            raise Exception("ERROR: times file missing - data saving abortet")
        
        with open(file_name, 'r') as f:
            times = map(lambda x: x.strip(), f)
        return times


        
    def run(self):
        # self.set_video_file()
        self.check_if_necessary_files_exist()
        self.set_video_capture()

        self.extract_data()
        self.dm.estimate_missing_pos(self.roim.get_roi("tracking_area"))
        self.dm.estimate_missing_ori()
        self.im.draw_data_on_overview_image(self.roim.get_roi("tracking_area"), self.dm)
        self.im.draw_estimated_data_on_overview_image(self.dm.estimated_pos_roi, self.roim.get_roi("tracking_area"), self.im.circle_size)

        self.dm.copy_original_to_est_data()

        # self.print_data()
        self.dm.check_frames_missing_fish(self.fish_not_detected_threshold)

        file_name, file_directory = self.extract_video_file_name_and_path()
        if file_name == "":
            return

        times = self.load_frame_times(file_directory + file_name + "_times.dat")
        output_file_name, out_dir = self.get_output_file_and_dir(file_name, file_directory)

        # TODO add video size
        params = {}
        params['source file'] = self.video_file
        params['fish_min_size'] = self._fish_size_threshold
        params['fish_max_size'] = self._fish_max_size_threshold
        params['fish_max_size_enabled'] = str(self._enable_max_size_threshold)
        params['fish_start_orientation'] = self._start_ori
        params['erosion_iterations'] = self._erosion_iterations
        params['dilation_iterations'] = self._dilation_iterations
        params['erosion_matrix_value'] = self._erosion_matrix_value
        params['dilation_matrix_value'] = self._dilation_matrix_value

        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        DataWriter.write_nix(output_file_name + ".h5", times, self.dm, self.roim, self.mm, params)
        cv2.imwrite(output_file_name + "_OV_path.png", self.im.overview_output)

        self.write_config_file()

        self.dm.check_data_integrity()

    # @property
    # def roi(self):
    #     return self._roi

    @property
    def erosion_iterations(self):
        return self._erosion_iterations

    @erosion_iterations.setter
    def erosion_iterations(self, value):
        self._erosion_iterations = value

    @property
    def dilation_iterations(self):
        return self._dilation_iterations

    @dilation_iterations.setter
    def dilation_iterations(self, value):
        self._dilation_iterations = value

    @property
    def erosion_matrix_value(self):
        return self._erosion_matrix_value
    @erosion_matrix_value.setter
    def erosion_matrix_value(self, value):
        self._erosion_matrix_value = value

    @property
    def dilation_matrix_value(self):
        return self._dilation_matrix_value
    @dilation_matrix_value.setter
    def dilation_matrix_value(self, value):
        self._dilation_matrix_value = value

    @property
    def fish_size_threshold(self):
        return self._fish_size_threshold

    @fish_size_threshold.setter
    def fish_size_threshold(self, value):
        self._fish_size_threshold = value
        self.cm.fish_max_size_threshold = self.fish_size_threshold

    @property
    def fish_max_size_threshold(self):
        return self._fish_max_size_threshold

    @fish_max_size_threshold.setter
    def fish_max_size_threshold(self, value):
        self._fish_max_size_threshold = value
        self.cm.fish_max_size_threshold = self.fish_max_size_threshold

    @property
    def enable_max_size_threshold(self):
        return self._enable_max_size_threshold

    @enable_max_size_threshold.setter
    def enable_max_size_threshold(self, bool):
        self._enable_max_size_threshold = bool

    @property
    def start_ori(self):
        return self._start_ori

    @start_ori.setter
    def start_ori(self, value):
        self._start_ori = value


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tracking fish in video file')
    parser.add_argument('paths', type=str, nargs="*", help="absolute file paths to video including file name and file extension")
    parser.add_argument('-w', '--wait_time', type=int, default=1,
                        help="display time of watch frame in ms.")

    args = parser.parse_args()
    for path in args.paths:
        if not os.path.exists(path):
            print('File does not exist!')
            continue
        tr = Tracker(path=path, wait_time=args.wait_time)
        tr.run()

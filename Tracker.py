import numpy as np
import cv2
import math
import sys
import copy
import argparse


FRAME_WAITTIME = 25

frame_counter = 0

DRAW_CONTOUR = False

DRAW_ELLIPSE = True
ellipse = None

DRAW_LINE = True
line_point_offset = 5
line = None
lx1 = 0
ly1 = 0
lx2 = 0
ly2 = 0

DRAW_TRAVEL_ORIENTATION = True
img_travel_orientation = []

DRAW_TRAVEL_ROUTE = True
img_travel_route = []
DRAW_ORIGINAL_OUTPUT = True

# set region of interest (ROI)
ROI_X1 = 15
ROI_X2 = 695
ROI_Y1 = 80
ROI_Y2 = 515


fish_size_threshold = 700

fish_started = False

# init last position and lists for saving
last_pos = None
all_pos_roi = []
all_pos_original = []

# init last orientation and list for saving
last_ori = None
all_oris = []

last_frame = None
last_frame_OV_output = None



# define testvideo
# path to directory
dir = "examples/"

# videofile_name = "2014-10-02_5"
# videofile_name = "2014-10-02_27"
videofile_name = "2014-10-01_33"
# videofile_name = "2014-10-01_31"
video_file = dir + videofile_name + ".avi"

# sets video file to terminal-attribute path to video file
def set_video_file():
    if len(sys.argv) > 1:
        global video_file
        video_file = sys.argv[1]
    else:
        return


# init cap
cap = ""

# captures video defined by path stored in video file
def set_video_capture():
    global cap
    cap = cv2.VideoCapture(video_file)


# create and position windows
cv2.namedWindow("file")
cv2.moveWindow("file", 0, 0)
cv2.namedWindow("ROI")
cv2.moveWindow("ROI", 1300, 0)
cv2.namedWindow("Background subtracted")
cv2.moveWindow("Background subtracted", 0, 600)

cv2.namedWindow("morphed")
cv2.moveWindow("morphed", 1300, 600)

cv2.namedWindow("canny")
cv2.moveWindow("canny", 600, 70)

cv2.namedWindow("contours")
cv2.moveWindow("contours", 570, 570)


# temporary function
# show images
def show_imgs(img, roi, roi_bg_subtracted, roi_bg_subtracted_morphed, canny_edges):

    # show original output
    cv2.imshow('file', img)

    # show original ROI
    cv2.imshow('ROI', roi)

    # show ROI with subtracted BG
    cv2.imshow('Background subtracted', roi_bg_subtracted)

    # show morphed subtracted BG-img
    cv2.imshow("morphed", roi_bg_subtracted_morphed)

    # show ROI img with canny edge detection
    cv2.imshow("canny", canny_edges)

    return


##########################################################################################
##########################################################################################
# serious stuff starts here

# morph given img by erosion/dilation
def morph_img(img):
    # erode img
    er_kernel = np.ones((6, 6), np.uint8)
    er_img = cv2.erode(img, er_kernel, iterations=1)
    # dilate img
    di_kernel = np.ones((5,5), np.uint8)
    di_img = cv2.dilate(er_img, di_kernel, iterations=4)
    # thresholding to black-white
    ret, morphed_img = cv2.threshold(di_img, 127, 255, cv2.THRESH_BINARY)
    return  ret, morphed_img



# set a threshold for area. all contours with smaller area get deleted
def del_small_contours(contour_list):
    area_threshold = fish_size_threshold
    if len(contour_list) > 0:

        counter = 0
        while counter < len(contour_list):

            popped = False

            # print "contour nr" + str(counter) + ": area  = " + str(cv2.contourArea(contour_list[counter]))
            if cv2.contourArea(contour_list[counter]) < area_threshold:
                contour_list.pop(counter)
                popped = True
            if not popped:
                # print(cv2.contourArea(contour_list[counter]))
                counter += 1
    return contour_list



# only keep biggest-area object in contour list
def keep_biggest_contours(contour_list):
    if len(contour_list) == 0:
        return

    biggest = cv2.contourArea(contour_list[0])

    counter = 1
    while counter < len(contour_list):
        next_size = cv2.contourArea(contour_list[counter])
        if next_size < biggest:
            contour_list.pop(counter)
        elif next_size > biggest:
            biggest = next_size
            contour_list.pop(counter-1)
        else:
            counter += 1

    return contour_list



# calculates distance of two given points (tuples)
def calculate_distance(p1, p2):
    x_diff = p2[0] - p1[0]
    y_diff = p2[1] - p1[1]
    dist = math.sqrt(x_diff*x_diff + y_diff*y_diff)
    return dist

# get center of contour based on fitting ellipse
def get_center(cnt):
    ellipse = cv2.fitEllipse(cnt)
    return ellipse[0]

# if two or more contours (of same size) in contour_list delete which is farthest away from last pos fish was
def keep_nearest_contour(contour_list):

    global last_pos
    if last_pos is None:
        last_pos = (ROI_Y2-ROI_Y1, int((ROI_X2-ROI_X1)/2))

    cnt_center = get_center(ellipse[0])
    biggest_dist= calculate_distance(cnt_center, last_pos)

    counter = 1
    while counter < len(contour_list):
        next_center = get_center(ellipse[counter])
        next_dist = calculate_distance(next_center, last_pos)
        if next_dist < biggest_dist:
            contour_list.pop(counter)
        elif next_dist > biggest_dist:
            biggest_dist = next_dist
            contour_list.pop(counter-1)
        else:
            counter += 1

    return contour_list



# check if fish started from the right side
def check_if_fish_started(contour_list, roi):
    height, width, depth = roi.shape
    non_starting_area_x = int(0.85 * width)
    non_starting_area_y1 = int(0.30 * height)
    non_starting_area_y2 = int(0.70 * height)

    for i in range(0, len(contour_list)):
        cnt = contour_list[i]
        ellipse = cv2.fitEllipse(cnt)
        if ellipse[0][0] > non_starting_area_x and ellipse[0][1] > non_starting_area_y1 and ellipse[0][1] < non_starting_area_y2:
            global fish_started
            fish_started = True



# fitting ellipse onto contour
def fit_ellipse_on_contour(contour_list):
    if contour_list != None and len(contour_list) > 0:
        if len(contour_list) > 0:
            cnt = contour_list[0]
            ellipse = cv2.fitEllipse(cnt)
            ## center: ellipse[0]
            ## size  : ellipse[1]
            ## angle : ellipse[2]
            # print ellipse
            return ellipse


# calculates start and endpoint for a line displaying the orientation of given ellipse (thus of the fish)
def get_line_from_ellipse(ellipse):

    center_x = ellipse[0][0]
    center_y = ellipse[0][1]
    grade_angle = -1 * ellipse[2]
    # print "ellipse angle: " +  str(ellipse[2])
    # print "  grade angle: " + str(grade_angle)
    angle_prop = grade_angle/180
    angle = math.pi*angle_prop
    # print "        angle: " + str(angle)

    x_dif = math.sin(angle)
    y_dif = math.cos(angle)

    x1 = int(round(center_x - line_point_offset*x_dif))
    y1 = int(round(center_y - line_point_offset*y_dif))
    x2 = int(round(center_x + line_point_offset*x_dif))
    y2 = int(round(center_y + line_point_offset*y_dif))

    return x1, y1, x2, y2

def append_to_travel_orientation(lx1, ly1, lx2, ly2):
    coordinates = (lx1, ly1, lx2, ly2)
    img_travel_orientation.append(coordinates)

def append_to_travel_route(ellipse):
    if ellipse != None:
        ellipse_x = int(round(ellipse[0][0]))
        ellipse_y = int(round(ellipse[0][1]))
        point = (ellipse_x, ellipse_y)
        img_travel_route.append(point)

def set_last_pos(ellipse):
    if ellipse is None:
        return
    else:
        global last_pos
        last_pos = ellipse[0]

def save_fish_positions():
    global last_pos
    all_pos_roi.append(last_pos)
    if last_pos is None:
        all_pos_original.append(last_pos)
    else:
        original_x = last_pos[0]+ROI_X1
        original_y = last_pos[1]+ROI_Y1
        all_pos_original.append((original_x,original_y))

def set_last_orientation(ellipse):
    if not fish_started or ellipse is None:
        return

    global last_ori
    if last_ori is None:
        last_ori = 270

    ell_ori = ellipse[2]
    if last_ori > ell_ori:
        ori_diff = last_ori - ell_ori
        if ori_diff > 270:
            last_ori = ell_ori
        elif ori_diff < 90:
            last_ori = ell_ori
        else:
            last_ori = (ell_ori + 180) % 360
    if last_ori < ell_ori:
        ori_diff = ell_ori - last_ori
        if ori_diff < 90:
            last_ori = ell_ori % 360
        else:
            last_ori = (ell_ori + 180) % 360

def save_fish_orientations():
    if not fish_started:
        all_oris.append(None)
        return

    global last_ori
    all_oris.append(last_ori)



def run_Tracker():

    # create BG subtractor
    bg_sub = cv2.BackgroundSubtractorMOG2()

    # main loop
    while cap.isOpened():


        ret, frame = cap.read()

        if frame is None:
            break

        # set region of interest ROI
        roi = copy.copy(frame[ROI_Y1:ROI_Y2, ROI_X1:ROI_X2])
        roi_output = copy.copy(roi)

        frame_output = copy.copy(frame)

        # subtract background fro ROI
        roi_bg_sub = bg_sub.apply(roi)

        # morph img
        ret, mo_roi_bg_sub = morph_img(roi_bg_sub)

        # detect edges of bg-deleted img
        edges = cv2.Canny(roi_bg_sub, 500, 500)

        # detect edges of morphed img (not displayed)
        mo_edges = cv2.Canny(mo_roi_bg_sub, 500, 500)


        # getting contours (of the morphed img)
        ret,thresh_img = cv2.threshold(mo_roi_bg_sub,127,255,cv2.THRESH_BINARY)
        contour_list, hierarchy = cv2.findContours(thresh_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)


        # everything below fish_size_threshold is being ignored
        contour_list = del_small_contours(contour_list)

        # check if fish started
        if not fish_started:
            check_if_fish_started(contour_list, roi)

        # if fish hasn't started yet, delete all contours
        if not fish_started:
            contour_list = []

        # keep only biggest contours
        contour_list = keep_biggest_contours(contour_list)


        # if two or more contours (of same size) in list delete which is farthest away from last point
        if fish_started and contour_list is not None and len(contour_list) > 1:
            contour_list = keep_nearest_contour(contour_list)


        # draw countours to ROI img and show img
        if DRAW_CONTOUR:
            cv2.drawContours(roi, contour_list, -1, (0,255,0), 3)

        # fit ellipse on contour
        ellipse =  fit_ellipse_on_contour(contour_list)
        # draw ellipse
        if DRAW_ELLIPSE and ellipse is not None and fish_started:
            cv2.ellipse(roi,ellipse,(0, 0, 255),2)

        # get line from ellipse
        if fish_started and ellipse is not None:
            lx1, ly1, lx2, ly2 = get_line_from_ellipse(ellipse)
        # draw line
        if DRAW_LINE and ellipse is not None:
            cv2.line(roi, (lx1, ly1), (lx2, ly2), (0,0,255), 1)


        # append ellipse center to travel route
        if DRAW_TRAVEL_ROUTE:
            append_to_travel_route(ellipse)

        # set last_pos to ellipse center
        set_last_pos(ellipse)

        # save fish positions
        save_fish_positions()

        # set last orientation
        set_last_orientation(ellipse)

        # save orientations
        save_fish_orientations()

        # append coordinates to travel_orientation
        if DRAW_TRAVEL_ORIENTATION and fish_started:
            append_to_travel_orientation(lx1, ly1, lx2, ly2)


        # draw travel route
        if DRAW_TRAVEL_ORIENTATION:
            for coordinates in img_travel_orientation:
                cv2.line(roi, (coordinates[0], coordinates[1]), (coordinates[2], coordinates[3]), (150,150,0), 1)

        # draw travel orientation
        if DRAW_TRAVEL_ROUTE:
            for point in img_travel_route:
                cv2.circle(roi, point, 2, (255, 0, 0))

        if DRAW_ORIGINAL_OUTPUT:
            for coordinates in img_travel_orientation:
                cv2.line(frame_output, (coordinates[0]+ROI_X1, coordinates[1]+ROI_Y1), (coordinates[2]+ROI_X1, coordinates[3]+ROI_Y1), (150,150,0), 1)
            for point in all_pos_original:
                if point is not None:
                    cv2.circle(frame_output, (int(round(point[0])), int(round(point[1]))), 2, (255, 0, 0))



        # show all imgs
        if DRAW_ORIGINAL_OUTPUT:
            show_imgs(frame_output, roi_output, roi_bg_sub, mo_roi_bg_sub, edges)
        else:
            show_imgs(frame, roi_output, roi_bg_sub, mo_roi_bg_sub, edges)

        # show output img
        cv2.imshow("contours", roi)

        global frame_counter
        frame_counter += 1

        global last_frame
        last_frame = roi
        global last_frame_OV_output
        last_frame_OV_output = frame_output

        if cv2.waitKey(FRAME_WAITTIME) & 0xFF == 27:
            break


    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='tracking fish in video file')
    # parser.add_argument('path', type=str,
    #                     help="absolute file path to video including file name")
    # args = parser.parse_args()

    set_video_file()
    set_video_capture()

    run_Tracker()
    cv2.namedWindow("result")
    cv2.moveWindow("result", 200, 350)
    if DRAW_ORIGINAL_OUTPUT:
        cv2.namedWindow("result_ov")
        cv2.moveWindow("result_ov", 900, 350)

    # print all_pos_roi
    # print all_pos_original
    # print all_oris

    cv2.imshow("result", last_frame)
    if DRAW_ORIGINAL_OUTPUT:
        cv2.imshow("result_ov", last_frame_OV_output)
    cv2.waitKey(0)
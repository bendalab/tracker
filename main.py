import numpy as np
import cv2


FRAME_WAITTIME = 10

DRAW_CONTOUR = True

DRAW_ELLIPSE = False
ellipse = None

DRAW_LINE = False
line = None

DRAW_TRAVEL_ROUTE = True

travel_route = []

ROI_X1 = 80
ROI_X2 = 515
ROI_Y1 = 15
ROI_Y2 = 695


fish_started = False


# define testvideo
# path to directory
dir = "examples/"

# videofile_name = "2014-10-02_5"
# videofile_name = "2014-10-02_27"
videofile_name = "2014-10-01_33"
# videofile_name = "2014-10-01_31"
testVid = dir + videofile_name + ".avi"

# capture video
cap = cv2.VideoCapture(testVid)

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


##########################################################################################
##########################################################################################
# serious stuff starts here

# morph given img by erosion/dilation
def morph_img(img):
    # erode img
    er_kernel = np.ones((5, 5), np.uint8)
    er_img = cv2.erode(img, er_kernel, iterations = 1)
    # dilate img
    di_kernel = np.ones((5,5), np.uint8)
    di_img = cv2.dilate(er_img,di_kernel,iterations = 4)
    # thresholding to black-white
    ret, morphed_img = cv2.threshold(di_img, 127, 255, cv2.THRESH_BINARY)
    return  ret, morphed_img



# set a threshold for area. all contours with smaller area get deleted
def del_small_contours(contour_list, threshold):
    area_threshold = threshold
    if (len(contour_list) > 0 ):

        counter = 0
        while (counter < len(contour_list)):

            popped = False

            # print "contour nr" + str(counter) + ": area  = " + str(cv2.contourArea(contour_list[counter]))
            if (cv2.contourArea(contour_list[counter]) < area_threshold):
                contour_list.pop(counter)
                popped = True
            if not popped:
                # print(cv2.contourArea(contour_list[counter]))
                counter += 1
    return contour_list


# only keep biggest-area object in contour list
def keep_biggest_contours(contour_list):
    if (len(contour_list) == 0):
        return

    biggest = cv2.contourArea(contour_list[0])

    counter = 1
    while (counter < len(contour_list)):
        next_size = cv2.contourArea(contour_list[counter])
        if (next_size < biggest):
            contour_list.pop(counter)
        elif (next_size > biggest):
            biggest = next_size
            contour_list.pop(counter-1)
        else:
            counter += 1

    return contour_list

def fit_ellipse_on_contour(contour_list):
    if (contour_list != None and len(contour_list) > 0):
        if (len(contour_list) > 0):
            cnt = contour_list[0]
            ellipse = cv2.fitEllipse(cnt)
            ## center: ellipse[0]
            ## size  : ellipse[1]
            ## angle : ellipse[2]
            print ellipse
            return ellipse

def fit_line_on_contour(contour_list):
    if (contour_list != None and len(contour_list) > 0):
        cnt = contour_list[0]
        line = cv2.fitLine(cnt, cv2.DIST_LABEL_PIXEL, 0, 0.01, 0.01)
        return line

def append_to_travel_route(ellipse):
    if (ellipse != None):
        ellipse_x = int(round(ellipse[0][0]))
        ellipse_y = int(round(ellipse[0][1]))
        point = (ellipse_x, ellipse_y)
        travel_route.append(point)

if __name__ == '__main__':

    # create BG subtractor
    bg_sub = cv2.BackgroundSubtractorMOG2()

    # main loop
    while(cap.isOpened()):
        ret, frame = cap.read()

        if (frame == None):
            break

        # set region of interest ROI
        roi = frame[ROI_X1:ROI_X2, ROI_Y1:ROI_Y2]


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


        # set a threshold for object area. everything below threshold is ignored
        threshold = 700
        contour_list = del_small_contours(contour_list, threshold)

        # keep only biggest contours
        contour_list = keep_biggest_contours(contour_list)

        # TODO check  if fish already started, if not, delete contours
        # if fish not yet started, delete contours


        # TODO if two contours (of same size) in list delete which is farthest away from last point


        # show all imgs
        show_imgs(frame, roi, roi_bg_sub, mo_roi_bg_sub, edges)

        # draw countours to ROI img and show img
        if (DRAW_CONTOUR):
            cv2.drawContours(roi, contour_list, -1, (0,255,0), 3)

        # fit ellipse on contour
        ellipse =  fit_ellipse_on_contour(contour_list)
        # draw ellipse
        if (DRAW_ELLIPSE and ellipse != None):
            cv2.ellipse(roi,ellipse,(0, 0, 255),2)

        # fit line on contour
        line = fit_line_on_contour(contour_list)
        # draw line
        if (DRAW_LINE and line != None):
            vx = line[0]
            vy = line[1]
            # gradient = vx/vy

            x1 = line[2]
            y1 = line[3]
            x2 = x1 + vx*200
            y2 = y1 + vy*200
            x3 = x1 - vx*20
            y3 = y1 - vy*20

            cv2.line(roi, (x2, y2), (x3, y3), (0, 0, 255), 2)

        # append ellipse center to travel route
        if (DRAW_TRAVEL_ROUTE):
            append_to_travel_route(ellipse)


        # draw travel route
        if (DRAW_TRAVEL_ROUTE):
            for point in travel_route:
                cv2.circle(roi, point, 2, (255, 0, 0))

        # show output img
        cv2.imshow("contours", roi)


        if cv2.waitKey(FRAME_WAITTIME) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()



import numpy as np
import cv2

# print cv2.__version__


# TODO
# 0. define path with given arguments
#
# 1. define region of interest ROI
#   - extract white area of frame 1
# 2.


WAITKEY = 50


# define testvideo
dir = "examples/"
# date = "2014-10-02_5"
# date = "2014-10-02_27"
date = "2014-10-01_33"
testVid = dir + date + ".avi"

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

# create BG subtractor
bg_sub = cv2.BackgroundSubtractorMOG2()

while(cap.isOpened()):
    ret, frame = cap.read()

    if (frame == None):
        break

    # set region of interest ROI
    roi = frame[80:515, 15:695]

    # show original output
    cv2.imshow('file', frame)

    # show original ROI
    cv2.imshow('ROI', roi)

    # subtract background fro ROI
    roi_bg_sub = bg_sub.apply(roi)
    cv2.imshow('Background subtracted', roi_bg_sub)


    # erode img
    er_kernel = np.ones((5,5),np.uint8)
    er_roi_bg_sub = cv2.erode(roi_bg_sub, er_kernel, iterations = 1)
    # dilate img
    di_kernel = np.ones((5,5),np.uint8)
    di_roi_bg_sub = cv2.dilate(er_roi_bg_sub,di_kernel,iterations = 1)

    # set morphed output
    mo_roi_bg_sub = di_roi_bg_sub

    # show morphed image
    cv2.imshow("morphed", mo_roi_bg_sub)

    # # dilate edges of bg-deleted img
    # dilate_kernel = np.ones((3,3),np.uint8)
    # dilated_roi_bg_sub = cv2.dilate(roi_bg_sub,dilate_kernel,iterations = 1)
    # detect edges of bg-deleted img
    edges = cv2.Canny(roi_bg_sub, 500, 500)

    # detect edges of morphed img (not displayed)
    mo_edges = cv2.Canny(mo_roi_bg_sub, 500, 500)

    # edges = cv2.Canny(roi, 100, 200)
    cv2.imshow("canny", edges)


    #########################################################
    # things i don't understand yet

    # getting contours (of the canny img)
    ret,thresh_img = cv2.threshold(mo_edges,127,255,cv2.THRESH_BINARY)
    contour_list, hierarchy = cv2.findContours(thresh_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)


    if (len(contour_list) > 0 ):

        counter = 0
        while (counter < len(contour_list)):

            popped = False

            print "contour nr" + str(counter) + ": area  = " + str(cv2.contourArea(contour_list[counter]))
            if (cv2.contourArea(contour_list[counter]) < 300):
                contour_list.pop(counter)
                popped = True
            if not popped:
                counter += 1
        #
        #
        # draw countours to ROI img and show img
        print "contour list:" + str(contour_list)
        cv2.drawContours(roi, contour_list, -1, (0,255,0), 3)
        cv2.imshow("contours", roi)




    if cv2.waitKey(WAITKEY) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
import numpy as np
import cv2


FRAME_WAITTIME = 25


# define testvideo
# path to directory
dir = "examples/"

# videofile_name = "2014-10-02_5"
# videofile_name = "2014-10-02_27"
videofile_name = "2014-10-01_33"
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
    er_kernel = np.ones((5, 5),np.uint8)
    er_img = cv2.erode(img, er_kernel, iterations = 1)
    # dilate img
    di_kernel = np.ones((5,5),np.uint8)
    di_img = cv2.dilate(er_img,di_kernel,iterations = 4)
    # thresholding to easy black-white
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



if __name__ == '__main__':

    # create BG subtractor
    bg_sub = cv2.BackgroundSubtractorMOG2()

    # main loop
    while(cap.isOpened()):
        ret, frame = cap.read()

        if (frame == None):
            break

        # set region of interest ROI
        roi = frame[80:525, 15:695]


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
        contour_list, hierarchy = cv2.findContours(thresh_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)


        # set a threshold for object area. everything below threshold is ignored
        threshold = 700
        contour_list = del_small_contours(contour_list, threshold)


        # show all imgs
        show_imgs(frame, roi, roi_bg_sub, mo_roi_bg_sub, edges)


        # draw countours to ROI img and show img
        # print "contour list:" + str(contour_list)
        cv2.drawContours(roi, contour_list, -1, (0,255,0), 3)
        cv2.imshow("contours", roi)





        if cv2.waitKey(FRAME_WAITTIME) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()



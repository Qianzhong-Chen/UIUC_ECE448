#!/usr/bin/env python

'''

lab6pkg_improc/lab6_img.py

@brief: image processing for lab6, including template matching, image filtering, edge detection, contour detection, etc.
@author: Songjie Xiao
@date: Monday 2023/3/20

'''

#########################################################################
#
#  Lab 6-Image Processing
#  Main task is to pick and place all the blocks to your destination.
#  Camera is used to detect blocks. With image processing methods, 
#  robot is able to know the position, shape and orientation of the blocks.
#  Since block's position is based on image coordinate, what we should do
#  is to transform it into robot coordinate.
# 
#  In this lab, you only need to complete the image processing part.
#
#########################################################################

import cv2
import numpy as np

class ImageProcess():
    def __init__(self):

        self.contours_elip = []
        self.contours_rect = []

    def template_process(self, img_path):

        # read image from img_path
        img_temp = cv2.imread(img_path)

        if img_temp is None:
            print('Template Image is None, Please check image path!')
            return
        
        img_copy = img_temp.copy()

        # Bilateral Filter smooths images while preserving edges,
        # by means of a nonlinear combination of nearby image values.
        # cv2.bilateralFilter(src, d, sigmaColor, sigmaSpace)
        # d - Diameter of each pixel neighborhood that is used during filtering.
        img_blur = cv2.bilateralFilter(img_copy, 19, 130, 30)

        # cv2.medianBlur() is used to reduce noise in the image
        img_blur = cv2.medianBlur(img_blur, 9)

        # cv2.cvtColor() is used to convert the image to grayscale
        img_gray = cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY)

        # cv2.Sobel() is used to find the gradient of the image
        x_grid = cv2.Sobel(img_gray, cv2.CV_16SC1, 1, 0)
        y_grid = cv2.Sobel(img_gray, cv2.CV_16SC1, 0, 1)
        # cv2.Canny() is used to find the edges of the image
        img_canny = cv2.Canny(x_grid, y_grid, 30, 220)

        # split image into two parts, rectangle and ellipse
        weight, height = img_canny.shape
        img_rect = img_canny[:, :weight]
        img_elip = img_canny[:, weight:]

        # cv2.findContours to find contour
        # variable contours_1 stores all contours, each of which is composed of a series of pixel point 
        # For example: len(contours) contours[0] 
        # rectangle
        self.contours_rect, hierarchy = cv2.findContours(img_rect, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # elipse
        self.contours_elip, hierarchy = cv2.findContours(img_elip, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Test code
        # cv2.imshow('canny image', img_canny)
        # cv2.waitKey()
        # cv2.destroyAllWindows()

        # cv2.imshow('rect image', img_rect)
        # cv2.waitKey()
        # cv2.destroyAllWindows()

        # cv2.imshow('elip image', img_elip)
        # cv2.waitKey()
        # cv2.destroyAllWindows()
        # print('contours_rect: ', self.contours_rect)
        # print('length of rectangle: ', len(self.contours_rect))
        # print('example of rectangle: ', self.contours_rect[0])
        # print('contours_elip: ', self.contours_elip)
        # print('length of ellipse: ', len(self.contours_elip))
        # print('example of ellipse: ', self.contours_elip[0])

    def image_process(self, img_path):

        # read image from img_path
        img_src = cv2.imread(img_path)

        if img_src is None:
            print('Source Image is None, Please check image path!')
            return
        
        img_copy = img_src.copy()

        ############## Your Code Start Here ##############
        # TODO: image process including filtering, edge detection, contour detection and so on.
        
        # Important: check contours and make sure the contour is available.
        # For one block, there will be 4 contours, 2 for rectangle or ellipse outside and 2 for arrow inside.
        # For one rectangle edge, there will be 2 contours in image resolution.
        # Tips: use cv2.contourArea(contour) as threshold to filter out the contour.
        img_blur = cv2.bilateralFilter(img_copy, 29,70,200)

        # cv2.medianBlur() is used to reduce noise in the image
        img_blur = cv2.medianBlur(img_blur, 9)

        # cv2.cvtColor() is used to convert the image to grayscale
        img_gray = cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY)

        # cv2.Sobel() is used to find the gradient of the image
        x_grid = cv2.Sobel(img_gray, cv2.CV_16SC1, 1, 0)
        y_grid = cv2.Sobel(img_gray, cv2.CV_16SC1, 0, 1)
        # cv2.Canny() is used to find the edges of the image
        img_canny = cv2.Canny(x_grid, y_grid, 50,150)

        # split image into two parts, rectangle and ellipse
        weight, height = img_canny.shape
        img_rect = img_canny[:, :weight]
        img_elip = img_canny[:, weight:]

        cv2.imshow('canny image', img_canny)
        cv2.waitKey()
        cv2.destroyAllWindows()
        

        # cv2.imshow('rect image', img_rect)
        # cv2.waitKey()
        # cv2.destroyAllWindows()

        # cv2.imshow('elip image', img_elip)
        # cv2.waitKey()
        # cv2.destroyAllWindows()
        
        
        # # # rectangle
        # contours_rect, hierarchy = cv2.findContours(img_rect, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # # # elipse
        # contours_elip, hierarchy = cv2.findContours(img_elip, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # contours = contours_rect

        # contours.append(contours_elip)

        contours_ini, hierarchy = cv2.findContours(img_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = []

        for con in contours_ini:
            flag = False
            for con_rec in self.contours_rect:
                if cv2.contourArea(con) >= cv2.contourArea(con_rec):
                    flag = True
                    break
            for con_eli in self.contours_elip:
                if cv2.contourArea(con) >= cv2.contourArea(con_eli):
                    flag = True
                    break

            if flag == True:
                contours.append(con)


        ############### Your Code End Here ###############

        # length of contours equals to 4 times the number of blocks
        print("length of contours: ", len(contours))

        ############## Your Code Start Here ##############
        # TODO: compute the center of contour and the angle of arrow,
        # as well as match shapes of your block
        center_value = []
        shape = [] # 0 represents rectangle while 1 represents ellipse
        theta = []
        
        # for i in range(len(contours)):
        #     image = cv2.drawContours(img_copy, contours, i, (0,255,0), 3)
        #     cv2.imshow("Image number {}".format(i),image)
            
        for i in range(len(contours) // 2):
            if i % 2 == 0:
                ############## Your Code Start Here ##############
                # TODO: compute the center of external contour (rectangle/ellipse) and match shapes of your block
                # Tips: ret = cv2.matchShapes(contour1, contour2, 1, 0.0) 
                N = cv2.moments(contours[i * 2])
                center_x = int(N["m10"] / N["m00"])
                center_y = int(N["m01"] / N["m00"])
                center_value.append((center_x,center_y))
                cv2.circle(img_copy, (int(center_x), int(center_y)), 7, [0,0,255], -1)

                diff_rec = cv2.matchShapes(contours[i*2], self.contours_rect[0], 1, 0.0)
                diff_eli = cv2.matchShapes(contours[i*2], self.contours_elip[0], 1, 0.0)
                if diff_rec <= diff_eli:
                    shape_now = 1 # ellipse now
                    shape.append(shape_now)

                

                

                ############### Your Code End Here ###############

            else:
                # compute the center of internal contour (arrow) and compute the angle of arrow
                N = cv2.moments(contours[i * 2])
                _center_x = int(N["m10"] / N["m00"])
                _center_y = int(N["m01"] / N["m00"])
                # draw a circle on the center point
                cv2.circle(img_copy, (int(_center_x), int(_center_y)), 7, [0,255,0], -1)

                ############## Your Code Start Here ##############
                # TODO: compute the angle of arrow
                # Tips: compute the distance between center point of external contour and every point of internal contour,
                # find the furthest point, then you can compute the angle.


                
                x = 0
                y = 0
                
                dist = 0
                center = center_value[(i-1)//2]
                c_x = center[0]
                c_y = center[1]
                
                for dot in contours[i*2]:
                    x_temp = dot[0][0]
                    y_temp = dot[0][1]
                    dist_temp = (x_temp - c_x)**2 + (y_temp - c_y)**2
                    if dist_temp >= dist:
                        x = x_temp
                        y = y_temp
                        dist = dist_temp

                angle = np.arctan2((y - c_y), (x - c_x))
                theta.append(angle)

                cv2.line(img_copy, (_center_x, _center_y), (x, y), (128, 0, 0), 2)

                

                ############### Your Code End Here ###############

        cv2.imshow('image with center and orientation', img_copy)
        cv2.waitKey()
        cv2.destroyAllWindows()

        return center_value, shape, theta

def main():

    # init image path
    # template image for template matching of rectangle and ellipse
    path_template = "../img/template.jpg"
    # two calibration images to calculate the image coordinate
    # with corresponding image coordinate and robot coordinate, 
    # a linear transformation between image coordinate and robot coordinate can be computed
    path_img_cali1 = '../img/img_cali_1.bmp'
    path_img_cali2 = '../img/img_cali_2.bmp'
    # snapshot image saved by your camera
    path_img_snap = '../img/img_snap.bmp'

    # init ImageProcess class
    img_process = ImageProcess()

    # template process to get the contour of rectangle and ellipse
    img_process.template_process(path_template)

    # image process for calibration images to get the position of blocks
    center_cali1, shape_cali1, theta_cali1 = img_process.image_process(path_img_cali1)
    center_cali2, shape_cali2, theta_cali2 = img_process.image_process(path_img_cali2)

    # image process to get the shape, position and orientation of blocks
    center_snap, shape_snap, theta_snap = img_process.image_process(path_img_snap)

if __name__ == '__main__':
	
	main()
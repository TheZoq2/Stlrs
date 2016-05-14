#include "Raspi-ImageProcessing/desktop/objectTracking/ColorTracker.h"
#include "Raspi-ImageProcessing/desktop/config.h"

#include <opencv2/opencv.hpp>

#include <fstream>
#include <string>

const std::string COMM_PATH_OUT = "/tmp/stlrs_coords";
const std::string COMM_PATH_IN = "/tmp/stlrs_cmd";

cv::Mat getPerspectiveTransform(std::vector<Flooder::Blob> blobs);


int main()
{
    ColorTracker ct;

    cv::VideoCapture camera = cv::VideoCapture(Config::CAMERA_ID);

    cv::Mat currentImage;

    //Read fisheye correction stuff from a file. Generate using the "cpp/calibration" sample
    cv::Mat camera_matrix, distortion;
    cv::FileStorage fs("../data/fisheye0.txt", cv::FileStorage::READ);
    cv::FileNode fn = fs["IntParam"];
    fn["camera_matrix"] >> camera_matrix;
    fn["distortion_coefficients"] >> distortion;

    bool calibrated = false;
    cv::Mat perspectiveTransform;

    //cv::namedWindow("Yolo");

    while(true)
    {
        

        camera >> currentImage;

        //Fisheye correction
        //Fix fisheye problems
        cv::Mat tmpImg;


        cv::undistort(currentImage, tmpImg, camera_matrix, distortion);

        if(calibrated)
        {
            cv::warpPerspective(tmpImg, tmpImg, perspectiveTransform, cv::Size(640, 640));
        }

        ct.setImage(tmpImg);
        ct.runTracker();

        auto blobs = ct.getBlobs(80);

        std::fstream outFile(COMM_PATH_OUT, std::fstream::out);
        for(auto blob : blobs)
        {
            std::cout << blob.center.getString() << std::endl;

            outFile << blob.center.getString() << std::endl;
        }
        outFile.close();

        cv::imshow("Yolo", tmpImg);
        cv::imshow("bin", ct.getBinary());

        cv::waitKey(1);

        std::cout << "New frame" << std::endl;

        //Reading the command from python
        std::fstream inFile(COMM_PATH_IN, std::fstream::in);

        std::string cmd;

        if(inFile >> cmd)
        {
            if(cmd == "calibrate" && calibrated == false)
            {
                std::cout << "calibrating" << std::endl;
                perspectiveTransform = getPerspectiveTransform(blobs);

                calibrated = true;
            }
            if(cmd == "restart" && calibrated == true)
            {
                calibrated = false;
                std::cout << "Restarting" << std::endl;
            }
        }

        inFile.close();
    }
    return 0;
}

cv::Mat getPerspectiveTransform(std::vector<Flooder::Blob> blobs)
{
    float center_x = 640;
    float center_y = 480;

    float total_x = 0;
    float total_y = 0;

    for(auto blob : blobs)
    {
        total_x += blob.center.val[0];
        total_y += blob.center.val[1];
    }

    center_x = total_x / blobs.size();
    center_y = total_y / blobs.size();

    std::cout << "Center: " << center_x << " " << center_y << std::endl;
    cv::Mat result;

    cv::Point2f screen_points[] = {
            cv::Point2f(100, 100),
            cv::Point2f(450, 100),
            cv::Point2f(100, 450),
            cv::Point2f(450, 450)
        };
    cv::Point2f camera_points[] = {
            cv::Point2f(100, 100),
            cv::Point2f(100, 450),
            cv::Point2f(450, 100),
            cv::Point2f(450, 450)
        };

    for(auto blob : blobs)
    {
        std::cout << "Blob: " << blob.center.getString() << std::endl;
        if(blob.center.val[0] < center_x && blob.center.val[1] < center_y)
        {
            camera_points[0] = cv::Point2f(blob.center.val[0], blob.center.val[1]);
            std::cout << "x< y<" << std::endl;
        }
        else if(blob.center.val[0] > center_x && blob.center.val[1] < center_y)
        {
            camera_points[1] = cv::Point2f(blob.center.val[0], blob.center.val[1]);

            std::cout << "x> y<: " << std::endl;
        }
        else if(blob.center.val[0] > center_x && blob.center.val[1] > center_y)
        {
            camera_points[3] = cv::Point2f(blob.center.val[0], blob.center.val[1]);
            std::cout << "x> y>: "<< std::endl;
        }
        else
        {
            camera_points[2] = cv::Point2f(blob.center.val[0], blob.center.val[1]);
            std::cout << "x< y>: " << std::endl;
        }
    }

    result = cv::getPerspectiveTransform(camera_points, screen_points);

    return result;
}

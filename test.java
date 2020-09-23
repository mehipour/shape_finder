
int main( int argc, char** argv )
{
    Mat src = imread( argv[1] );
    Mat gray, blurred;
    cvtColor( src, gray, COLOR_BGR2GRAY );
    threshold( gray, gray, 127, 255, THRESH_BINARY );
    GaussianBlur( gray, blurred, Size(), 5 );
    threshold( blurred, blurred, 180, 255, THRESH_BINARY_INV );
    gray.setTo( 255, blurred );
    imshow("result of step 1",gray);

    vector<vector<Point> > contours;

    /// Find contours
    findContours( gray.clone(), contours, RETR_TREE, CHAIN_APPROX_SIMPLE );

    /// Find the rotated rectangles and ellipses for each contour
    vector<RotatedRect> minRect( contours.size() );
    vector<RotatedRect> minEllipse( contours.size() );

    for( size_t i = 0; i < contours.size(); i++ )
    {
        minRect[i] = minAreaRect( Mat(contours[i]) );
        if( contours[i].size() > 5 )
        {
            minEllipse[i] = fitEllipse( Mat(contours[i]) );
        }
    }

    /// Draw contours + rotated rects + ellipses
    for( size_t i = 0; i< contours.size(); i++ )
    {
        Mat drawing = src.clone();
        // contour
        //drawContours( drawing, contours, (int)i, color, 1, 8, vector<Vec4i>(), 0, Point() );
        // ellipse
        ellipse( drawing, minEllipse[i], Scalar( 0, 0, 255 ), 2 );
        // rotated rectangle
        Point2f rect_points[4];
        minRect[i].points( rect_points );
        for( int j = 0; j < 4; j++ )
            line( drawing, rect_points[j], rect_points[(j+1)%4], Scalar( 0, 255, 0 ), 2 );
        /// Show in a window
        imshow( "results of step 2", drawing );
        waitKey();
    }

    return 0;
}
import numpy as np
import cv2
import pytesseract

from Soduku import Soduku


def perspective_transform(image, corners):
    def order_corner_points(corners):
        # Separate corners into individual points
        # Index 0 - top-right
        #       1 - top-left
        #       2 - bottom-left
        #       3 - bottom-right
        corners = [(corner[0][0], corner[0][1]) for corner in corners]
        top_r, top_l, bottom_l, bottom_r = corners[0], corners[1], corners[2], corners[3]
        return (top_l, top_r, bottom_r, bottom_l)

    # Order points in clockwise order
    ordered_corners = order_corner_points(corners)
    top_l, top_r, bottom_r, bottom_l = ordered_corners

    # Determine width of new image which is the max distance between
    # (bottom right and bottom left) or (top right and top left) x-coordinates
    width_A = np.sqrt(((bottom_r[0] - bottom_l[0]) ** 2) + ((bottom_r[1] - bottom_l[1]) ** 2))
    width_B = np.sqrt(((top_r[0] - top_l[0]) ** 2) + ((top_r[1] - top_l[1]) ** 2))
    width = max(int(width_A), int(width_B))

    # Determine height of new image which is the max distance between
    # (top right and bottom right) or (top left and bottom left) y-coordinates
    height_A = np.sqrt(((top_r[0] - bottom_r[0]) ** 2) + ((top_r[1] - bottom_r[1]) ** 2))
    height_B = np.sqrt(((top_l[0] - bottom_l[0]) ** 2) + ((top_l[1] - bottom_l[1]) ** 2))
    height = max(int(height_A), int(height_B))

    # Construct new points to obtain top-down view of image in
    # top_r, top_l, bottom_l, bottom_r order
    dimensions = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1],
                    [0, height - 1]], dtype = "float32")

    # Convert to Numpy format
    ordered_corners = np.array(ordered_corners, dtype="float32")

    # Find perspective transform matrix
    matrix = cv2.getPerspectiveTransform(ordered_corners, dimensions)

    # Return the transformed image
    return cv2.warpPerspective(image, matrix, (width, height))
def approx_contour(ext_contours):
    lst = sorted(ext_contours,key=cv2.contourArea,reverse=True)
    for c in lst:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.01 * peri, True)
        if len(approx) == 4:
            # Here we are looking for the largest 4 sided contour
            return approx
def extract_num (str):
    for c in str:
        if c.isdigit():
            return int(c)

    return 0


pytesseract.pytesseract.tesseract_cmd = "C:\Program Files (x86)\Tesseract-OCR\\tesseract.exe"
img_path = "resources\img6.jpg"
soduku_img = cv2.imread(img_path,cv2.IMREAD_GRAYSCALE)
process = cv2.GaussianBlur(soduku_img,(7,7),3)
process = cv2.adaptiveThreshold(process, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 11, 2)
process = cv2.bitwise_not(process)
kernel = np.array([[0., 1., 0.], [1., 1., 1.], [0., 1., 0.]], np.uint8)
process = cv2.dilate(process, kernel)
img2 = cv2.imread(img_path)
cv2.imshow("soduku2",process)
contours , hirarchy = cv2.findContours(process,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)


cnt = approx_contour(contours)
peri = cv2.arcLength(cnt, True)
approx = cv2.approxPolyDP(cnt, 0.015 * peri, True)
cv2.drawContours(img2, [approx], 0, (255, 0, 255), 5)
cv2.imshow("contours", img2)




transformed = perspective_transform(img2,cnt)
board_img = [[0 for j in range (9)] for i in range(9)]
board = [[0 for j in range (9)] for i in range(9)]
l = transformed.shape[0]//9
h = transformed.shape[1]//9
for i in range (9):
    for j in range (9):
        num = transformed[i*l:i*l+l,j*h:j*h+h]
        num = cv2.cvtColor(num,cv2.COLOR_BGR2GRAY)
        num = cv2.bitwise_not(num)
        _, num = cv2.threshold(num, 200, 255, cv2.THRESH_BINARY)
        num = cv2.bitwise_not(num)

        cv2.imshow("num",num)
        cv2.waitKey(500)
        board_img[i][j] = num
        predict = pytesseract.image_to_string(num,config="--psm 10")
        predict = extract_num(predict)
        board[i][j] = predict
        print(predict)

cv2.imshow("board",img2)
print("start solving")
print ("original")
soduku = Soduku(board)
soduku.display()
print ("soloution")
soduku.solve()
cv2.waitKey(0)


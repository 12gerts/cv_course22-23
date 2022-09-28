import cv2 as cv
import numpy as np


def color_mask(img):
    """ Creating a mask by blue pixels. """
    low_blue = np.array((90, 70, 70), np.uint8)
    high_blue = np.array((150, 255, 255), np.uint8)
    img_hsl = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    mask_blue = cv.inRange(img_hsl, low_blue, high_blue)
    return mask_blue


def remove_noise(img):
    """ Noise reduction with erosion and dilatation. """
    kernel = np.ones((5, 5), np.uint8)
    img_erosion = cv.erode(img, kernel, iterations=2)
    img_dilation = cv.dilate(img_erosion, kernel, iterations=2)
    return img_dilation


def find_contours(img):
    (contours, _) = cv.findContours(img.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    return contours


def merge_image(img1, img2):
    """ Creating a new image by merging two previous images.

    The images are combined horizontally.
    The new width is equal to the sum of the widths of img1 and img2.
    """
    return np.concatenate((img1, img2), axis=1)


def resize(img):
    """ Changing the size of the frame.

    Frames the frame if the width of the image is greater than 900 pixels.
    The height is corrected proportionally.
    """
    if img.shape[1] > 900:
        coefficient = 900 / img.shape[1]
        width = int(img.shape[1] * coefficient)
        height = int(img.shape[0] * coefficient)
        size = (width, height)
        return cv.resize(img, size)
    return img


def show(text, img):
    cv.imshow(text, img)
    cv.waitKey(5)


def process(cap):
    """ Converting each frame of video. """
    while cap.isOpened():
        success, img = cap.read()
        if not success:
            print("Can't receive frame")
            break
        img = resize(img)
        mask = color_mask(img)
        img_without_noise = remove_noise(mask)
        contours = find_contours(img_without_noise)
        # adding more channels
        img_modified = cv.cvtColor(img_without_noise, cv.COLOR_GRAY2RGB)

        for contour in contours:
            # find the rectangle with the smallest area
            rect = cv.minAreaRect(contour)
            # peak search
            box = cv.boxPoints(rect)
            # coordinate rounding
            box = np.int0(box)
            # add contours to images
            cv.drawContours(img, [box], 0, (150, 200, 12), 3)
            cv.drawContours(img_modified, [box], 0, (150, 200, 12), 3)

        merged = merge_image(img, img_modified)
        show('result', merged)

        # exit
        if cv.waitKey(1) == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()


def main():
    video = cv.VideoCapture('data\\hw_1.mp4')
    process(video)


if __name__ == '__main__':
    main()

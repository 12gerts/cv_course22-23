import cv2 as cv
import numpy as np
from pynput.keyboard import Key, Controller

LOW_BLUE = (35, 30, 30)
HIGH_BLUE = (85, 255, 255)
YELLOW = (0, 255, 255)
GREEN = (150, 200, 12)
OFFSET = 100


def color_mask(img):
    """ Creating a mask by blue pixels. """
    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    mask_blue = cv.inRange(img_hsv, LOW_BLUE, HIGH_BLUE)
    return mask_blue


def remove_noise(img):
    """ Noise reduction with erosion and dilatation. """
    kernel = np.ones((5, 5), np.uint8)
    img_erosion = cv.erode(img, kernel, iterations=2)
    img_dilation = cv.dilate(img_erosion, kernel, iterations=2)
    return img_dilation


def find_contours(img):
    (contours, _) = cv.findContours(img.copy(), cv.RETR_TREE,
                                    cv.CHAIN_APPROX_SIMPLE)
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
    cv.imshow(text, cv.flip(img, flipCode=1))
    cv.waitKey(5)


def return_max_area_rectangle(mask):
    mask = np.copy(mask)
    contours, hierarchy = cv.findContours(mask, 1, 2)
    area_array = np.zeros(len(contours))
    counter = 0
    for contour in contours:
        area_array[counter] = cv.contourArea(contour)
        counter += 1
    if area_array.size == 0:
        return None, None, None, None
    max_area_index = np.argmax(area_array)
    cnt = contours[max_area_index]
    (x, y, w, h) = cv.boundingRect(cnt)
    return x, y, w, h, cnt


def return_max_area_center(mask):
    try:
        x, y, w, h, cnt = return_max_area_rectangle(mask)
    except ValueError:
        return None, None
    m = cv.moments(cnt)
    if m['m00'] == 0:
        return None, None
    cx = int(m['m10'] / m['m00'])
    cy = int(m['m01'] / m['m00'])
    return cx, cy


def draw_grid(img):
    height, width = img.shape[:2]
    x_center = width // 2
    y_center = height // 2
    cv.line(img, (x_center + OFFSET, 0), (x_center + OFFSET, height), GREEN, 2)
    cv.line(img, (x_center - OFFSET, 0), (x_center - OFFSET, height), GREEN, 2)
    cv.line(img, (0, y_center + OFFSET), (width, y_center + OFFSET), GREEN, 2)
    cv.line(img, (0, y_center - OFFSET), (width, y_center - OFFSET), GREEN, 2)
    return img


def draw_area(img, x, y):
    keyboard = Controller()

    height, width = img.shape[:2]
    y_center = img.shape[0] // 2
    x_center = img.shape[1] // 2

    if x_center + OFFSET < x and abs(y_center - y) <= OFFSET:
        active_area = img[(y_center - OFFSET):(y_center + OFFSET),
                      (x_center + OFFSET):width, :]
        active_area[:, :, 2] = 100
        img[(y_center - OFFSET):(y_center + OFFSET),
        (x_center + OFFSET):width, :] = active_area
        keyboard.press(Key.left)
        keyboard.release(Key.left)

    elif x_center - OFFSET > x and abs(y_center - y) <= OFFSET:
        active_area = img[(y_center - OFFSET):(y_center + OFFSET),
                      0:(x_center - OFFSET), :]
        active_area[:, :, 2] = 100
        img[(y_center - OFFSET):(y_center + OFFSET), 0:(x_center - OFFSET),
        :] = active_area
        keyboard.press(Key.right)
        keyboard.release(Key.right)

    elif y_center + OFFSET < y and abs(x_center - x) <= OFFSET:
        active_area = img[(y_center + OFFSET):height,
                      (x_center - OFFSET):(x_center + OFFSET), :]
        active_area[:, :, 2] = 100
        img[(y_center + OFFSET):height,
        (x_center - OFFSET):(x_center + OFFSET), :] = active_area
        keyboard.press(Key.down)
        keyboard.release(Key.down)

    elif y_center - OFFSET > y and abs(x_center - x) <= OFFSET:
        active_area = img[0:(y_center - OFFSET),
                      (x_center - OFFSET):(x_center + OFFSET), :]
        active_area[:, :, 2] = 100
        img[0:(y_center - OFFSET), (x_center - OFFSET):(x_center + OFFSET),
        :] = active_area
        keyboard.press(Key.up)
        keyboard.release(Key.up)
    return img


def draw_text(img):
    img = cv.flip(img, flipCode=1)
    cv.putText(img, "Take green object", (60, 60), cv.FONT_HERSHEY_SIMPLEX, 2, GREEN, 2)
    return cv.flip(img, flipCode=1)


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
        x, y = return_max_area_center(img_without_noise)
        if x is None:
            img = draw_text(img)
            show('', img)
            continue
        cv.circle(img, (x, y), 5, YELLOW, -1)
        img = draw_grid(img)
        img = draw_area(img, x, y)
        show('', img)

        if cv.waitKey(1) == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()


def main():
    video = cv.VideoCapture(0)
    process(video)


if __name__ == '__main__':
    main()

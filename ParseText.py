import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'.\tesseractv5.0.0-rc1.20211030\tesseract.exe'


def _parse_string(string):
    """
    parses the time string to return the number of seconds currently
    present
    :param string: the timer string from getTimer
    :return: the seconds of the timer
    """

    colon = string.find(':')
    if colon == -1:
        # return a -1 if not found
        return -1
    else:
        # return the two numbers before the middle
        return string[colon+1:colon+3]


def get_timer(img):
    """
    uses pytesseract to parse the timer from the text in the game
    :param img: the minimal screenshot containing the timer
    :return: a text based representation of the timer
    """
    # detect text in the image using pytesseract
    custom_config = r'-l eng --oem 1 --psm 7 -c tessedit_char_whitelist=0123456789/:'
    out = pytesseract.image_to_string(img, lang='eng', config=custom_config)
    return _parse_string(out)

# old code for get_timer
# sct = mss.mss()
# monitor_right = {'top': 50, 'left': 1920 - 405, 'width': 250, 'height': 50}
# screen_right = sct.grab(monitor_right)
# img_right = np.array(screen_right)
# cv2.imshow('image', img_right)
# cv2.waitKey(10)
# # detect text in the image using pytesseract
# custom_config = r'--oem 3 --psm 6 outputbase digits'
# print(parse_string(pytesseract.image_to_string(img_right, config=custom_config)))

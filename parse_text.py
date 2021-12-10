import pytesseract

# to set tesseract to run from a specific location
# pytesseract.pytesseract.tesseract_cmd = r'.\tesseractv5.0.0-rc1.20211030\tesseract.exe'


def _parse_string_timer(string):
    """
    parses the time string to return the number of seconds
    passed in the level
    :param string: the timer string from getTimer
    :return: the seconds elapsed
    """

    #TODO replace with strptime for rhobustness
    colon = string.find(':')
    if colon == -1:
        # return a -1 if not found
        return -1
    else:
        mins = string[colon-2:colon]
        secs = string[colon+1:colon+3]
        try:
            mins = int(mins)
            secs = int(secs)
            return 60 * mins + secs
        except:
            return -1


def get_timer(img):
    """
    uses pytesseract to parse the timer from the text in the game
    :param img: the minimal screenshot containing the timer
    :return: a text based representation of the timer
    """
    # detect text in the image using pytesseract
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789/:'
    out = pytesseract.image_to_string(img, lang='eng', config=custom_config)
    return _parse_string_timer(out)


def get_level(img):
    """
    uses pytesseract to parse the timer from the text in the game
    :param img: the minimal screenshot containing the level number
    :return: a text based representation of the level number
    """
    # detect text in the image using pytesseract
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789-—'
    out = pytesseract.image_to_string(img, lang='eng', config=custom_config)
    return out

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

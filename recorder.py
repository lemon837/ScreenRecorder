import pyautogui
import cv2
import numpy as np
 
def run():
    # Specifies screen recording variables.
    resolution = (1920, 1080)
    codec = cv2.VideoWriter_fourcc(*"XVID")
    filename = "Recording.avi"
    fps = 30.0

    out = cv2.VideoWriter(filename, codec, fps, resolution)     # Creates a VideoWriter object.
    cv2.namedWindow("Live", cv2.WINDOW_NORMAL)                  # Creates an empty window on desktop.
    cv2.resizeWindow("Live", 70, 30)                            # Resizes the window

    # Specifies hook control image variables.
    hook_template = cv2.imread('hook.png')
    sift = cv2.SIFT_create()
    keypoints1, descriptors1 = sift.detectAndCompute(hook_template, None)
    bfmatcher = cv2.BFMatcher()

    while True:
        img = pyautogui.screenshot(region=(60, 350, 80, 70))    # Takes a screenshot using PyAutoGUI.
        frame = np.array(img)                                   # Converts the screenshot to a Numpy array.
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)         # Converts to grayscale.
    
        out.write(frame)
        cv2.imshow('Live', frame)           # Displays the recording screen.

        if cv2.waitKey(1) == ord('q'):      # Stop recording when we press 'q'
            break
    
    out.release()               # Afterwards releases the video writer object,
    cv2.destroyAllWindows()     # and destroys all windows.

def compare():
    template_image = cv2.imread('hook.png')
    test_image = cv2.imread('hook1.png')
    sift = cv2.SIFT_create()

    keypoints1, descriptors1 = sift.detectAndCompute(template_image, None)
    keypoints2, descriptors2 = sift.detectAndCompute(test_image, None)

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(descriptors1, descriptors2, k=2)
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    if len(good_matches) > 5:
        print("Images are similar enough.")

    # # Draw the matches on a combined image
    # result_image = cv2.drawMatches(template_image, keypoints1, test_image, keypoints2, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    # # Save and display the result
    # cv2.imwrite('sift_matches.png', result_image)
    # cv2.imshow('Matches', result_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

if __name__ == ("__main__"):
    run()
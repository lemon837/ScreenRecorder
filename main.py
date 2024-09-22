import pyautogui
import cv2
import numpy as np
import tkinter as tk


def run():
    # Specifies screen recording variables.
    resolution = (2560, 1440)
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
    # result_image = cv2.drawMatches(template_image, keypoints1, test_image, keypoints2, good_matches, None,
    # flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    # # Save and display the result
    # cv2.imwrite('sift_matches.png', result_image)
    # cv2.imshow('Matches', result_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


def run_app():
    # Initialises the tkinter application.
    root = tk.Tk()
    root.title("DBD Hook Counter")
    root.geometry("200x200")
    label1 = tk.Label(root, text="Survivor 1: ")
    label1.pack(pady=10)
    label2 = tk.Label(root, text="Survivor 2: ")
    label2.pack(pady=10)
    label3 = tk.Label(root, text="Survivor 3: ")
    label3.pack(pady=10)
    label4 = tk.Label(root, text="Survivor 4: ")
    label4.pack(pady=10)
    root.update()       # Ensures app stays open and waits for updates.

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
    bf = cv2.BFMatcher(cv2.NORM_L2)

    # Initialises main survivor variables (integers for now).
    survivor1, survivor2, survivor3, survivor4 = 0, 0, 0, 0

    while True:
        img = pyautogui.screenshot(region=(100, 500, 200, 200))    # Takes a screenshot using PyAutoGUI.
        frame = np.array(img)                                   # Converts the screenshot to a Numpy array.
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)         # Converts to grayscale.
        cv2.imshow('Live', frame)                               # Displays the recording screen.

        # Analyses survivor's current image, compares to template.
        keypoints2, descriptors2 = sift.detectAndCompute(frame, None)
        if descriptors2 is not None and descriptors1 is not None:
            matches = bf.knnMatch(descriptors1, descriptors2, k=2)
            good_matches = []
            for match in matches:
                if len(match) == 2:
                    m, n = match
                    if m.distance < 0.75 * n.distance:
                        good_matches.append(m)
            if len(good_matches) > 5:
                label1.config(text="Survivor 1: good matches: " + str(len(good_matches)))
                print(f"Good matches: {len(good_matches)}")

        if cv2.waitKey(1) == ord('q'):      # Stops recording when 'q' is pressed.
            break
    
    out.release()               # Afterwards releases the video writer object,
    cv2.destroyAllWindows()     # and destroys all windows.
    root.mainloop()


if __name__ == ("__main__"):
    run_app()
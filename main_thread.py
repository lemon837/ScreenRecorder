"""
A Python program that serves as a per-survivor hook counter for killer players in the game Dead By Daylight.
This program exclusively uses screen recording software and does not constitute an unfair advantage in the game
that cannot be gained by writing the same information down manually. It is simply a means to automate this manual writing.

Known Issues:
- pyautogui.screenshot throws an "OSError: screen grab failed" when using ctrl-alt-del.

Written by ...
"""

import pyautogui
import cv2
import numpy as np
import tkinter as tk
import time
from functools import partial
import threading

hook_thread = None
stop_event = None

def create_app():
    # Initialises the tkinter application.
    root = tk.Tk()
    root.title("DBD Hook Counter")
    root.geometry("375x350")
    label1 = tk.Label(root, text="Survivor 1: ")
    label1.pack(pady=10)
    label2 = tk.Label(root, text="Survivor 2: ")
    label2.pack(pady=10)
    label3 = tk.Label(root, text="Survivor 3: ")
    label3.pack(pady=10)
    label4 = tk.Label(root, text="Survivor 4: ")
    label4.pack(pady=10)
    root.update()       # Ensures app stays open and waits for updates.
    start_button = tk.Button(root, text="Start Counter", command=partial(start_thread, root, label1, label2, label3, label4))
    start_button.pack(pady=15)
    reset_button = tk.Button(root, text="Reset Counter", command=partial(reset_thread, root, label1, label2, label3, label4))
    reset_button.pack(pady=15)
    root.mainloop()


def start_thread(root, label1, label2, label3, label4):
    global hook_thread, stop_event

    # if hook_thread

    stop_event = threading.Event()
    hook_thread = threading.Thread(target=count_hooks, args=(root, label1, label2, label3, label4))
    hook_thread.start()


def reset_thread(root, label1, label2, label3, label4):
    global hook_thread, stop_event
    
    print("reset")
    if hook_thread.is_alive():
        print("thread alive already, stopping...")
        stop_event.set()
        hook_thread.join()

    stop_event = threading.Event()
    hook_thread = threading.Thread(target=count_hooks, args=(root, label1, label2, label3, label4))
    hook_thread.start()


def count_hooks(root, label1, label2, label3, label4):
    # Specifies screen recording variables.
    resolution = (1920, 1080)
    codec = cv2.VideoWriter_fourcc(*"XVID")
    filename = "Recording.avi"
    fps = 30.0

    # Creates the four windows that show each survivor's status icon.
    out = cv2.VideoWriter(filename, codec, fps, resolution)     # Creates a VideoWriter object.
    cv2.namedWindow("surv1", cv2.WINDOW_NORMAL)                 # Creates an empty window on desktop.
    cv2.resizeWindow("surv1", 110, 110)                         # Resizes the window
    cv2.namedWindow("surv2", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("surv2", 110, 110)
    cv2.namedWindow("surv3", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("surv3", 110, 110)
    cv2.namedWindow("surv4", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("surv4", 110, 110)

    # Initialises main survivor variables.
    surv1_count, surv2_count, surv3_count, surv4_count = 0, 0, 0, 0
    surv1_status, surv2_status, surv3_status, surv4_status = "not_hooked", "not_hooked", "not_hooked", "not_hooked"

    # Specifies hook control image variables, to compare to survivor status icons.
    hook_template = cv2.imread('hook.png')
    sift = cv2.SIFT_create()
    keypoints0, descriptors0 = sift.detectAndCompute(hook_template, None)
    bf = cv2.BFMatcher(cv2.NORM_L2)

    while True:
        img = pyautogui.screenshot(region=(100, 630, 110, 110))     # Takes a screenshot using PyAutoGUI.
        frame1 = np.array(img)                                      # Converts the screenshot to a Numpy array.
        frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)           # Converts to grayscale.
        cv2.imshow('surv1', frame1)                                 # Displays the recording screen.

        img = pyautogui.screenshot(region=(100, 740, 110, 110))
        frame2 = np.array(img)
        frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        cv2.imshow('surv2', frame2)

        img = pyautogui.screenshot(region=(100, 850, 110, 110))
        frame3 = np.array(img)
        frame3 = cv2.cvtColor(frame3, cv2.COLOR_BGR2GRAY)
        cv2.imshow('surv3', frame3)

        img = pyautogui.screenshot(region=(100, 960, 110, 110))
        frame4 = np.array(img)
        frame4 = cv2.cvtColor(frame4, cv2.COLOR_BGR2GRAY)
        cv2.imshow('surv4', frame4)

        # Analyses survivor's current image, compares to template.
        keypoints1, descriptors1 = sift.detectAndCompute(frame1, None)
        if descriptors1 is not None and descriptors0 is not None:
            matches = bf.knnMatch(descriptors0, descriptors1, k=2)
            good_matches = []
            for match in matches:
                if len(match) == 2:
                    m, n = match
                    if m.distance < 0.75 * n.distance:
                        good_matches.append(m)
            if len(good_matches) > 12 and surv1_status == "not_hooked":
                surv1_status = "hooked"
                surv1_count += 1
            if len(good_matches) < 8 and surv1_status == "hooked":
                surv1_status = "not_hooked"
            label1.config(text=f"Survivor 1: (matches: {str(len(good_matches))}) (status: {surv1_status}) count: {surv1_count}")

        keypoints2, descriptors2 = sift.detectAndCompute(frame2, None)
        if descriptors2 is not None and descriptors0 is not None:
            matches = bf.knnMatch(descriptors0, descriptors2, k=2)
            good_matches = []
            for match in matches:
                if len(match) == 2:
                    m, n = match
                    if m.distance < 0.75 * n.distance:
                        good_matches.append(m)
            if len(good_matches) > 12 and surv2_status == "not_hooked":
                surv2_status = "hooked"
                surv2_count += 1
            if len(good_matches) < 8 and surv2_status == "hooked":
                surv2_status = "not_hooked"
            label2.config(text=f"Survivor 2: (matches: {str(len(good_matches))}) (status: {surv2_status}) count: {surv2_count}")

        keypoints3, descriptors3 = sift.detectAndCompute(frame3, None)
        if descriptors3 is not None and descriptors0 is not None:
            matches = bf.knnMatch(descriptors0, descriptors3, k=2)
            good_matches = []
            for match in matches:
                if len(match) == 2:
                    m, n = match
                    if m.distance < 0.75 * n.distance:
                        good_matches.append(m)
            if len(good_matches) > 12 and surv3_status == "not_hooked":
                surv3_status = "hooked"
                surv3_count += 1
            if len(good_matches) < 8 and surv3_status == "hooked":
                surv3_status = "not_hooked"
            label3.config(text=f"Survivor 3: (matches: {str(len(good_matches))}) (status: {surv3_status}) count: {surv3_count}")

        keypoints4, descriptors4 = sift.detectAndCompute(frame4, None)
        if descriptors4 is not None and descriptors0 is not None:
            matches = bf.knnMatch(descriptors0, descriptors4, k=2)
            good_matches = []
            for match in matches:
                if len(match) == 2:
                    m, n = match
                    if m.distance < 0.75 * n.distance:
                        good_matches.append(m)
            if len(good_matches) > 12 and surv4_status == "not_hooked":
                surv4_status = "hooked"
                surv4_count += 1
            if len(good_matches) < 8 and surv4_status == "hooked":
                surv4_status = "not_hooked"
            label4.config(text=f"Survivor 4: (matches: {str(len(good_matches))}) (status: {surv4_status}) count: {surv4_count}")
            
        if cv2.waitKey(1) == ord('q'):      # Stops recording when 'q' is pressed.
            out.release()                   # Afterwards releases the video writer object,
            cv2.destroyAllWindows()         # and destroys all windows.
            exit()

        root.update()           # Updates the tkinter app with all the new labels.
        time.sleep(0.5)         # 500ms wait until next loop.


if __name__ == ("__main__"):
    create_app()

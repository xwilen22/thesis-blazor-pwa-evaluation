from datetime import datetime
import os
import time
import pyautogui as pag

# Everytime a user intalls a PWA it gets a newly generated ID
REACT_PWA_WINDOW_TITLE_ID_IMAGE_NAME_TUPLE = ("React App", "nebdgepidhcmjhbdbhbookkcdmegnjpf", "reactStart")
BLAZOR_PWA_WINDOW_TITLE_ID_IMAGE_NAME_TUPLE = ("pwa-blazor", "illajbeckacllfemigjbekmgianibfbn", "blazorStart")

# Keep pathstring according to Windows standard.
# Observe! This path must exist before starting experiment!
PARAMETER_JSON_SAVE_PATH = "C:\OutputPerformanceJSON"
# Keep this one a few seconds above the testing paramters on the seperate PWAs
PARAMETER_EXPERIMENT_LENGTH_SECONDS = 30
# How many times should each PWA be run?
PARAMETER_EXPERIMENT_INSTANCE_AMOUNT = 30

PARAMETER_SLOWNESS_SECONDS = 10

def get_pwa_with_title_id(title, id):
    os.system("start .\system\start-chrome-pwa.bat {pwaId}".format(pwaId = id))
    pwaWindow = pag.getActiveWindow()

    # If something goes wrong and the browser window is not the current window
    while pwaWindow.title != title:
        windowsWithSubStringTitle = pag.getWindowsWithTitle(title)
        if len(windowsWithSubStringTitle) > 0:
            pwaWindow = windowsWithSubStringTitle[0]
    
    return pwaWindow

def get_dev_tools_window(browserWindow):
    allDevToolWindows = []

    while(len(allDevToolWindows) < 1):
        browserWindow.show()
        pag.press("f12")
        time.sleep(2 + PARAMETER_SLOWNESS_SECONDS)

        allDevToolWindows = pag.getWindowsWithTitle("DevTools - ")

    return allDevToolWindows[0]

def send_short_command(command, devToolsWindow):
    devToolsWindow.show()
    # Hotkey for opening command window, executes command pressing ENTER
    pag.hotkey("ctrl", "p")
    time.sleep(PARAMETER_SLOWNESS_SECONDS)
    pag.typewrite(str(command))
    time.sleep(PARAMETER_SLOWNESS_SECONDS)
    pag.press("enter")
    time.sleep(PARAMETER_SLOWNESS_SECONDS)

def get_start_button_point(imageName):
    startButtonPoint = None
    while startButtonPoint is None:
        # Wait for site to load
        time.sleep(PARAMETER_SLOWNESS_SECONDS)
        try:
            foundStartButton = pag.locateOnScreen("./img/{reactStart}.png".format(reactStart = imageName), confidence = 0.75)
            if foundStartButton is not None:
                startButtonPoint = pag.center(foundStartButton)
        except pag.ImageNotFoundException:
            print("Failed to find start button. Trying again...")
    return startButtonPoint

def start_experiment(pwaTitleIdImageTuple):
    pwaWindow = get_pwa_with_title_id(pwaTitleIdImageTuple[0], pwaTitleIdImageTuple[1])

    # Gets developer console on PWA
    devToolsWindow = get_dev_tools_window(pwaWindow)
    ## RECORDING
    # Opens command menu and sends short-command for viewing performance
    send_short_command("> Performance", devToolsWindow)
    # Shortcut for recording performance
    pag.hotkey("ctrl", "e")
    devToolsWindow.hide()
    ## START EXPERIMENT, finds and clicks start button
    pwaWindow.maximize()

    # Must click to get focus of PWA window
    pag.click(x = pwaWindow.centerx, y = pwaWindow.centery)

    startButtonPoint = get_start_button_point(pwaTitleIdImageTuple[2])
    pag.click(x=startButtonPoint.x, y=startButtonPoint.y)

    ## WAIT...
    time.sleep(PARAMETER_EXPERIMENT_LENGTH_SECONDS)

    ## STOP RECORDING, EXPERIMENT END
    devToolsWindow.show()
    devToolsWindow.maximize()
    time.sleep(2)
    # Must click to get focus of dev window
    pag.click(x = devToolsWindow.centerx, y = devToolsWindow.centery)
    # Toggles to stop and saves
    pag.hotkey("ctrl", "e")
    # Waits for profile to be processed w margin
    time.sleep(30 + PARAMETER_SLOWNESS_SECONDS)
    
    ## SAVE PERFORMANCE
    saveWindow = pag.getActiveWindow()
    # Only works on Swedish settings
    while saveWindow.title != "Spara som":
        pag.hotkey("ctrl", "s")
        time.sleep(10 + PARAMETER_SLOWNESS_SECONDS)
        saveWindow = pag.getActiveWindow()

    time.sleep(10 + PARAMETER_SLOWNESS_SECONDS)

    pag.write("{path}\{instanceTitle}-{name}".format(
        path = PARAMETER_JSON_SAVE_PATH, 
        instanceTitle = str(pwaTitleIdImageTuple[0]).replace(' ', '_'), 
        name = str(datetime.now()).replace(':', '.'))
    , interval = 0.05)
    time.sleep(PARAMETER_SLOWNESS_SECONDS)

    while pag.getActiveWindow().title == saveWindow.title:
        pag.press("enter")
        time.sleep(PARAMETER_SLOWNESS_SECONDS)

    # END OF INSTANCE, CLOSE ALL DOWN
    pwaWindow.close()
    # Wait for everything to close down
    time.sleep(5 + PARAMETER_SLOWNESS_SECONDS)

selection = input("Hello! Are the following parameters correct?\n\nReact PWA\nWindow title: {}\nApp ID: {}\n\nBlazor PWA\nWindow title: {}\nApp ID: {}\n\nYes or No? (Y/N)".format(
    REACT_PWA_WINDOW_TITLE_ID_IMAGE_NAME_TUPLE[0], 
    REACT_PWA_WINDOW_TITLE_ID_IMAGE_NAME_TUPLE[1], 
    BLAZOR_PWA_WINDOW_TITLE_ID_IMAGE_NAME_TUPLE[0], 
    BLAZOR_PWA_WINDOW_TITLE_ID_IMAGE_NAME_TUPLE[1]
)).lower()

if selection == 'y':
    print("Starting ReactJS testing...")
    reactInstances = 0
    while reactInstances < PARAMETER_EXPERIMENT_INSTANCE_AMOUNT:    
        start_experiment(REACT_PWA_WINDOW_TITLE_ID_IMAGE_NAME_TUPLE)
        reactInstances += 1
        print("Done with instance! ({}/{})".format(reactInstances, PARAMETER_EXPERIMENT_INSTANCE_AMOUNT))
    
    print("\n\nStarting Blazor Wasm testing...")
    blazorInstances = 0
    while blazorInstances < PARAMETER_EXPERIMENT_INSTANCE_AMOUNT:
        start_experiment(BLAZOR_PWA_WINDOW_TITLE_ID_IMAGE_NAME_TUPLE)
        blazorInstances += 1
        print("Done with instance! ({}/{})".format(blazorInstances, PARAMETER_EXPERIMENT_INSTANCE_AMOUNT))
    
    input("Job's done! You can find the JSON-files at {}".format(PARAMETER_JSON_SAVE_PATH))
else:
    input("\nChange them in this file\nEnter to quit...")
    quit()
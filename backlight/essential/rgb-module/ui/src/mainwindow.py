"""
Implementation of Main Window and Cef Browser Control
"""

from cefpython3 import cefpython as cef
import logging
import os
import sys

import tkinter as tk

from utils.staticvalues import PROGRAM_NAME
from utils.helper import get_file_uri, is_user_root, create_modprobe_file
import keyboardcontroller

WIDTH = 880
HEIGHT = 660

LOGGER = logging.getLogger(PROGRAM_NAME)

class MainWindow(object):
    class __MainWindow():
        """
        The Singleton MainWindow Class
        """

        def __init__(self):
            self.browser = None
            self.start_ui = get_file_uri(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui", "index.html"))

        def start(self, debugmode):
            """
            This functions initialize all objects and variables need to start the application
            """

            LOGGER.debug("start mainwindow")

            LOGGER.debug("configure cef")
            sys.excepthook = cef.ExceptHook
            cef_loglevel = cef.LOGSEVERITY_ERROR
            cef_logfile = os.path.join("/var", "log", PROGRAM_NAME, "cef.log")

            if debugmode:
                cef_loglevel = cef.LOGSEVERITY_VERBOSE

            browser_settings = {
                            "debug": debugmode,
                            "log_file": cef_logfile,
                            "log_severity": cef_loglevel, 
                            "context_menu": {
                                                # Deactivating the Chrome Contextmenu
                                                "enabled": debugmode
                                            }
                        }

            commandline_switch = {
                "disable-gpu": "disable"
            }

            LOGGER.debug("initialize tk")
            root = tk.Tk()
            root.resizable(width=False, height=False)
            app = MainFrame(root)

            LOGGER.debug("initialize cef")
            cef.Initialize(browser_settings, commandline_switch)

            LOGGER.debug("start mainloop")
            app.mainloop()
            cef.Shutdown()

        def create_browser(self, window):
            """
            Create CEF Browser Object
            """

            LOGGER.debug("create browser")

            from utils.helper import load_kernel_module, unload_kernel_module, set_module_status, activate_automatic_module_start, deactivate_automatic_module_start

            LOGGER.debug("set start page")
            self.browser = cef.CreateBrowserSync(url=self.start_ui, window_info=window)

            LOGGER.debug("loading language data")
            language_data = ""
            with open(os.path.join(os.path.dirname(__file__), "ui", "resources", "localization.json"), "r") as json_file:
                language_data = json_file.read()

            LOGGER.debug("create js bindings")
            jsbinding = cef.JavascriptBindings(bindToFrames=True, bindToPopups=True)
            jsbinding.SetProperty("language_data" , language_data)
            jsbinding.SetProperty("available_keyboard_colors", keyboardcontroller.AVAILABLE_KEYBOARD_COLORS)
            jsbinding.SetProperty("available_keyboard_modes", keyboardcontroller.AVAILABLE_KEYBOARD_MODES)
            jsbinding.SetProperty("keyboard_max_brightness", keyboardcontroller.KEYBOARD_MAX_BRIGHTNESS)
            jsbinding.SetProperty("keyboard_min_brightness", keyboardcontroller.KEYBOARD_MIN_BRIGHTNESS)
            jsbinding.SetProperty("keyboard_step_brightness", keyboardcontroller.KEYBOARD_STEP_BRIGHTNESS)
            jsbinding.SetProperty("keyboard_state_on", keyboardcontroller.KEYBOARD_STATE_ON)
            jsbinding.SetProperty("keyboard_state_off", keyboardcontroller.KEYBOARD_STATE_OFF)
            jsbinding.SetProperty("is_user_root", is_user_root())

            jsbinding.SetProperty("keyboard_mode", keyboardcontroller.get_keyboard_mode())
            jsbinding.SetProperty("keyboard_colors", keyboardcontroller.get_keyboard_color())
            jsbinding.SetProperty("keyboard_brightness", keyboardcontroller.get_keyboard_brightness())
            jsbinding.SetProperty("keyboard_state", keyboardcontroller.get_keyboard_state())

            jsbinding.SetFunction("set_keyboard_mode", keyboardcontroller.set_keyboard_mode)
            jsbinding.SetFunction("set_keyboard_color", keyboardcontroller.set_keyboard_color)
            jsbinding.SetFunction("set_keyboard_brightness", keyboardcontroller.set_keyboard_brightness)
            jsbinding.SetFunction("set_keyboard_state", keyboardcontroller.set_keyboard_state)

            jsbinding.SetFunction("load_module", load_kernel_module)
            jsbinding.SetFunction("unload_module", unload_kernel_module)
            jsbinding.SetFunction("set_module_status", set_module_status)

            jsbinding.SetFunction("activate_automatic_module_start", activate_automatic_module_start)
            jsbinding.SetFunction("deactivate_automatic_module_start", deactivate_automatic_module_start)

            jsbinding.SetFunction("create_modprobe_file", create_modprobe_file)

            self.browser.SetJavascriptBindings(jsbinding)

        def get_browser(self):
            """
            Return the Browser Object from CEF

            Returns:
                Browser Object from CEF
            """

            return self.browser

    # Instance Variable for the Singleton Class
    instance = None

    def __new__(cls):
        if not MainWindow.instance:
            MainWindow.instance = MainWindow.__MainWindow()

        return MainWindow.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)

class MainFrame(tk.Frame):
    def __init__(self, root):
        self.browser_frame = None

        # Set Root Window to Center of screen
        ws = root.winfo_screenwidth() # width of the screen
        hs = root.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (WIDTH/2)
        y = (hs/2) - (HEIGHT/2)
        root.geometry("%dx%d+%d+%d" % (WIDTH, HEIGHT, x, y))

        if is_user_root:
            title = "TUXEDO WMI UI (Root)"
        else:
            title = "TUXEDO WMI UI"

        # MainFrame
        tk.Frame.__init__(self, root)
        self.master.title(title)
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.master.bind("<Configure>", self.on_root_configure)
        self.setup_icon()
        self.bind("<Configure>", self.on_configure)

        # BrowserFrame
        self.browser_frame = BrowserFrame(self)
        self.browser_frame.grid(row=0, column=0, sticky=(tk.N + tk.S + tk.E + tk.W))
        tk.Grid.rowconfigure(self, 0, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)

        # Pack MainFrame
        self.pack(fill=tk.BOTH, expand=tk.YES)

    def on_root_configure(self, _):
        LOGGER.debug("MainFrame.on_root_configure")
        if self.browser_frame:
            self.browser_frame.on_root_configure()

    def on_configure(self, event):
        LOGGER.debug("MainFrame.on_configure")
        if self.browser_frame:
            width = event.width
            height = event.height

            self.browser_frame.on_mainframe_configure(width, height)

    def on_close(self):
        if self.browser_frame:
            self.browser_frame.on_root_close()

        self.master.destroy()

    def get_browser(self):
        if self.browser_frame:
            return self.browser_frame.browser
        return None

    def get_browser_frame(self):
        if self.browser_frame:
            return self.browser_frame
        return None

    def setup_icon(self):
        icon_path = os.path.join(os.path.dirname(__file__), "tcc.png")
        if os.path.exists(icon_path):
            self.icon = tk.PhotoImage(file=icon_path)
            self.master.call("wm", "iconphoto", self.master._w, self.icon)

class BrowserFrame(tk.Frame):
    def __init__(self, master):
        self.closing = False
        self.browser = None
        tk.Frame.__init__(self, master)
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
        self.bind("<Configure>", self.on_configure)
        self.focus_set()

    def embed_browser(self):
        window_info = cef.WindowInfo()
        rect = [0, 0, self.winfo_width(), self.winfo_height()]
        window_info.SetAsChild(self.get_window_handle(), rect)

        MainWindow().create_browser(window_info)
        self.browser = MainWindow().get_browser()

        self.browser.SetClientHandler(FocusHandler(self))

        self.message_loop_work()

    def get_window_handle(self):
        if self.winfo_id() > 0:
            return self.winfo_id()
        else:
            raise Exception("Couldn't obtain window handle")

    def message_loop_work(self):
        cef.MessageLoopWork()
        self.after(10, self.message_loop_work)

    def on_configure(self, _):
        if not self.browser:
            self.embed_browser()

    def on_root_configure(self):
        # Root <Configure> event will be called when top window is moved
        if self.browser:
            self.browser.NotifyMoveOrResizeStarted()

    def on_mainframe_configure(self, width, height):
        if self.browser:
            self.browser.SetBounds(0, 0, width, height)
            self.browser.NotifyMoveOrResizeStarted()

    def on_focus_in(self, _):
        LOGGER.debug("BrowserFrame.on_focus_in")
        if self.browser:
            self.browser.SetFocus(True)

    def on_focus_out(self, _):
        LOGGER.debug("BrowserFrame.on_focus_out")
        if self.browser:
            self.browser.SetFocus(False)

    def on_root_close(self):
        if self.browser:
            self.browser.CloseBrowser(True)
            self.clear_browser_references()
        self.destroy()

    def clear_browser_references(self):
        # Clear browser references that you keep anywhere in your
        # code. All references must be cleared for CEF to shutdown cleanly.
        self.browser = None

class FocusHandler(object):
    def __init__(self, browser_frame):
        self.browser_frame = browser_frame

    def OnTakeFocus(self, next_component, **_):
        LOGGER.debug("FocusHandler.OnTakeFocus, next=%s", next_component)

    def OnSetFocus(self, source, **_):
        LOGGER.debug("FocusHandler.OnSetFocus, source=%s", source)
        return False

    def OnGotFocus(self, **_):
        #Fix CEF focus issues (#255). Call browser frame's focus_set
        #to get rid of type cursor in url entry widget.
        LOGGER.debug("FocusHandler.OnGotFocus")
        self.browser_frame.focus_set()

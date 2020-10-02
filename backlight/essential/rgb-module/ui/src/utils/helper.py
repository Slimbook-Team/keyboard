"""
This module contains helper functions
"""

import logging
from utils.staticvalues import PROGRAM_NAME, KERNEL_MODULE_NAME

LOGGER = logging.getLogger(PROGRAM_NAME)

def get_file_uri(filepath):
    """
    Convert a path to file uri

    Args:
        param1: The path of the file

    Returns:
        A file uri, for exemple convert this function the path "/tmp/testfile.sh" in "file:///tmp/testfile.sh"
    """

    file_uri = ""

    LOGGER.debug("create fileuri for file '%s'", filepath)

    if not filepath.startswith("file://"):
        file_uri = "file://" + filepath
    elif filepath.startswith("file://"):
        file_uri = filepath

    LOGGER.debug("fileuri is '%s'", file_uri)

    return file_uri

def set_module_status(js_callback):
    """
    Call the JavaScript callback with the current state of the kernel module
    """

    js_callback.Call(is_kernel_module_loaded())

def is_kernel_module_loaded():
    """
    Check if the kernel module loaded

    Returns True or false
    """

    import subprocess
    import shlex

    LOGGER.debug("call lsmod")
    return_value, output = subprocess.getstatusoutput("lsmod")

    if return_value is not 0:
        LOGGER.error("Error the call lsmod. Return value '%s'", return_value)

    is_loaded = False

    LOGGER.debug("parse lsmod output")
    for line in output.split("\n"):
        if KERNEL_MODULE_NAME in line:
            is_loaded = True

    LOGGER.debug("the kernel module is loaded: '%s'", is_loaded)

    return is_loaded

def load_kernel_module():
    """
    Load the kernel module with insmod

    Returns the return code of insmod
    """

    import subprocess
    import shlex

    LOGGER.debug("create commando")
    command = "insmod {}".format(KERNEL_MODULE_NAME)

    LOGGER.debug("command: %s", command)
    return_value = subprocess.call(shlex.split(command))

    LOGGER.debug("return value: %s", return_value)
    return return_value

def unload_kernel_module():
    """
    Unload the kernel module with rmmod

    Returns the return code of rmmod
    """

    import subprocess
    import shlex

    LOGGER.debug("create commando")
    command = "rmmod {}".format(KERNEL_MODULE_NAME)

    LOGGER.debug("command: %s", command)
    return_value = subprocess.call(shlex.split(command))

    LOGGER.debug("return value: %s", return_value)
    return return_value

def is_user_root():
    """
    Check if user root

    Return True or False
    """

    import os

    LOGGER.debug("check root")
    root = os.geteuid() == 0

    LOGGER.debug("is user root: %s", root)
    return root

def is_module_in_modulefile():
    """
    Check if module in /etc/modules

    Return True or False
    """

    is_exist = False

    try:
        LOGGER.debug("read /etc/modules")
        with open("/etc/modules", "r") as file:
            for line in file.readlines():
                if KERNEL_MODULE_NAME in line:
                    is_exist = True
    except IOError as err:
        LOGGER.exception(err)

    LOGGER.debug("the module is in file '%s'", is_exist)

    return is_exist

def activate_automatic_module_start():
    """
    Append the module into /etc/modules for start at booting
    """

    is_exist = is_module_in_modulefile()

    if is_exist is False:
        try:
            LOGGER.debug("edit /etc/modules")
            with open("/etc/modules", "a") as file:
                file.seek(2)
                file.write(KERNEL_MODULE_NAME)
                file.write("\n")
        except IOError as err:
            LOGGER.exception(err)

def deactivate_automatic_module_start():
    """
    Remove the module from /etc/modules
    """

    is_exist = is_module_in_modulefile()

    if is_exist:
        try:
            LOGGER.debug("edit /etc/modules")
            with open("/etc/modules", "r+") as file:
                d = file.readlines()
                file.seek(0)
                for i in d:
                    if i != "{}\n".format(KERNEL_MODULE_NAME):
                        file.write(i)
                file.truncate()
        except IOError as err:
            LOGGER.exception(err)

def create_modprobe_file(mode, brightness, colors ,state):
    """
    Generate module optionsfile

    Args:
        mode: Number (Values between 0 - 7)
        brightness: Number (Values between 1 - 10)
        colors: List with the colors
        state: Number (Values 0 and 1)
    """

    import os

    LOGGER.debug("Generate filename")
    filename = os.path.join("/etc/modprobe.d/", "{}_options.conf".format(KERNEL_MODULE_NAME))
    LOGGER.debug("Filename: %s", filename)

    options = []

    LOGGER.debug("check mode")
    if mode != "":
        options.append("kb_mode={}".format(mode))

    LOGGER.debug("check brightness")
    if brightness != "":
        options.append("kb_brightness={}".format(brightness))

    LOGGER.debug("check colors")
    if len(colors) == 3:
        options.append("kb_color={left_color},{middle_color},{right_color}"
                        .format(left_color=colors["left"], 
                                middle_color=colors["middle"], 
                                right_color=colors["right"]))

    LOGGER.debug("check state")
    if state != "":
        options.append("kb_mode={}".format(state))

    LOGGER.debug("check file exist")
    if os.path.exists(filename):
        os.remove(filename)

    if len(options) >= 1:
        try:
            LOGGER.debug("write file")
            LOGGER.debug("file content: %s", " ".join(options))
            with open(filename, "w") as file:
                file.write("options {} ".format(KERNEL_MODULE_NAME))
                file.write(" ".join(options))
        except IOError as err:
            LOGGER.exception(err)

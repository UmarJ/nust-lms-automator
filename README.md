# NUST LMS Automator

A small script to automatically download all course materials from the NUST Learning Management System (LMS) Online Portal.

**Updated to work with new LMS.**

----
## Installation Guide

_This guide assumes that you have you have your Python binary under `python` and pip under `pip`. Depending on your installation, you may have to run `python3` or `py` for Python and `pip3` for pip. You can change this behaviour using Symbolic Links._

### Cloning the Repository 
If you have `git` installed, you can clone this repository using

```
git clone <url_of_this_page>
```

Otherwise you can Download and Extract this repository in ZIP Format using the "Download ZIP" button at the top.

### Installing Dependencies 

Make sure you have Python with pip installed. Run

```
pip install -r requirements.txt
```

### Editing The Config File

The config.py file contains the following variables:

| Variable | Function |
| -------- | -------- |
| USERNAME | Your LMS Username. |
| PASSWORD | Your LMS Password. |
| COURSE_LINKS | Links to courses that you want to download course materials for. |
| ALIASES | If you want course materials for a specific course to be placed in a different subdirectory, you can specify the name for that subdirectory here. Add a key-value pair to the dictionary with the key equal to the name of the course on LMS and the value equal to the preferred name of the subdirectory. |
| DOWNLOAD_DIRECTORY | Absolute path of the download directory. Set it to None to download in the current directory. |
| LAB_MANUALS_DIR | Directory inside `DOWNLOAD_DIRECTORY` where lab manuals are saved. Set it to `None` to download in the same directory as other files. |

## Running the Script

Copy the config file and the script download.py to the directory where you want folders for courses to be made and navigate to it using Command Prompt/Terminal. Then run

```
python download.py
```

## Automatically Running this Script

### Windows

Follow [this guide](https://towardsdatascience.com/automate-your-python-scripts-with-task-scheduler-661d0a40b279).

### Linux

Use a [cron job](https://www.ostechnix.com/a-beginners-guide-to-cron-jobs/).

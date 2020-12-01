 NUST LMS Automator

A small script to automatically download all course materials from the NUST Learning Management System (lMS) Online Portal.

----
## Installation Guide

_This guide assumes that you have you have your Python binary under `python` and pip under `pip`. Depending on your installation, you may have to run `python3` or `py` for Python and `pip3` for pip. You can change that behavious using Symbolic Links._

### Cloning the Repository 
If you have `git` installled, you can clone this repository using 
```
git clone <url_of_this_page>
```
Otherwise you can Downlaod and Extract this repository in ZIP Format using the "Download ZIP" button at the top.

### Installing the Dependencies 
Make sure you have Python with pip installed. Run,
```
pip install -r requirements.txt
```
You can optionally create and activate a virtual environment first using,

### Editing The Config File Information

The config.py file contains the following variables:

USERNAME: Edit it to match your LMS Username

PASSWORD: Put your username under this.

IGNORED_COURSES: Changed this to an array of courses that you do not want to download

ALIASES: If you don't like the name of a course on LMS and want its course materials to be placed in a different folder, you can specify the name for the alternate folder here. Just add an element with a key equal to the name of the course and value equal to the folder that you want to copy it's contents to.

### Running the Script

Copy the config file and the script download.py to the directory where you want folders for courses to be made and navigate to it using Command Prompt/Terminal. Finally run,
```
python download.py
```

## Automatically Running this Script

### Windows

Follow [this guide](https://towardsdatascience.com/automate-your-python-scripts-with-task-scheduler-661d0a40b279).

### Linux

Use a [cron job](https://www.ostechnix.com/a-beginners-guide-to-cron-jobs/).
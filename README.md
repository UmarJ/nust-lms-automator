# NUST LMS Automator

Python3 is needed for this script.

## Installing Required Modules

### Windows

```
python -m pip install beautifulsoup4
python -m pip install lxml
python -m pip install mechanize
```

### Linux

```
pip3 install beautifulsoup4
pip3 install lxml
pip3 install mechanize
```

## Config File Information

#### Username
Put your username under this.

#### Password
Put your username under this.

#### Ignored Courses
If you don't want to automatically download course materials for an enrolled course, you can copy its name from LMS and put it under this.

#### Aliases
If you don't like the name of a course on LMS and want its course materials to be placed in a different folder, you can specify the name for the alternate folder here. Just copy the name of the course on the first line, and its preferred name on the next line. There is no limit to the number of courses that can be added.

## Running the Script

Copy the config file and the script download.py to the directory where you want folders for courses to be made and navigate to it using Command Prompt/Terminal.

### Windows

```
python download.py
```

### Linux

```
python3 download.py
```

## Automatically Running this Script

### Windows

Follow [this guide](https://towardsdatascience.com/automate-your-python-scripts-with-task-scheduler-661d0a40b279).

### Linux

Use a [cron job](https://www.ostechnix.com/a-beginners-guide-to-cron-jobs/).
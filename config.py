# Your LMS Credentials
USERNAME = "<Your Username Here>"
PASSWORD = "<Your Password Here>"

# Courses that you want to download
COURSE_LINKS = ["https://lms.nust.edu.pk/portal/course/view.php?id=00000",
                "https://lms.nust.edu.pk/portal/course/view.php?id=00000",
                "https://lms.nust.edu.pk/portal/course/view.php?id=00000"
                ]

# Mapping of Course Names to Folder Names
ALIASES = {"HU212 Technical & Business Writing BSCS-8ABC -- (Fall'19)": "Technical & Business Writing",
           "MATH222 Linear Algebra BSCS-8A -- (Fall'19)": "Linear Algebra",
           "CS220 Database Systems BSCS-8AB -- (Fall'19)": "Database Systems",
           "CS250 Data Structures & Algorithms BSCS-8AB -- (Fall'19)": "Data Structures & Algorithms"
           }

# Absolute path of directory to save files into e.g. "~/NUST/1st Semester" for Linux or
# "E:/NUST/1st Semester" for Windows
# Set to None for current directory
DOWNLOAD_DIRECTORY = None

# Directory to save lab manuals into (files containing 'lab' in the filename)
# This directory will be created inside DOWNLOAD_DIRECTORY
# Set to None to save in the same directory as other files
LAB_MANUALS_DIR = "Lab Manuals"

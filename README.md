# UBC Course Crawler

## Disclaimer and Terms of Use
Your use of this software is deemed acceptance of these terms. This software, including all the source code, is offered without any warranties or conditions, express or implied, as to its use, functionality, or legality. The author(s) will not be held responsible for your use of this software and any consequences arising from your use of this software. The author(s) note that since this software was first developed, the University of British Columbia ("UBC") has updated its website policies and it may not be possible to legally use this software. You should seek independent legal advice before using this software in order to ascertain whether the software can be legally used in keeping with all UBC website terms of use, UBC policies, and any other applicable law or policies. The author(s) will not be held responsible for illegal or non-compliant use of this software in contravention of any law or UBC policies. The author(s) will furthermore not be held liable for any use of modified versions of this software. Your use of this software is entirely at your own risk.

## About
UBC Course Crawler automatically looks up a list of courses, and then creates a table of available courses, sorted by day and block. Specifically, it groups courses by Mon/Wed/Fri or Tue/Thur, so that you may efficiently register for your courses. This program can check course availability for 100 courses in less than 2 minutes and then automatically sort them; to do that manually would take several hours.

NOTE: this program has an intentional pause between requests to UBC's SSC website, so as not to slow the server down. Please do not change this.

## Requirements:
* BeautifulSoup4 (install via easy_install or pip)

## Usage instructions:
* Copy/paste the list of courses that you would like to register for in courseList.csv
* Run "python crawler.py" at the command-line
* See your available courses, sorted by day and time, in courseList.html!

**NOTE: this program used to also have the ability to directly register for courses automatically, but this functionality has been removed for three reasons:**
* Login information was challenging
* Could easily allow the user to exploit access to the UBC SSC website, violating UBC's terms of use (the existence of the program itself would not be in violation, however, but I do not wish to encourage irresponsible usage)
* While it was relatively easy for the program to receive a ranking of course preferences, it was difficult (as the user) to rank these courses ahead of time, especially without knowing which courses overlapped and needed to be directly compared.

For the reasons stated above, I have removed the automatic course signup functionality and instead opted for outputting an html file which creates a table of available courses, sorted by day and block.

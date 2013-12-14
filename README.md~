UBC Course Crawler
=================

UBC Course Crawler automatically looks up a list of courses, and then creates a table of available courses, sorted by day and block. Specifically, it groups courses by Mon/Wed/Fri or Tue/Thur, so that you may efficiently register for your courses. This program can check course availability for 100 courses in less than 2 minutes and then automatically sort them; to do that manually would take several hours.

NOTE: this program has an intentional pause between requests to UBC's SSC website, so as not to slow the server down. Please do not change this.

================

Requirements:
- BeautifulSoup4 (install via easy_install or pip)

Useage instructions:
1) Copy/paste the list of courses that you would like to register for in courseList.csv

2) Run "python crawler.py" at the command-line

3) See your available courses, sorted by day and time, in courseList.html!

NOTE: this program used to also have the ability to directly register for courses automatically, but this functionality was buggy for two reasons:
1) Login information was challenging
2) While it was relatively easy for the program to receive a ranking of course preferences, it was difficult (as the user) to rank these courses ahead of time, especially without knowing which courses overlapped and needed to be directly compared.

Therefore, I have removed the automatic course signup functionality and instead opted for outputting an html file which creates a table of available courses, sorted by day and block.



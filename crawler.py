import urllib
import urllib2
import requests
import time
from libs.grabber import urlgrab
from libs.progress import text_progress_meter
from bs4 import BeautifulSoup
import cookielib
import re
import sys
from datetime import datetime
import operator
# BeautifulSoup needs a bigger recursion to parse the latest.php file
sys.setrecursionlimit(9000)


DEBUG = False
# Get general information from the soup


s = requests.Session()
response = s.get('https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=sectsearch')
soup = BeautifulSoup(response.text)

url = 'https://courses.students.ubc.ca' + soup.find_all('form')[2]['action'].strip()

Cookie = ''
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:22.0) Gecko/20100101 Firefox/22.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Referer': 'https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=sectsearch',
    'Accept-Encoding': 'gzip, deflate',
    'Cookie': Cookie
}

values = {'subj' : 'HIST',
          'crsno' : '102',
          'SECTION_SEARCH_KEYWORD' : '',
          'actv' : '--Any--',
          'credit' : '',
          'term' : '--Any--',
          'seat' : '--Any--',
          'sTime' : '',
          'eTime' : '',
          'scrsz' : '20',
          'submit' : 'Search+for+Sections'}


response = s.post(url,data=values,headers=headers)
the_page = response.text
if DEBUG:
    f = open('debugSearchResults.html', 'r')
    the_page = f.read()
    f.close()

soup = BeautifulSoup(the_page, 'lxml')
soup.find_all("tr", class_="section1")

    

# The ubc doc works like this: section1 tontains the name
# soup.find_all("tr", class_="section1")[1].find_all('td')[X]
# X:0: Full or space, to indicate class size
# X=1: Ignore... better to use 'a' tag to get course name
# X=2: Discussion or Lecture
# X=3: '1' or '2' or '1-2'  (to indicate term) 
# X=4: Interval... ignore
# X=5: Fri... indicates days, by first three letters
# X=6: Start time in 24hour format
# X=7: End time in 24hour format
# X=8: Section comments
# soup.find_all("tr", class_="section1")[0].a['href'] to get url
class Course:
    def __init__(self, subject, courseNumber, sectionNumber, space, type, term, days, startTime, endTime, comments,href,description, prereq):
        self.subject = subject
        self.courseNumber = courseNumber
        self.sectionNumber = sectionNumber
        self.space = space
        self.type = type
        self.term = term
        self.days = days
        self.startTime = startTime
        self.endTime = endTime
        self.comments = comments
        self.href = href
        self.description = description
        self.prereq = prereq


def getCourses(currentCourseList, subj, courseNumber,description,prereq):
    print 'URL = ' + url
    values = {'subj' : subj.strip(),
          'crsno' : str(courseNumber).strip(),
          'SECTION_SEARCH_KEYWORD' : '',
          'actv' : '--Any--',
          'credit' : '',
          'term' : '--Any--',
          'seat' : '--Any--',
          'sTime' : '',
          'eTime' : '',
          'scrsz' : '20',
          'submit' : 'Search+for+Sections'}

    response = s.post(url,data=values,headers=headers)
    the_page = response.text
    if DEBUG:
        f = open('debugSearchResults.html', 'r')
        the_page = f.read()
        f.close()
    soup = BeautifulSoup(the_page, 'lxml')
    
    # The following gets the course name in full ie. 'HIST 102 L1D'
    #soup.find_all("tr", class_="section1")[2].a.string.strip()
    
    for i in range(len(soup.find_all("tr", { "class" : re.compile(r"section[1-2]") }))):
        tr = soup.find_all("tr", { "class" : re.compile(r"section[1-2]") })[i]

        # Initialize some values that may not always have a value

        courseName = tr.a.string.strip().split()
        courseName = [c.replace(u'\xa0', u' ') for c in courseName]
        # The ubc doc works like this: section1 tontains the name
        # soup.find_all("tr", class_="section1")[1].find_all('td')[X]
        # X:0: Full or space, to indicate class size
        space = tr.find_all('td')[0].string or ""
        space = space.replace(u'\xa0', u' ')
        # X=1: Ignore... better to use 'a' tag to get course name
        # X=2: Discussion or Lecture
        type = tr.find_all('td')[2].string or ""
        type = type.replace(u'\xa0', u' ')
        # X=3: '1' or '2' or '1-2'  (to indicate term) 
        term = tr.find_all('td')[3].string or ""
        term = term.replace(u'\xa0', u' ')
        # X=4: Interval... ignore
        # X=5: Fri... indicates days, by first three letters
        days = tr.find_all('td')[5].string or ""
        days = days.replace(u'\xa0', u' ')
        # X=6: Start time in 24hour format
        startTime = tr.find_all('td')[6].string or ""
        startTime = startTime.replace(u'\xa0', u' ')
        # X=7: End time in 24hour format
        endTime = tr.find_all('td')[7].string or ""
        endTime = endTime.replace(u'\xa0', u' ')
        # X=8: Section comments
        comments = tr.find_all('td')[8].string or ""
        comments = comments.replace(u'\xa0', u' ')
        # soup.find_all("tr", class_="section1")[0].a['href'] to get url
        href = tr.a['href'] or ""
        href = href.replace(u'\xa0', u' ')
        # Fix time objects to ensure that they are 24 hours XX:XX format
        if len(str(startTime).split(':')[0]) < 2:
               startTime = '0' + startTime
        if len(str(endTime).split(':')[0]) < 2:
               endTime = '0' + endTime
        # (subject, courseNumber, sectionNumber, space, type, term, days, startTime, endTime, comments
        #currentCourseList.append(Course(courseName[0].encode('utf-8'),courseName[1].encode('utf-8'),courseName[2].encode('utf-8'),space.encode('utf-8'),type.encode('utf-8'),term.encode('utf-8'),days.encode('utf-8'),startTime.encode('utf-8'),endTime.encode('utf-8'),comments.encode('utf-8'),href.encode('utf-8'),description.encode('utf-8'),prereq.encode('utf-8')))
        currentCourseList.append(Course(str(courseName[0]),str(courseName[1]),str(courseName[2]),str(space),str(type),str(term),str(days),str(startTime),str(endTime),str(comments),str(href),str(description),str(prereq)))

    return currentCourseList


def writeCourseListRow(html, course, color):
    if color == True:
        html += '<tr style="background-color:blue;color:white">'
    else:
        html += '<tr style="">'
    html += '<td>' + course.space + '</td>'
    html += '<td>' + course.subject + '</td>'
    html += '<td>' + course.courseNumber + '</td>'
    html += '<td><a target="_blank" href="https://courses.students.ubc.ca'+ course.href + '">' + course.sectionNumber + '</a></td>'
    html += '<td>' + course.term + '</td>'
    html += '<td>' + course.days + '</td>'
    html += '<td>' + course.startTime + '</td>'
    html += '<td>' + course.endTime + '</td>'
    html += '<td width="200px">' + course.comments + '</td>'
    html += '<td width="200px">' + course.description + '</td>'
    html += '<td>' + course.prereq + '</td>'
    html += '</tr>'
    return html

def writeCourseList(CourseList):
    f = open('courseList.html','w')
    html = '<!DOCTYPE html>\n<html><head><meta charset="UTF-8"><style>body { font-family:Arial;font-size:1.2em;}</style><title>Course List</title></head><body>'
    
    html += '<h1>UBC Course Planner updated on: ' + str(datetime.now()) + '</h1>'

    T1MWFCourseList = []
    T1TTCourseList = []
    T2MWFCourseList = []
    T2TTCourseList = []
    T12CourseList = []
    
    for course in CourseList:
        if '1-2' in course.term:
            T12CourseList.append(course)
        elif '1' in course.term:
            if 'Mon' in course.days or 'Wed' in course.days or 'Fri' in course.days:
                T1MWFCourseList.append(course)
            if 'Tue' in course.days or 'Thu' in course.days:
                T1TTCourseList.append(course)
        elif '2' in course.term:
            if 'Mon' in course.days or 'Wed' in course.days or 'Fri' in course.days:
                T2MWFCourseList.append(course)
            if 'Tue' in course.days or 'Thu' in course.days:
                T2TTCourseList.append(course)
        else:
            print 'WARNING: a course without a proper term: ' + course.subject + course.courseNumber

    T1MWFCourseList.sort(key=lambda x: x.startTime)
    T1TTCourseList.sort(key=lambda x: x.startTime)
    T2MWFCourseList.sort(key=lambda x: x.startTime)
    T2TTCourseList.sort(key=lambda x: x.startTime)
    T12CourseList.sort(key=lambda x: x.startTime)
    color = True
    # Select Term 1 MWF courses
    html += '<h2>Term 1 - Monday/Wednesday/Friday Courses</h2>'
    html += '<table cellpadding="10px">'
    for course in T1MWFCourseList:
        html = writeCourseListRow(html, course, color)
        if color == True:
            color = False
        else:
            color = True
    html += '</table>'
            
    # Select Term 1 TT courses
    html += '<h2>Term 1 - Tuesday/Thursday Courses</h2>'
    html += '<table cellpadding="10px">'
    for course in T1TTCourseList:
        html = writeCourseListRow(html, course, color)
        if color == True:
            color = False
        else:
            color = True
    html += '</table>'
            
    # Select Term 2 MWF courses
    html += '<h2>Term 2 - Monday/Wednesday/Friday Courses</h2>'
    html += '<table cellpadding="10px">'
    for course in T2MWFCourseList:
        html = writeCourseListRow(html, course, color)
        if color == True:
            color = False
        else:
            color = True
    html += '</table>'
            
    # Select Term 2 TT courses
    html += '<h2>Term 2 - Tuesday/Thursday Courses</h2>'
    html += '<table cellpadding="10px">'
    for course in T2TTCourseList:
        html = writeCourseListRow(html, course, color)
        if color == True:
            color = False
        else:
            color = True
    html += '</table>'
            
    # Select both term courses
    html += '<h2>Term 1 and 2 courses - mix of days</h2>'
    html += '<table cellpadding="10px">'
    for course in T12CourseList:
        html = writeCourseListRow(html, course, color)
        if color == True:
            color = False
        else:
            color = True
    html += '</table>'
    
    html += '</body></html>'
    f.write(html)
    f.close()        

print "Welcome to the UBC Course Lister"
print "Let us get to work..."
operation = input("Do you want to (1) look up the courses in the file or (2) look up a specific course: ")
CourseList = []
if operation == 1:
    f = open('courseList.csv', 'r')
    for line in f.readlines():
        line = line.split(',')
        # The first line is 'Code'
        if line[0] != 'Code':
            subject = line[0]
            courseNumber = line[2]
            description = line[4]
            prereq = line[5]
            CourseList = getCourses(CourseList,subject.strip(),courseNumber.strip(),description.strip(),prereq.strip())
            print 'Finished getting ' + subject + ' ' + courseNumber
            time.sleep(0.5)
    f.close()
    print '\n\nAll courses obtained!\n'
    for course in CourseList:
        print course.subject + ', ' + course.courseNumber + ', ' + course.sectionNumber + ', ' + course.space
    writeCourseList(CourseList)
elif operation == 2:
    subject = raw_input("Subject: ").strip()
    courseNumber  = raw_input("Course Number: ").strip()
    CourseList = getCourses(CourseList,subject.strip(),courseNumber.strip())
    for course in CourseList:
        print course.subject + ', ' + course.courseNumber + ', ' + course.sectionNumber + ', ' + course.space
    writeCourseList(CourseList)
else:
    print "\nERROR! Invalid command... please rerun script" 
    
print "Reached the end of the program"
    
 

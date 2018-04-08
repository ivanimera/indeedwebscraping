# coding: utf-8

# In[13]:

import re  # Regular expressions
import urllib.request  # Website connections
from bs4 import BeautifulSoup  # For HTML parsing
import DateTime  # show the current date and time
from time import sleep # To prevent overwhelming the server between connections
import csv

def text_cleaner(website):
    '''
    This function just cleans up the raw html so that I can look at it.
    Inputs: a URL to investigate
    Outputs: Cleaned text only
    '''
    try:
        site = urllib.request.urlopen(website).read()  # Connect to the job posting
    except:
        return  # Need this in case the website isn't there anymore or some other weird connection problem

    soup_obj = BeautifulSoup(site,"html.parser")  # Get the html from the site
    for script in soup_obj(["script", "style"]):
        script.extract()  # Remove these two elements from the BS4 object
    text = soup_obj.get_text()  # Get the text from this
    lines = (line.strip() for line in text.splitlines())  # break into lines
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))  # break multi-headlines into a line each

    def chunk_space(chunk):
        chunk_out = chunk + ' '  # Need to fix spacing issue
        return chunk_out

    text = ''.join(chunk_space(chunk) for chunk in chunks if chunk).encode('utf-8')  # Get rid of all blank lines and ends of line
    # Now clean out all of the unicode junk (this line works great!!!)

    try:
        text = text.decode('unicode_escape').encode('ascii', 'ignore')  # Need this as some websites aren't formatted
    except:  # in a way that this works, can occasionally throw
        return  # an exception

    text = re.sub("[^a-zA-Z.+3]", " ", str(text))  # Now get rid of any terms that aren't words (include 3 for d3.js)
    # Also include + for C++
    text = text.lower()  # Go to lower case and split them apart
    return text


# create my dictionary by using the important keywords
mydictionary_S = ['Python','Anaconda','Scikit','Matplotlib',\
                'Java','JavaScript','C++','C','Scala','Perl','Ruby','Canopy',\
                'R','Rstudio','Matlab','SAS','SPSS',\
                'Weka','BigML','Knime','DataRobot','LibSVM','H2O','RapidMiner',\
                'Mathematica','Chorus','Azure','Tensorflow','Stata',\
                'SQL','MySQL','Oracle','NoSQL','SQLite','PHP',\
                'Teradata','Cloudera','Solr','MapR','Lucene','ElasticSearch',\
                'Hadoop','Hive','MapReduce','Spark','Pig','HBase','Cassandra','Zookeeper', 'Kafka',\
                'Strata','Github','Tableau','Cognos','GraphLab',\
                'Linux','Bash','UNIX',\
                'Qlikview',\
                'Shiny','Alteryx','Spotfire','Plotly',\
                'Impala','Redshift','Omniture','ARCGIS','CoreMetrics',\
                'WebTrends','Caffe','OpenCV','GPGPU','Theano',\
                'PowerPivot','Pentaho','Microstrategy','Bokeh','Trifacta','Torch',\
                'VB','Excel','Powerpoint',\
                'Mahout','MongoDB','D3','Flume','Shark','D3.js','Oozie','Jupyter',\
                'Mathematics',\
                'Statistics','Math','Clustering',\
                'Economics',\
                'Communications','Team','Optimization','Creativity','Writing','Planning',\
                'Finance','Financial','Marketing','Insurance',\
                'Hospital','Health','Healthcare','Pharmaceutical','Cosmetic',\
                'tech','Manufacture']

mydictionary_D = ['Microsoft SQL Server','IBM DB2','Apache Hadoop','spark MLLib',\
                  'Google Charts','SAS Visual Analytics','Google Analytics', \
                  'Power BI', 'Oracle BI','BI software', 'Random Forests',\
                  'Adobe Analytics','Machine Learning','Artificial Intelligence',\
                  'Data Mining', 'Data Modeling', 'Deep Learning','Core Metrics', \
                  'Visual Basic','Natural Language Processing','Linear Regression', \
                  'Data Warehousing', 'Data Management', 'Data Visualization', 'Relational Databases', \
                  'Business Intelligence', 'Business Analysis', 'Business Objects', 'Business Solutions',\
                  'Data Science', 'Big Data', 'Data Analysis', 'Predictive Models', \
                  'Detail oriented','Extraction Transformation and Loading']

# for the search of data scientist,
# "BigML","Core Metrics","Extraction Transformation and Loading","H2O","Google Charts","IBM DB2","Trifacta","Strata" is not founded at all.

def text_mining(text,mydictionary_S,mydictionary_D):

    # convert all the single keywords to lower case
    thedict_S=[]
    for i in mydictionary_S:
        j=i.lower()
        thedict_S.append(j)

    # convert all the single keywords to lower case
    thedict_D=[]
    for i in mydictionary_D:
        j=i.lower()
        thedict_D.append(j)

    counter_list = []
    if text == None:
        return(counter_list)
    else:
        thetext = text.split()


        # count how many times the single keywords appear
        for k in thedict_S:
            a = thetext.count(k)
            if a == 0:
                d = 0
            else:
                d = 1

            counter_list.append(d)


        # count how many times the double or more than double keyword appear
        for k in thedict_D:
            b = re.findall(str(k),text)
            if b == []:
                c = 0
            else:
                c = 1


            counter_list.append(c)

        return(counter_list)



def total_jobs(search_job,state):
    # get the search page from indeed
    # final_site_list = ['http://www.indeed.com/jobs?q=', search_job] # vague match

    final_site_list = ['http://www.indeed.com/jobs?q="', search_job, '"&l="',state,'"']  # close match

    final_site = ''.join(final_site_list)  # Merge the html address together into one string
    html = urllib.request.urlopen(final_site).read()  # Open up the front page of our search first
    soup = BeautifulSoup(html, "html.parser")  # Get the html from the first page

    # Now find out how many jobs there were
    num_jobs_find = soup.find(id='searchCount').encode('utf-8')  # The 'searchCount' object has this
    num_jobs_area = str(num_jobs_find)

    # Now extract the total number of jobs found
    # From b'<div id="searchCount">Jobs 1 to 10 of 23,383</div>'
    job_numbers_list = re.findall(r'([\d\,]+)</div>', num_jobs_area)  # Extract the total jobs found from the search result
    job_numbers = job_numbers_list[0]
    separator_place = job_numbers.find(',')

    # delete the "," inside the job_numbers
    if len(job_numbers) > 3:
        # Have a total number of jobs greater than 1000
        total_num_jobs = (int(job_numbers[:separator_place]) * 1000) + int(job_numbers[separator_place + 1:])
    else:
        total_num_jobs = int(job_numbers)
    return(total_num_jobs)



# define state_list, because indeed limit the max number 1000 of showing the search result.
state_list = ['AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA',\
              'ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK',\
            'OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']


# define the header of excel file
theheader = ['Index','Job Title','Company Name','State','Location','URL']
for each in mydictionary_S:
    theheader.append(each)
for each in mydictionary_D:
    theheader.append(each)


def web_scarping(search_job):
    # calculate the number of pages
    # This will be how we know the number of times we need to iterate over each new search result page

    mycsv = csv.writer(open("pickles.csv", 'w'))
    mycsv.writerow(theheader)

    theindex = 1000000

    for state in state_list:
        final_site_list = ['http://www.indeed.com/jobs?q="', search_job, '"&l="', state, '"']  # close match
        final_site = ''.join(final_site_list)  # Merge the html address together into one string
        total_num_jobs = total_jobs(search_job,state)
        print('There were', total_num_jobs, 'jobs of', search_job, 'found in',state,'.')  # Display how many jobs were found
        print(DateTime.DateTime())  # show the current date and time

        if total_num_jobs % 10 == 0:
            num_pages = int(total_num_jobs / 10)
        else:
            num_pages = total_num_jobs // 10 + 1


        for i in range(1, num_pages +1):  # Loop through all of our search result pages
            print('Getting page', i)
            start_num = str(i * 10)  # Assign the multiplier of 10 to view the pages we want
            current_page = ''.join([final_site, '&start=', start_num])
            # Now that we can view the correct 10 job returns, start collecting the text samples from each

            html_page = urllib.request.urlopen(current_page).read()  # Get the page

            page_obj = BeautifulSoup(html_page, "html.parser")  # Locate all of the job links
            page_obj_h2 = page_obj.find_all('h2')  # where the job postings exist

            page_obj_span = page_obj.find_all('div', attrs={'class': ' row result'})
            page_obj_spanL = page_obj.find_all('div', attrs={'class': 'lastRow row result'})

            comp_name = []
            job_location = []
            for elem in page_obj_span:
                if elem.find('span', attrs={'class': 'company'})==None:
                    each_name = ''
                else:
                    each_name = elem.find('span', attrs={'class': 'company'}).getText().strip()
                comp_name.append(each_name)

                if elem.find('span', attrs={'itemprop': 'jobLocation'})==None:
                    each_loca = ''
                else:
                    each_loca = elem.find('span', attrs={'itemprop': 'jobLocation'}).getText().strip()
                job_location.append(each_loca)


            for elem1 in page_obj_spanL:
                if elem1.find('span', attrs={'class': 'company'})== None:
                    each_name1 = ''
                else:
                    each_name1 = elem1.find('span', attrs={'class': 'company'}).getText().strip()
                comp_name.append(each_name1)

                if elem1.find('span', attrs={'itemprop': 'jobLocation'})==None:
                    each_loca1 = ''
                else:
                    each_loca1 = elem1.find('span', attrs={'itemprop': 'jobLocation'}).getText().strip()
                job_location.append(each_loca1)

            m=0
            for link in page_obj_h2:
                print('Getting information of job position with index =',theindex)

                job_link = re.findall(r'href="(.*?)"', str(link))
                job_URLS = base_url + str(job_link[0])

                job_title = re.findall(r'title="(.*?)"', str(link))

                mytext = text_cleaner(job_URLS)
                the_result = []
                the_result.append(theindex)
                the_result.append(job_title)
                the_result.append(comp_name[m])
                the_result.append(state)
                the_result.append(job_location[m])
                the_result.append(job_URLS)
                items = text_mining(mytext,mydictionary_S,mydictionary_D)
                for each in items:
                    the_result.append(each)
                try:
                    mycsv.writerow(the_result)
                except:
                    "The WebPage couldn't be saved to Excel file."

                theindex += 1
                m += 1

                sleep(1)  # So that we don't be jerks. If you have a very fast internet connection you could hit the server a lot!


# define the key word of job title which is used for search

base_url = 'http://www.indeed.com'

# web_scarping(search_job)

# search_job = 'data+analyst'  # searching for data scientist exact fit("data scientist" on Indeed search)
search_job = 'data+scientist'  # searching for data scientist exact fit("data scientist" on Indeed search)
web_scarping(search_job)


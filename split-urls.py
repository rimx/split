import sys
import requests
import math
from datetime import datetime

startTime = datetime.now()

domains = {
  'uk_division_web_live':'https://www.statravel.co.uk', 
  'de_division_web_live': 'https://www.statravel.de'
}
#read 2 params
if len(sys.argv) < 3:
  print("Please pass the project folder as param1 and redirect file as param2")
  print("i.e. python split.py uk_division_web_live get-redirects-uk-en")
  quit()
else:
  project = sys.argv[1] 
  redirect = sys.argv[2]
  domain = domains[project]
  # Get the urls from the API
  api = "http://s607650rgvl190.bluee.net:8080/cps/rde/rest/v1/project/"+project+"/contents?group=content&type=HTML&sortorder=asc&sortedby=changed&chunksize=250&chunk="
  print ("Start crawling URL's from "+ api +" ...")
  response = requests.get(api)
  data = response.json()
  num_of_pages = int(data['hits'])
  iteration_needed = math.ceil(num_of_pages/250)

  pages = set()
  for p in range(1, iteration_needed +1):
    contents = requests.get(api+str(p)).json()['contents']
    #loop through the contents array and find out only name with html extension
    contents_length = len(contents)
    for x in range(0, contents_length):

      if contents[x]['name'][-4:] == '.htm':
       pages.add(contents[x]['name'])
  
  # now we have all the pages with .htm in DS
  # lets check the files in the redirect file 
  print ("Done with crawling ...")
  # Update : 17.04:2018
  # save all get urls
  with open('gets_urls.txt', 'w') as f:
    for p in pages:
      f.write(domain + '/' + p + "\n")
  quit()
  print ("Opening the file "+ redirect +" ...")
  lines = set()
  with open(redirect) as f:
    for line in f:
      # strip new lines and split on tab - get the first value, right strip /-
      # debug : there are some strings separated by space - split them as well
      # debug : get rid of params
      # split on / and get the last value - it should be the page name
      line = line.strip().split("\t")[0].split(" ")[0].rstrip('/-').rstrip('\-').split('/')[-1].split("?")[0].split("#")[0]
      lines.add(line)
  print ("Done with file reading ...")
  print ("Start processing ...")
  # filter out empty values and get the unique URL's
  lines = set(filter(None, lines))
  redirect_in_zxtm = set()
  redirect_in_cms = set()
  delete_from_project = set()
  # now loop throug lines and check if it exists in the project
  # url without .htm -> redirect using ZXTM
  # url exist in the project -> redirect using CMS
  # url doesn't exist in the project -> delete them 

  for path in lines:
    
    if path[-4:] != '.htm':
      redirect_in_zxtm.add(path)
    elif path in pages:
      redirect_in_cms.add(path)
    else:
      #delete_from_project.add(path)
      session = requests.Session()
      session.max_redirects = 5
      session.timeout = 5
      headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'}
      url = domain + '/' + path.rstrip()
      print(url);
      csv_line="";
      try:
        response = session.get(url, headers = headers)
        if response.history:
          # loop through the history
          for resp in response.history:
            csv_line+= resp.url + "("+str(resp.status_code) + ");"
          # final destination
          csv_line+= response.url + "("+str(response.status_code) + ");"
        else:
          csv_line+= response.url + "("+str(response.status_code) + ")"
        #add the line to set  
        delete_from_project.add(csv_line.rstrip(";"))
      except requests.exceptions.RequestException as e:
        r = e.response
        print (r)
  redirect_in_zxtm_headline = '*'*72 + "\n Can be redirected in ZXTM \n" + " Total Pages : " + str(len(redirect_in_zxtm)) + "\n" +  '*'*72 + "\n"
  redirect_in_cms_headline = '*'*72 + "\n Can be redirected in CMS \n" + " Total Pages : " + str(len(redirect_in_cms)) + "\n" +  '*'*72 + "\n"
  delete_from_project_headline = '*'*72 + "\n Can be deleted in CMS \n" + " Total Pages : " + str(len(delete_from_project)) + "\n" +  '*'*72 + "\n"
   #wtite the files
  with open('redirect_in_zxtm.txt', 'w') as f:
    f.write(redirect_in_zxtm_headline)
    f.write('\n'.join(redirect_in_zxtm))
  with open('redirect_in_cms.txt', 'w') as f:
    f.write(redirect_in_cms_headline)
    f.write('\n'.join(redirect_in_cms))
  with open('delete_from_project.txt', 'w') as f:
    f.write(delete_from_project_headline)
    f.write('\n'.join(delete_from_project))
  #print to console
  print(redirect_in_zxtm_headline)
  print (redirect_in_zxtm)
  print(redirect_in_cms_headline)
  print (redirect_in_cms)
  print(delete_from_project_headline)
  print (delete_from_project)

  print("Time taken in  hh:mm:ss => " + str(datetime.now() - startTime))
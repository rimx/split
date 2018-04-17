import sys
import requests

domains = {
  'uk_division_web_live':'https://www.statravel.co.uk'
}

with open('delete_from_project.txt') as f:
  domain = domains['uk_division_web_live']
  session = requests.Session()
  session.max_redirects = 5
  session.timeout = 5
  lines = set()
  for line in f:
    url = domain + '/' + line.rstrip()
    line="";
    try:
      response = session.head("https://www.statravel.co.uk/buy-foreign-currency.htm")
      if response.history:
        # loop through the history
        for resp in response.history:
          line+= resp.url + "("+str(resp.status_code) + ");"
        # final destination
        line+= response.url + "("+str(response.status_code) + ");"
      else:
        line+= response.url + "("+str(response.status_code) + ")"
      #add the line to set
      lines.add(line.rstrip(";"))
    except requests.exceptions.RequestException as e:
      r = exc.response
      print (r)

  print(lines)  

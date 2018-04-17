import sys
import requests

domains = {
  'uk_division_web_live':'https://www.statravel.co.uk'
}
session = requests.Session()
session.max_redirects = 5
session.timeout = 5
headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'}
lines = set()
line=""
try:
  response = session.get("https://www.statravel.co.uk/buy-foreign-currency.htm", headers=headers, timeout =4)
  print(response)
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
  r = e.response
  print("response")
  print (r)

  print(lines)  

import urllib, requests
import json



username = 'databrugis'
password = 'databrugis'

url = 'http://127.0.0.1:8000/tablestates/'
data = urllib.urlencode({
        'username':username,
        'password':password,
    })
# return the url to the user in the email template
#print url
#data = urllib.urlopen(url)
#line = data.readlines()
#print "Read Line: %s" % (line)


resp = requests.get(url,auth=('databrugis', 'databrugis'))
if(resp.ok):

    # Loading the response data into a dict variable
    # json.loads takes in only binary or string variables so using content to fetch binary content
    # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
    jData = json.loads(resp.content)

    print("The response contains {0} properties".format(len(jData)))
    print("\n")
    for key in jData:
        print key + " : " + str(jData[key])
else:
    # If response code is not ok (200), print the resulting http error code with description
    resp.raise_for_status()
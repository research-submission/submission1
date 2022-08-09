import json
import time
import requests 

#Load credentials
creds = json.load(open('credentials.json','r'))

#Call the API and handle backoff
def call(url, params):
    print(url)
    print(params)
    time.sleep(0.5)
    resp = requests.get(url, params)
    obj = resp.json()
    for key in obj.keys():
      if key != 'items':
        print(key +':'+ str(obj[key]))
    if 'backoff' in obj:
      print("Backing off for {}".format(obj['backoff']))
      time.sleep(obj['backoff'])
    return obj

#Form an API query, adding in the site and key,
#and handle pagination of results.
def makequery(path, params, outfile, get_all=True):
  url = "https://api.stackexchange.com/2.2/"+path
  params['site'] = 'security'
  params['key'] = creds['key']
  outhandle = open(outfile, 'a')
  obj = call(url, params)
  for itm in obj['items']:
    outhandle.write(json.dumps(itm)+'\n')
  if 'page' not in params:
    params['page'] = 2
  while get_all and obj['has_more'] == True:
    obj = call(url, params)
    for itm in obj['items']:
      outhandle.write(json.dumps(itm)+'\n')
    params['page'] += 1
  return

#Get all questions on the site, using a filter that asks for all answers to be
#included in the response, with the max 100 responses/page.
params = {}
params['filter'] = creds['filter']
params['page'] = 1
params['sort'] = 'creation'
params['order'] = 'asc'
params['pagesize'] = 100
makequery('questions', params, 'data/all/questions.json')

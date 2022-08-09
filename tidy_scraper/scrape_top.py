import json
import time
import requests 

creds = json.load(open('credentials.json','r'))

def call(url, params):
    print(url)
    print(params)
    time.sleep(0.5)
    resp = requests.get(url, params)
    obj = resp.json()
    if 'backoff' in obj:
      print("Backing off for {}".format(obj['backoff']))
      time.sleep(obj['backoff'])
    return obj

#Form an API query, adding in the site and key,
#and handle pagination of results.
def makequery(path, params, get_all=True):
  url = "https://api.stackexchange.com/2.2/"+path
  params['site'] = 'security'
  params['key'] = creds['key']
  objlist = []
  obj = call(url, params)
  objlist += obj['items']
  params['page'] = 2
  while get_all and obj['has_more'] == True:
    obj = call(url, params)
    objlist += obj['items']
    params['page'] += 1
  params['page'] = 1
  return objlist


#Get the static profile information about each user listed in
#`uidfile` and their first page of answers as sorted by votes.
def getusers(uidfile, outdir, pagesize=10):
  uids = [u[7:u.rindex('/')] for u in open(uidfile,'r')]
  ustr = ';'.join(uids)
  params = {}
  params['filter'] = creds['filter']
  json.dump(makequery('users/'+ustr, params), open(outdir+'users.json','w'))
  params['sort'] = 'votes'
  params['pagesize'] = pagesize
  answerlist = []
  for uid in uids:
    answers = makequery('users/'+uid+'/answers', params, get_all=False)
    answerlist.append(answers)
  json.dump(answerlist, open(outdir+'answers.json','w'))
  return


#From a list of answer objects, query for information about questions.
#This is less efficient than using the method in scrape_all.
def getquestions(answerfile, outdir):
  ansobj = json.load(open(answerfile, 'r'))
  quids = list(set([str(ans['question_id']) for ulist in ansobj for ans in ulist]))
  params = {}
  params['filter'] = creds['filter']
  questionlist = []
  for i in range(0, len(quids), 99):
    questionlist += makequery('questions/'+';'.join(quids[i:i+99]), params)
  json.dump(questionlist, open(outdir+'questions.json','w'))
  return


# Basic info about the site.
json.dump(makequery('info', {}), open('data/siteinfo.json','w'))

#Get users and top-100 answers from the UIDs provided
getusers('data/alltop100/users', 'data/alltop100x100/', pagesize=100)

#Get the questions corresponding to the top 100 answers
getquestions('data/alltop100x100/answers.json','data/alltop100x100/')

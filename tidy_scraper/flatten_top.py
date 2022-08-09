import json
import csv

def translateusers(jsonfile, csvfile):
  fields = ['user_id','user_type','is_employee','display_name','about_me','website_url','location','reputation','badges_bronze','badges_silver','badges_gold','accept_rate','view_count','down_vote_count','up_vote_count','answer_count','question_count','creation_date','last_access_date','last_modified_date','profile_image','link']
  csvout = csv.DictWriter(open(csvfile, 'w'), fieldnames=fields)
  csvout.writeheader()
  jsonin = json.load(open(jsonfile,'r'))
  
  for udict in jsonin:
    out = {}
    for field in fields:
      if 'badge' in field:
        out[field] = udict['badge_counts'][field[7:]]
      elif field not in udict:
        out[field] = ''
      else:
        out[field] = udict[field]
    csvout.writerow(out)


def getquestion(qlist, quid):
  for q in qlist:
    if q['question_id'] == quid:
      return q
  return None


def timestats(ans, question):
  atimes = [a['creation_date'] for a in question['answers']]
  isfirstanswer = min(atimes) == ans['creation_date']
  islastanswer  = max(atimes) == ans['creation_date']
  timediff = ans['creation_date'] - question['creation_date']
  return (isfirstanswer, islastanswer, timediff)

def wonbounty(ans):
  if 'awarded_bounty_amount' in ans:
    return True
  return False

def askedquestion(ans, question):
  if 'user_id' not in question['owner']:
    return False
  return ans['owner']['user_id'] == question['owner']['user_id']



def translateanswers(datadir):
  answers = json.load(open(datadir+'answers.json','r'))
  questions = json.load(open(datadir+'questions.json','r'))

  qfields =  ['question_title','question_body','question_link','question_creation_date','question_last_edit_date','question_last_activity_date','question_answer_count','question_score','question_up_vote_count','question_down_vote_count','question_reopen_vote_count','question_delete_vote_count','question_comment_count','question_tags']
  afields =  ['answer_body','answer_link','answer_content_license','answer_creation_date','answer_last_edit_date','answer_last_activity_date','answer_score','answer_is_accepted','answer_up_vote_count','answer_down_vote_count','answer_comment_count','answer_tags']
  sfields = ['answer_is_first_answer','answer_is_last_answer','answer_timediff','answer_won_bounty','answer_own_question']
  fields = ['answer_id','question_id','user_id'] + qfields + afields + sfields
  csvout = csv.DictWriter(open(datadir+'answers.csv', 'w'), fieldnames=fields)
  csvout.writeheader()

  for ulist in answers:
    for topans in ulist:
      out = {}
      question = getquestion(questions, topans['question_id'])
      out['question_id']  = topans['question_id']
      out['answer_id']    = topans['answer_id']
      out['user_id']      = topans['owner']['user_id']
      out['answer_is_first_answer'],out['answer_is_last_answer'],out['answer_timediff'] = timestats(topans, question)
      out['answer_own_question'] = askedquestion(topans,question)
      out['answer_won_bounty'] = wonbounty(topans)
      for field in qfields:
        sfield = field[9:]
        if sfield == 'tags':
          out[field] = ';'.join(question[sfield])
        else:
          out[field] = question[sfield] if sfield in question else ''
      for field in afields:
        sfield = field[7:]
        out[field] = topans[sfield] if sfield in topans else ''
      csvout.writerow(out)

      

translateusers('data/alltop100x100/users.json','data/alltop100x100/users.csv')
translateanswers('data/alltop100x100/')

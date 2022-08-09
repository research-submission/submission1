import json
import csv


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

def askedquestion(ansid, question):
  if 'user_id' not in question['owner']:
    return False
  return ansid == question['owner']['user_id']


def translateanswers(datadir):
  qlist = open(datadir+'questions.json','r')

  qfields =  ['question_title','question_body','question_link','question_creation_date','question_last_edit_date','question_last_activity_date','question_answer_count','question_score','question_up_vote_count','question_down_vote_count','question_reopen_vote_count','question_delete_vote_count','question_comment_count','question_tags']
  afields =  ['answer_body','answer_link','answer_content_license','answer_creation_date','answer_last_edit_date','answer_last_activity_date','answer_score','answer_is_accepted','answer_up_vote_count','answer_down_vote_count','answer_comment_count','answer_tags']
  sfields = ['answer_is_first_answer','answer_is_last_answer','answer_timediff','answer_won_bounty','answer_own_question']
  fields = ['answer_id','question_id','user_id'] + qfields + afields + sfields
  csvout = csv.DictWriter(open(datadir+'answers.csv', 'w'), fieldnames=fields)
  noans = csv.DictWriter(open(datadir+'unanswered.csv', 'w'), fieldnames=qfields)
  noans.writeheader()
  csvout.writeheader()

  for line in qlist:
    question = json.loads(line)
    if question['answer_count'] == 0:
      out = {}
      for field in qfields:
        sfield = field[9:]
        if sfield == 'tags':
          out[field] = ';'.join(question[sfield])
        else:
          out[field] = question[sfield] if sfield in question else ''
      noans.writerow(out)
    else:
      for ans in question['answers']:
        out = {}
        out['question_id']  = ans['question_id']
        out['answer_id']    = ans['answer_id']
        if 'user_id' not in ans['owner']:
          out['user_id']    = -1
        else:
          out['user_id']      = ans['owner']['user_id']
        out['answer_is_first_answer'],out['answer_is_last_answer'],out['answer_timediff'] = timestats(ans, question)
        out['answer_own_question'] = askedquestion(out['user_id'],question)
        out['answer_won_bounty'] = wonbounty(ans)
        for field in qfields:
          sfield = field[9:]
          if sfield == 'tags':
            out[field] = ';'.join(question[sfield])
          else:
            out[field] = question[sfield] if sfield in question else ''
        for field in afields:
          sfield = field[7:]
          if sfield == 'tags':
            out[field] = ''
          else:
            out[field] = ans[sfield] if sfield in ans else ''
        csvout.writerow(out)

translateanswers('data/all/')

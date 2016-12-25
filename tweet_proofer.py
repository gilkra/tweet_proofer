import sys
import json
import requests
import urllib2
from enchant.checker import SpellChecker
from enchant.tokenize import EmailFilter, URLFilter
from urllib2 import Request, urlopen, URLError

message = raw_input("Please paste the tweet you'd like to send: ")
image? = (raw_input("Do you have an image you'd like to check? (y/n)")).lower()



#looks for tricky legal terms or combo of terms
def legal_flag(message, wordlist):
	message = message.lower()
	all_good = True
	safety_terms = ['best available', 'industry leading', 'gold standard', 'safest', 'best-in-class']
	legal_flag_terms = ["Uber driver", "Uber courier", "Courier" ,
"Uber car" , "Uber vehicle","hire", "Hired", "application", "finish signing up", 
"complete your application", "easy application process","Finish your application", "Job",
"career", "work", "entry-level", "Benefits", "Shift", "Supply", "Part-time", "Full-time", "Drive for Uber", 
"Discipline", "fired", "Warning", "Punish", "Penalty box", "Wage", "Salary", "Commission", "Bonus",
"your background check is approved", "We need your social security number", "We need you on the road",
"Uber customer", "Uber client", "Surge", 'cheapest', 'safest', 'most affordable', 'most dependable'] 

	legal_flag_terms_fixed = [x.lower() for x in legal_flag_terms]
	for term in legal_flag_terms_fixed:
		if term in message:
			all_good = False
			print '- The term/phrase "'+term+'" may not be permitted based on the legal guidelines' 

	if ('guarantee' in message or 'guarantees' in message) and ('rewards' in message or 'reward' in message):
		print "- You mentioned both 'guarantee' and 'reward' in your message. Are you sure the message is clear to the driver?"

	for phrase in safety_terms:
		if phrase in message and ('background check' in message or 'safety' in message):
			all_good = False
			print "- You mentioned '"+phrase+"' in a message about safety/background checks. This may not be permitted based on the legal guidelines"

	for word in wordlist:
		if word in ['guarantee','guarantees','rewards','reward', 'earnings boost'] and 't.uber' not in message:
			all_good = False
			print '- Did you include a link to the terms of the guarantee? Terms should be linked with every guarantee'
	

	return all_good


#tests that t.uber.com url is set to public
def url_set_to_public(url):
	all_good = True
	response = requests.get(url)
	if 'uber.onelogin' in response.url:
		print '- Check your t.uber URL. Did you set it to "Public"?'
		all_good = False
	return all_good

#takes url and tests if valid
def is_valid_url(url):
	req = Request(url)
	try:
	    response = urlopen(req)
	except URLError, e:
		return False
	else:
		return True


#spellcheck
def spellcheck(message):
	all_good = True
	wordlist = message.split()
	fixed_wordlist = []
	for word_index in range(1,len(wordlist)):

		if (wordlist[word_index][0].isupper() and 
			(wordlist[word_index-1][-1] == '.' or
			 wordlist[word_index-1][-1] == ':' or
			wordlist[word_index-1][-1] == '!')) or wordlist[word_index][0].islower():
							
			fixed_wordlist.append(wordlist[word_index])
	
	fixed_wordlist = [x for x in fixed_wordlist if '.co' not in x]
	new_message = ' '.join(fixed_wordlist)

	d = SpellChecker("en_US", filters=[EmailFilter, URLFilter])
	d.set_text(new_message)
	for error in d:
		all_good = False
		print '- Spell check: ', error.word

	return all_good

URL_TEMPLATE = 'https://www.twitter.com/users/username_available?suggest=1&username=%s&full_name=&email=&suggest_on_username=true&context=front&custom=1'
def check_username(screen_name):
    url = URL_TEMPLATE % screen_name
    req = urllib2.Request(url)

    """
        Response will be in the form
        {"desc":"Available!","reason":"available","msg":"Available!","valid":true,"suggestions":[]}
        {"suggestions":[],"desc":"That username has been taken. Please choose another.","reason":"taken","msg":"Username has already been taken","valid":false}
    """
    try:
        json_res = urllib2.urlopen(req).read()
        resp = json.loads(json_res)
        return resp["reason"]
    except urllib2.HTTPError, e:
        return "error: %s" % (e.code,)

def check_image_size(url):
	all_good = True
	file = cStringIO.StringIO(urllib.urlopen(url).read())
    im=Image.open(file)
    # width, height = im.size
    if im.size != (1024, 512):
    	all_good = False
    	print '- Your image is not 1024 x 512. Is it worth resizing?'
    return all_good

#master tester function
def split_them(message):
	wordlist = message.split()

	link_counter = 0
	exclam_counter = 0
	all_good = True
	print "Ok, let's have a look here..." 
	print 
	for word_index in range(len(wordlist)-1):
		next_word = wordlist[word_index+1]
		if wordlist[word_index][-1] == '.' and next_word[0].islower():
			all_good = False
			print '- The sentence starting with "'+next_word+'" should probably be capitalized'

	for word in wordlist:
		if '.c' in word.lower() or 't.uber' in word.lower():
			if word == wordlist[-1]: 
				if word[-1] in [',', '.', ';','!']:
					all_good = False
					print "- No need for punctuation after the link"

			link_counter += 1
			if link_counter > 1:
				all_good = False
				print '- You have more than one link! Step up your game'

			if 'http' in word:
				if is_valid_url(word):
					if url_set_to_public(word) == False:
						all_good = False

				else:
					all_good = False
					print "- Something's fishy with that URL"
			else: 
				fixed_url = 'http://'+word
				if is_valid_url(fixed_url):
					if url_set_to_public(fixed_url) == False:
						all_good = False
				if not is_valid_url(fixed_url):
					all_good = False
					print "- Something's fishy with that URL"
					
		if word[-1] is '!' and word[-2] is '!':
			all_good = False
			print "- You're exclaiming super hard right now! Check to make sure you don't have consecutive exclamation marks in your message."
		if '!' in word:
			exclam_counter += 1
			if exclam_counter > 2:
				all_good = False
				print "- You have more than 2 excalamation marks. Try to find other ways to convey excitement."

		if word.lower() in ['bonus', 'commission', 'warning']:
			print '- Legal flag: reconsider your use of the word "'+word+'"'

		if not 't.uber.com' in word and '.com' in word:
			all_good = False
			print "- Looks like you didn't shorten your URL. Does it make sense to make a t.uber.com address?"

		if word[0] == '@':
			if check_username(word[1:]) == 'improper_format':
				all_good = False
				print "- Something's funky with that twitter handle's format"

			if check_username(word[1:]) != 'taken' and check_username(word[1:]) != 'improper_format':
				all_good = False
				print "- The twitter handle "+word+" doesn't seem to exist"

	
	if 'drive for uber' in message.lower() or 'driving for uber' in message.lower():
		all_good = False
	 	print '- Legal flag: Partners drive WITH, not FOR Uber'
	
	if 'work for uber' in message.lower() or 'working for uber' in message.lower():
		all_good = False
		print '- Legal flag: Partners work WITH, not FOR Uber'

	if len(message) > 140:
		all_good = False
		print "- Your message is too long! You're "+str((len(message)-140))+" characters above the 140 character limit."

	if spellcheck(message) == False:
		all_good = False
	if legal_flag(message, wordlist) == False:
		all_good = False

	if image? == 'y':
		img = raw_input('Please paste your image url here: ')
		all_good = check_image_size(img)

	if all_good == True:
		print '*Looks good to me! Go crush it!*'
		print



split_them(message)

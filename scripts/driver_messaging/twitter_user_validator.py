import argparse
import urllib2
import json
import sys

URL_TEMPLATE = 'https://www.twitter.com/users/username_available?suggest=1&username=%s&full_name=&email=&suggest_on_username=true&context=front&custom=1'

def check_name(screen_name):
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

def print_result(screen_name, msg):
    display = "[%s] %s %s\n"
    if "available" in msg:
        sys.stdout.write(display % ("+", screen_name, msg,))
    elif "error" in msg:
        sys.stdout.write(display % ("!", screen_name, msg))
    else:
        sys.stdout.write(display % ("-", screen_name, msg))

print check_name('gilkazasdhadfdnlks')
print check_name('gilkaz')
print check_name('@gilkaz')
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(prog="check-twitter-user")
#     parser.add_argument('username', help="name to check for")
#     args = parser.parse_args()

#     screen_name = args.username

#     msg = check_name(screen_name)
#     print_result(screen_name, msg)

############## all imports and variables  ##############################

# request library imported
import requests

#Base url for api requests
BASE_URL = "https://api.instagram.com/v1/"

# import the access token from the api_access_token file
from access_token import ACCESS_TOKEN

# to get the data in the url use this function urlretrieve
from urllib import urlretrieve

############### all functions definations ##############################

# function get user own details
def my_details():
    url = BASE_URL + "users/self/?access_token=" + ACCESS_TOKEN
    data = requests.get(url)
    data = data.json()
    if data['meta']['code'] == 200:
        print "Your instagram id is : " + data['data']['id']
        print "Your instagram username is : " + data['data']['username']
        print "Your instagram bio is : " + data['data']['bio']
        print "Your instagram posts count is : " + str(data['data']['counts']['media'])
        print "Your instagram follows count is : " + str(data['data']['counts']['follows'])
        print "Your instagram followed_by count is : " + str(data['data']['counts']['followed_by'])
    else:
        print "Sorry something went wrong"
    print "\n"

# function to get another user id bt their name
def getUserId(userName):
    url = BASE_URL + "users/search?q=" + userName + "&access_token=" + ACCESS_TOKEN
    data = requests.get(url)
    data = data.json()
    if data['meta']['code'] == 200:
        # if response is empty
        if len(data['data']):
            return data['data'][0]['id']
        else:
            print "user does not exist"
            return "none"
    else:
        print "Status code other than 200 was recieved"
        return "none"

############### menu ###################################################
def menu(userName):
    user_id = getUserId(userName)
    print user_id
    user_choice = raw_input("Select : \n1> View recent post \n2> Like recent Post \n3> Comment on recent post \n")
    if(user_choice == 1):
        print user_choice
    elif (user_choice == 2):
        print user_choice
    elif (user_choice == 3):
        print user_choice
    else:
        print user_choice


# main program starts here
print "Hello User"
my_details()
userName = raw_input("Enter User Name (of another User) : ")
menu(userName)

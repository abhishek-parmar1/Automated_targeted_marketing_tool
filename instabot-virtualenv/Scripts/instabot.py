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
def myDetails():
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
        print "Sorry something went wrong \nError : Status code other than 200 was recieved"

# function to get recent post id and download it of user itself
def getRecentPost(user_type):
    url = BASE_URL + "users/" + user_type + "/media/recent/?access_token=" + ACCESS_TOKEN
    data = requests.get(url)
    data = data.json()
    if data['meta']['code'] == 200:
        # if response is empty
        if len(data['data']):
            post_id = data['data'][0]['id']
            if data['data'][0]['type'] == "image":
                image_url = data['data'][0]['images']['standard_resolution']['url']
                urlretrieve(image_url, 'postImage.png');
                print "Post image downloaded"
                return post_id
            elif data['data'][0]['type'] == "video":
                video_url = data['data'][0]['videos']['standard_resolution']['url']
                urlretrieve(video_url, 'postVideo.png');
                print "Post video downloaded"
                return post_id
            else:
                print "post is neither image nor video"
                return post_id
        else:
            print "Sorry no post found"
            return "none"
    else:
        print "Sorry something went wrong \nError : Status code other than 200 was recieved"
        return "none"

# function to get recent post of user itself
def myRecentPost():
    return getRecentPost("self")

# function to get other user id by their name
def getOtherUserId(other_user_name):
    url = BASE_URL + "users/search?q=" + other_user_name + "&access_token=" + ACCESS_TOKEN
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
        print "Sorry something went wrong \nError : Status code other than 200 was recieved"
        return "none"

# function to get other user recent post
def getOtherUserPost(other_user_name):
    other_user_id = getOtherUserId(other_user_name)
    return getRecentPost(other_user_id)

############### menu ###################################################
def menu(other_user_name):
    while True:
        user_choice = int(raw_input("Select : \n1> Get other user recent post \n2> Like other user recent Post \n3> Comment on other user recent post \n4> Exit \n:"))
        if user_choice == 1:
            print other_user_name + " recent post id is : " + getOtherUserPost(other_user_name)
        elif user_choice == 2:
            print user_choice
        elif user_choice == 3:
            print user_choice
        elif user_choice == 4:
            break
        else:
            print "Enter valid input"

# main program starts here
print "Hello User"
while True:
    user_choice = int(raw_input("Select : \n1> Display your details \n2> Get your recent post \n3> Use instagram \n4> Exit \n:"))
    if user_choice == 1:
        myDetails()
    elif user_choice == 2:
        print "Your recent post id is : " + myRecentPost()
    elif user_choice == 3:
        other_user_name = raw_input("Enter User Name (of another User) : ")
        menu(other_user_name)
    elif user_choice == 4 :
        break
    else:
        print "Enter valid input"

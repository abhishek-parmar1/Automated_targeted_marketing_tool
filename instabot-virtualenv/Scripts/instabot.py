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
def getRecentPost(user_type,action):
    url = BASE_URL + "users/" + user_type + "/media/recent/?access_token=" + ACCESS_TOKEN
    data = requests.get(url)
    data = data.json()
    if data['meta']['code'] == 200:
        # if response is empty
        if len(data['data']):
            post_id = data['data'][0]['id']
            if data['data'][0]['type'] == "image":
                if action == "Download Post":
                    image_url = data['data'][0]['images']['standard_resolution']['url']
                    urlretrieve(image_url, 'postImage.png');
                    print "Post image downloaded"
            elif data['data'][0]['type'] == "video":
                if action == "Download Post":
                    video_url = data['data'][0]['videos']['standard_resolution']['url']
                    urlretrieve(video_url, 'postVideo.png');
                    print "Post video downloaded"
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
    return getRecentPost("self","Download Post")

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
    if other_user_id != "none":
        return getRecentPost(other_user_id,"Download Post")
    else:
        return "none"

# function to like other user post
def likeOtherUserPost(other_user_name):
    other_user_id = getOtherUserId(other_user_name)
    post_id = getRecentPost(other_user_id,"Like Post")
    if post_id != "none":
        data = {
            'access_token': ACCESS_TOKEN
        }
        url = BASE_URL + "media/" + str(post_id) + "/likes"
        info = requests.post(url, data)
        info = info.json()
        if info['meta']['code'] == 200:
            print other_user_name + " recent post liked"
        else:
            print "Sorry something went wrong \nError : Status code other than 200 was recieved"

# function to get the comments on the other user posts
def getCommentOtherUserPost(other_user_name):
    other_user_id = getOtherUserId(other_user_name)
    post_id = getRecentPost(other_user_id, "Get Comments")
    if post_id != "none":
        url = BASE_URL + "media/" + str(post_id) + "/comments?access_token=" + ACCESS_TOKEN
        info = requests.get(url)
        info = info.json()
        if info['meta']['code'] == 200:
            if len(info['data']):
                print "comments are : "
                for index in  info['data']:
                    print index['from']['username'] + " : " + index['text']
            else:
                print " no comments on the post "
        else:
            print "Sorry something went wrong \nError : Status code other than 200 was recieved"

# function to comment on other user post
def commentOtherUserPost(other_user_name):
    other_user_id = getOtherUserId(other_user_name)
    post_id = getRecentPost(other_user_id, "Comment Post")
    if post_id != "none":
        while True:
            text = raw_input("enter the commment text : ")
            if len(text) and len(text.strip()) :
                break
            else:
                print "Please provide some text in comment"
        data = {
            'access_token': ACCESS_TOKEN,
            'text' : text
        }
        url = BASE_URL + "media/" + str(post_id) + "/comments"
        info = requests.post(url, data)
        info = info.json()
        if info['meta']['code'] == 200:
            print " commented on the recent post of " + other_user_name
        else:
            print "Sorry something went wrong \nError : Status code other than 200 was recieved"

############### menu ###################################################
def menu(other_user_name):
    while True:
        user_choice = int(raw_input("Select : \n1> Get other user recent post \n2> Like other user recent Post \n3> Get Comments on other user recent post \n4> Comment on other user recent post \n5> Exit \n:"))
        if user_choice == 1:
            print other_user_name + " recent post id is : " + getOtherUserPost(other_user_name)
        elif user_choice == 2:
            likeOtherUserPost(other_user_name)
        elif user_choice == 3:
            getCommentOtherUserPost(other_user_name)
        elif user_choice ==4:
            commentOtherUserPost(other_user_name)
        elif user_choice == 5:
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

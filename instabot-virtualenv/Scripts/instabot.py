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
    response = requests.get(url)
    response = response.json()
    if response['meta']['code'] == 200:
        print "Your instagram id is : " + response['data']['id']
        print "Your instagram username is : " + response['data']['username']
        print "Your instagram bio is : " + response['data']['bio']
        print "Your instagram posts count is : " + str(response['data']['counts']['media'])
        print "Your instagram follows count is : " + str(response['data']['counts']['follows'])
        print "Your instagram followed_by count is : " + str(response['data']['counts']['followed_by'])
    else:
        print "Sorry something went wrong \nError : Status code other than 200 was recieved"

# function to get recent post id and download it of user itself
def getRecentPost(user_id,action):
    url = BASE_URL + "users/" + user_id + "/media/recent/?access_token=" + ACCESS_TOKEN
    response = requests.get(url)
    response = response.json()
    if response['meta']['code'] == 200:
        # if response is empty
        if len(response['data']):
            post_id = response['data'][0]['id']
            if response['data'][0]['type'] == "image":
                if action == "Download Post":
                    image_url = response['data'][0]['images']['standard_resolution']['url']
                    urlretrieve(image_url, 'postImage.png');
                    print "Post image downloaded"
                    getPostDetails(user_id, post_id)
            elif response['data'][0]['type'] == "video":
                if action == "Download Post":
                    video_url = response['data'][0]['videos']['standard_resolution']['url']
                    urlretrieve(video_url, 'postVideo.png');
                    print "Post video downloaded"
                    getPostDetails(user_id, post_id)
            else:
                print "post is neither image nor video"
            return post_id
        else:
            print "Sorry no post found"
            return "none"
    else:
        print "Sorry something went wrong \nError : Status code other than 200 was recieved"
        return "none"

# function to get a user post details
def getPostDetails(user_id, post_id):
    url = BASE_URL + "media/" + post_id + "?access_token=" + ACCESS_TOKEN
    response = requests.get(url)
    response = response.json()
    if response['meta']['code'] == 200:
        print "count of likes on the post is " + str(response['data']['likes']['count'])
        getLikeUserPost(user_id, post_id)
        print "count of comments on the post is " + str(response['data']['comments']['count'])
        getCommentUserPost(user_id, post_id)
    else:
        print "Sorry something went wrong \nError : Status code other than 200 was recieved"


# function to get recent post of user itself
def myRecentPost():
    return  getRecentPost("self","Download Post")

# function to get other user id by their name
def getUserId(user_name):
    url = BASE_URL + "users/search?q=" + user_name + "&access_token=" + ACCESS_TOKEN
    response = requests.get(url)
    response = response.json()
    if response['meta']['code'] == 200:
        # if response is empty
        if len(response['data']):
            return response['data'][0]['id']
        else:
            print "user does not exist"
            return "none"
    else:
        print "Sorry something went wrong \nError : Status code other than 200 was recieved"
        return "none"

# function to get other user recent post
def getOtherUserPost(user_name):
    user_id = getUserId(user_name)
    if user_id != "none":
        return getRecentPost(user_id,"Download Post")
    else:
        return "none"

# function to get the likes on the other user posts
def getLikeUserPost(user_id, post_id):
    if user_id != "self":
        post_id = getRecentPost(user_id, "Get Likes")
    if post_id != "none":
        url = BASE_URL + "media/" + str(post_id) + "/likes?access_token=" + ACCESS_TOKEN
        response = requests.get(url)
        response = response.json()
        if response['meta']['code'] == 200:
            if len(response['data']):
                print "recently liked by : "
                for index in response['data']:
                    print index['username']
            else:
                print "no recent likes on the post "
        else:
            print "Sorry something went wrong \nError : Status code other than 200 was recieved"

# function to like other user post
def likeUserPost(user_name):
    user_id = getUserId(user_name)
    post_id = getRecentPost(user_id,"Like Post")
    if post_id != "none":
        data = {
            'access_token': ACCESS_TOKEN
        }
        url = BASE_URL + "media/" + str(post_id) + "/likes"
        info = requests.post(url, data)
        info = info.json()
        if info['meta']['code'] == 200:
            print user_name + " recent post liked"
        else:
            print "Sorry something went wrong \nError : Status code other than 200 was recieved"

# function to get the comments on the other user posts
def getCommentUserPost(user_id, post_id):
    if user_id != "self":
        post_id = getRecentPost(user_id, "Get Comments")
    if post_id != "none":
        url = BASE_URL + "media/" + str(post_id) + "/comments?access_token=" + ACCESS_TOKEN
        response = requests.get(url)
        response = response.json()
        if response['meta']['code'] == 200:
            if len(response['data']):
                print "recent comments are : "
                for index in  response['data']:
                    print index['from']['username'] + " : " + index['text']
            else:
                print "no recent comments on the post "
        else:
            print "Sorry something went wrong \nError : Status code other than 200 was recieved"

# function to comment on other user post
def commentUserPost(user_name):
    user_id = getUserId(user_name)
    post_id = getRecentPost(user_id, "Comment Post")
    if post_id != "none":
        print "The total length of the comment cannot exceed 300 characters"
        print "The comment cannot contain more than 4 hashtags"
        print "The comment cannot contain more than 1 URL"
        print "The comment cannot consist of all capital letters"
        while True:
            text = raw_input("enter the commment text : ")
            if len(text) and len(text.strip()) and len(text)<=300 :
                break
            else:
                print "Please provide some text in comment less than 300 characters"
        data = {
            'access_token': ACCESS_TOKEN,
            'text' : text
        }
        url = BASE_URL + "media/" + str(post_id) + "/comments"
        info = requests.post(url, data)
        info = info.json()
        if info['meta']['code'] == 200:
            print "commented on the recent post of " + user_name
        else:
            print "Sorry something went wrong, \neither you have violated any of the above rule or Status code other than 200 was recieved"

# function to get recent liked post by the user itself
def getRecentLikedPost():
    url = BASE_URL + "users/self/media/liked?access_token=" + ACCESS_TOKEN
    response = requests.get(url)
    response = response.json()
    if response['meta']['code'] == 200:
        if len(response['data']):
            post_id = response['data'][0]['id']
            if response['data'][0]['type'] == "image":
                image_url = response['data'][0]['images']['standard_resolution']['url']
                urlretrieve(image_url, 'postImage.png');
                print "Post image downloaded"
                getPostDetails("self", post_id)
            elif response['data'][0]['type'] == "video":
                video_url = response['data'][0]['videos']['standard_resolution']['url']
                urlretrieve(video_url, 'postVideo.png');
                print "Post video downloaded"
                getPostDetails("self", post_id)
            else:
                print "recent liked post is neither image nor video"
        else:
            print "there are no posts liked by you"
    else:
        print "Sorry something went wrong \nError : Status code other than 200 was recieved"


############### menu ###################################################
def menu(other_user_name):
    while True:
        user_choice = int(raw_input("Select : \n1> Get other user recent post details \n2> Get likes other user recent post \n3> Like other user recent Post \n4> Get Comments on other user recent post \n5> Comment on other user recent post \n6> Exit \n:"))
        if user_choice == 1:
            print other_user_name + " recent post id is : " + getOtherUserPost(other_user_name)
        elif user_choice == 2:
            user_id = getUserId(other_user_name)
            getLikeUserPost(user_id, "anything")
        elif user_choice == 3:
            likeUserPost(other_user_name)
        elif user_choice == 4:
            user_id = getUserId(other_user_name)
            getCommentUserPost(user_id, "anything")
        elif user_choice == 5:
            commentUserPost(other_user_name)
        elif user_choice == 6:
            break
        else:
            print "Enter valid input"

# main program starts here
print "Hello User"
while True:
    user_choice = int(raw_input("Select : \n1> Display your details \n2> Get your recent post details \n3> Get recent post liked by you \n4> Search other user \n5> Exit \n:"))
    if user_choice == 1:
        myDetails()
    elif user_choice == 2:
        print "Your recent post id is : " + myRecentPost()
    elif user_choice == 3:
        getRecentLikedPost()
    elif user_choice == 4:
        other_user_name = raw_input("Enter User Name (of another User) : ")
        menu(other_user_name)
    elif user_choice == 5 :
        break
    else:
        print "Enter valid input"

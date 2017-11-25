from django.shortcuts import render
import json, requests, random, re
from pprint import pprint

from django.views import generic
from django.http.response import HttpResponse
#from rest_framework import status


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Transcript, AudioChunk, Audio, User

PAGE_ACCESS_TOKEN = "EAACOkErSag4BAAwIrNxCfF7loXyiZAKDfRbflZC6Pt2AqZAwSTtxIq7c5z03gA1qeFQJYcTsopA4PfqiCaDQZAcl1lZByS1HDH8cnBSZA1XSyJda9ZCcuYyXLBlIufTZBlz2ZC5qktm6JNVZC2bcuvZALY5rreKeHSwfst7ZCCJsptA5AAZDZD"
VERIFY_TOKEN = "2318934571"

jokes = { 'stupid': ["""Yo' Mama is so stupid, she needs a recipe to make ice cubes.""", 
                     """Yo' Mama is so stupid, she thinks DNA is the National Dyslexics Association."""], 
         'fat':      ["""Yo' Mama is so fat, when she goes to a restaurant, instead of a menu, she gets an estimate.""", 
                      """ Yo' Mama is so fat, when the cops see her on a street corner, they yell, "Hey you guys, break it up!" """], 
         'dumb': ["""Yo' Mama is so dumb, when God was giving out brains, she thought they were milkshakes and asked for extra thick.""", 
                  """Yo' Mama is so dumb, she locked her keys inside her motorcycle."""] }


audios = AudioChunk.objects.all()[:2]

audio = random.choice(audios)
waiting_transl = False

# Helper function
def saveTrasncript(sender_psid,text,audio_chunk):
    # Save in db
    transcript = Transcript()
    #audio_chunk = audio_chunk
    audio_chunk.transcript_set.create(
        user = User.objects.get(id=sender_psid),
        text = text
        )
def saveUserDetails(psid, user_details):
    #save userdetails
    user = User.objects.create(
        id = psid,
        first_name =  user_details['first_name'],
        last_name =  user_details['last_name'],
        profile_pic = user_details['profile_pic'],
        locale =  user_details['locale'],
        timezone = user_details['timezone'],
        gender = user_details['gender'])


def post_facebook_message(fbid, recevied_message):
    # Remove all punctuations, lower case the text and split it based on space
    tokens = re.sub(r"[^a-zA-Z0-9\s]",' ',recevied_message).lower().split()
    joke_text = ''
    for token in tokens:
        if token in jokes:
            joke_text = random.choice(jokes[token])
            break
    if not joke_text:
        joke_text = "I didn't understand! Send 'stupid', 'fat', 'dumb' for a Yo Mama joke!" 
    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid 
    user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN} 
    user_details = requests.get(user_details_url, user_details_params).json() 
    joke_text = 'Yo '+user_details['first_name']+'..! ' + joke_text
                   
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps({
        "recipient":{"id":fbid}, 
        "message":{"text":joke_text}
        })
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())

def callSendAPI(fbid, response):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps({
        "recipient":{"id":fbid}, 
        "message":response
        })    
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())

def handlePostback(sender_psid,received_postback):
    pass

def getUserDetails(fbid):
    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid 
    user_details_params = {
        'fields':'first_name,last_name,profile_pic,locale,timezone,gender', 
        'access_token':PAGE_ACCESS_TOKEN} 
    user_details = requests.get(user_details_url, user_details_params).json()
    return user_details

def buildResponse(content,type='text'):
    # build facebook m response
    if type == 'text':
        response = {"text":content}
    elif type == 'image' or type == 'audio':
        response = {"attachment":
                {"type":type,
                "payload":{"url":content,
                "is_reusable":True}
                }}
    return response


def handleMessage(sender_psid,recevied_message):
    
    #checks if the user is in the db
    if not (User.objects.filter(id=sender_psid)):
        saveUserDetails(sender_psid,getUserDetails(sender_psid))

    #Checks if the incoming message contains text
    global waiting_transl, audio

    if 'text' in recevied_message:
        #do some staff
        if waiting_transl:
            callSendAPI(sender_psid,{"text":'"Next" for other audio'})
            saveTrasncript(sender_psid,recevied_message["text"],audio)
            print('Translation received')
            waiting_transl = False

        elif recevied_message['text']=='Luke' or recevied_message['text']=='Next' :
            audio = random.choice(audios)
            callSendAPI(
                sender_psid,
                buildResponse(audio.url_link,"audio"))
            waiting_transl = True
            print('Waiting for translation')
        else:
            post_facebook_message(sender_psid, recevied_message['text'])
    if 'attachments' in recevied_message:
        attachment_type = recevied_message['attachments'][0]['type']
        
        #Gets the attachment's url
        attachment_url = recevied_message['attachments'][0]['payload']['url']
        print(attachment_url)
        #do something with atach
        if  attachment_type == 'image':
            #Process image
            callSendAPI(
                sender_psid,
                buildResponse("https://azure.microsoft.com/svghandler/bot-service/?width=600&height=315","image")
                )
            callSendAPI(sender_psid,{"text":"What do you think"})
        elif attachment_type == 'audio':
            #Process de audio
            callSendAPI(sender_psid,buildResponse("https://instaud.io/_/1s3c.mp3","audio"))
            pass 
        else:
            callSendAPI(sender_psid,{"text":"No Idea"})
        #post_facebook_message(sender_psid,'fat')

        pass
    pass


# Create your views here.
class DimitriB11View(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
    # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                if 'message' in message:
                    # Print the message to the terminal
                    pprint(message)    
                    # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
                    # are sent as attachments and must be handled accordingly. 
                    handleMessage(message['sender']['id'],message['message'])

        return HttpResponse()
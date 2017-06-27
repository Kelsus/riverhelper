from __future__ import print_function
import urllib.request
import re
import json


def get_river_section_flow_from_api(river_section_id):

    river_flow_request = urllib.request.urlopen('http://waterservices.usgs.gov/nwis/iv/?format=json&sites=' + river_section_id + '&parameterCd=00060&siteStatus=all')
    river_flow_data = river_flow_request.read()
    encoding = river_flow_request.info().get_content_charset('utf-8')
    river_json = json.loads(river_flow_data.decode(encoding))
    print("HI JC!!! here's river flow json", json.dumps(river_json))

    river_flow = river_json['value']['timeSeries'][0]['values'][0]['value'][0]['value']

    return river_flow


def create_river_section_attributes(river_section):
    return({"river_section":river_section})

def getRiverFlow(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = True

    if 'location' in intent['slots']:
        river_section = intent['slots']['location']['value']
        river_section_id = intent['slots']['location']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']


        river_section_flow = get_river_section_flow_from_api(river_section_id)

        session_attributes = create_river_section_attributes(river_section)
        speech_output = "The current flow on the " + \
                        river_section + \
                        " is " + \
                        river_section_flow + \
                        " cfs."
        reprompt_text = "You can ask for the current conditions at a USGS river station by saying 'what are the flows' and then saying the full name of a USGS station"
    else:
        speech_output = "I'm wasn't able to figure out what river section you wanted flows for. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your river section you wanted flows for. " \
                        "You can tell me what river section you want flow for by saying for example, " \
                        "'what is the current flow on the Colorado River below Glenwood Springs'.'"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))




# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "Glenwood Wave " + title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to river bot. " \
                    "You can get current river conditions by asking for the flows at a USGS river station. For example say,  'what is the current flow for the Colorado River Below Glenwood Springs.'"
    reprompt_text = "Ask for the flow at a USGS river station.  For example, 'what is the flow on the Colorado River Below Glenwood Springs.'"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))



# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "flow":
        return getRiverFlow(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        getGlenwoodWaveFlow()


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    if (event['session']['application']['applicationId'] != "amzn1.ask.skill.986f7243-1759-4bbf-a408-35d3a6d6da21"):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

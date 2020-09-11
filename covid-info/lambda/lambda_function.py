# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils
import requests
import json

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name, get_dialog_state, get_slot_value
from ask_sdk_model import Response, DialogState

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome, Lets start with Knowing about COVID. You can ask for national or state covid 19 data. May I know Your Name, Locatioon and Temparature Before Starting.."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class NationalCasesIntentHandler(AbstractRequestHandler):
    """Handler for National Cases Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("NationalCasesIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        url = "https://api.covid19india.org/data.json";
        response = requests.get(url)
        if response.status_code == 200:
            parsed_json = json.loads(response.text)
            speak_output = "{} new cases have been reported so far. There are {} confirmed cases in India, out of which {} are active. There have been {} recoveries and {} deaths.".format(
                parsed_json["statewise"][0]["deltaconfirmed"], parsed_json["statewise"][0]["confirmed"], parsed_json["statewise"][0]["active"], parsed_json["statewise"][0]["recovered"], parsed_json["statewise"][0]["deaths"])
        else:
            speak_output = "Sorry, covid 19 India API is down"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class StateCasesIntentHandler(AbstractRequestHandler):
    """Handler for State Cases Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("StateCasesIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        url = "https://api.covid19india.org/data.json"
        response = requests.get(url)
        if response.status_code == 200:
            parsed_json = json.loads(response.text)
            if slots["state"].value.lower() == "india":
                toCheck = "total"
            else:
                toCheck = slots["state"].value.lower()
            index = -1
            for i in range(len(parsed_json["statewise"])):
                if parsed_json["statewise"][i]["state"].lower() == toCheck:
                    index = i
                    break
            if index == -1:
                speak_output = "Sorry, please try another state"
            elif parsed_json["statewise"][index]["confirmed"] == "0":
                speak_output = "There are no cases in {}".format(parsed_json["statewise"][index]["state"])
            else:
                speak_output = "{} new cases have been reported so far. There are {} confirmed cases in {}, out of which {} are active. There have been {} recoveries and {} deaths.".format(
                    parsed_json["statewise"][index]["deltaconfirmed"], parsed_json["statewise"][index]["confirmed"], parsed_json["statewise"][index]["state"], parsed_json["statewise"][index]["active"], parsed_json["statewise"][index]["recovered"], parsed_json["statewise"][index]["deaths"])
        else:
            speak_output = "Sorry, covid 19 India API is down"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello World! Any time If you need me to Show My Presence !!" 

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class addDetails(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("addDetails")(handler_input)
    
    def handle(self, handler_input):
        #slots = handler_input.request_envelope.request.intent.slots
        #person_name_value=slots["name"].value
        #emparature_value=slots["temp"].value
        #person_location_value=slots["location"].value
        
        person_name_value = get_slot_value(handler_input=handler_input, slot_name="name")
        person_location_value = get_slot_value(handler_input=handler_input, slot_name="location")
        temparature_value = get_slot_value(handler_input=handler_input, slot_name="tmp")
        
        url = "https://2wlghkobg9.execute-api.us-east-1.amazonaws.com/personDetails?personName="+str(person_name_value)+"&personLocation="+str(person_location_value)+"&Temparature="+str(temparature_value)
        response = requests.get(url)
        speak_output=" Your Details are Registered {}, I hope It's wounderfull Growing up at {}, Must be very fascinating to you. Okay, Having {} Temparature You dont need to worry! I Wish I could help you more, Please check @https://covidindia.org/ For more information and guidelines about COVID-19".format(person_name_value, person_location_value, temparature_value)
        
        return(
            handler_input.response_builder
            .speak(speak_output)
            .response
        )

class QuestionAlexaHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("questionAlexa")(handler_input)
    
    def handle(self, handler_input):
        speak_output=" Here I am designed to have a healthy conversation regarding COVID 19 and To guide you through. Any further question you can Feel free to ask"
        
        return(
            handler_input.response_builder
            .speak(speak_output)
            .response
            )

class MildConditionHandler(AbstractRequestHandler):
    """Handler for Skill Mild Condition."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        
        return ask_utils.is_intent_name("mildCondition")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output="Hey! I guess you have nothing to worry much, Anyway, Please maintain social distance and stick to precautions. There are mild chances that you can get infected by Carona Virus "
        
        return(
            handler_input.response_builder
            .speak(speak_output)
            .response
            )

class SevereConditionHandler(AbstractRequestHandler):
    """Handler for Skill severe Condition."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        
        return ask_utils.is_intent_name("severeCondition")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output="Hey There ! It seems you have to be very carefull, for the sake of you and others too. Please Try to make a COVID Test asap. Take effective care and Consultation. You may be having severe Condition with respect to Carona Virus"
        
        return(
            handler_input.response_builder
            .speak(speak_output)
            .response
            )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can ask for state or national data! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(NationalCasesIntentHandler())
sb.add_request_handler(StateCasesIntentHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(addDetails())
sb.add_request_handler(QuestionAlexaHandler())
sb.add_request_handler(MildConditionHandler())
sb.add_request_handler(SevereConditionHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
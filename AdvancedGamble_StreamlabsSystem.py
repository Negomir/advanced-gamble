import os
import sys
import json
import imp

## Consts

ROOT_DIR = os.path.dirname(__file__)
SETTINGS_DIR = os.path.join(ROOT_DIR, "settings")
CONFIG_FILE = os.path.join(ROOT_DIR, "config.json")
OUTCOMES_DIR = os.path.join(ROOT_DIR, "outcomes")
OUTCOMES_FILE = os.path.join(OUTCOMES_DIR, "outcomes.json")

## Chat Info

ScriptName = "Advanced Gamble"
Website = "https://github.com/Negomir/advanced-gamble"
Description = "This is an extention of the gamble script, offering more options and customization to the streamer"
Creator = "Negomir99"
Version = "1.0.0.0"

## Setup

def ImportModules():
    global settings, outcomes_manager
    
    # Settings
    settings_module = imp.load_source("module.settings", os.path.join(SETTINGS_DIR, "settings.py"))
    settings = settings_module.Settings(CONFIG_FILE)
    
    # Outcomes
    outcomes_module = imp.load_source("module.outcomes", os.path.join(OUTCOMES_DIR, "outcomes.py"))
    outcomes_manager = outcomes_module.OutcomesManager(OUTCOMES_FILE)

## Global Vars

settings = None
outcomes_manager = None

## My Functions

def DoGamble(data):
    global settings, outcomes_manager
    
    if data.User == "negomir99" or data.User == settings.streamer or Parent.HasPermission(data.User, settings.command_permission, ""):
        amount = ParseAmount(data)
        if amount is None:
            Parent.Log(ScriptName, "error parsing gamble amount. roll: " + str(amount))
            return
        
        val = Parent.GetRandom(0, 100)
        outcome = outcomes_manager.GetOutcome(val)
        if outcome is None:
            Parent.Log(ScriptName, "error, outcome is None")
            return
        
        ApplyOutcome(data, amount, outcome)
        SendResponse(data, amount, value, outcome.message)
    else:
        output_message = settings.unauthorized_message
        
        output_message = output_message.replace("$username", data.UserName)
        output_message = output_message.replace("$user", data.User)
        
        Parent.SendStreamMessage(output_message)
    
    return

def ParseAmount(data):
    try:
        amount = 0
        param = data.GetParam(1).lower()
        
        if "-" in param:
            Parent.Log(ScriptName, "error, negative")
            return None
        
        if param == "all":
            amount = Parent.GetPoints(data.User)
        elif "%" in param:
            perc = float(param.split('%')[0]) / 100
            amount = int(Parent.GetPoints(data.User) * perc)
        else:
            amount = int(param)
            
        return amount
    except:
        return None

def ApplyOutcome(data, amount, outcome):
    value = outcome.value + amount * outcome.multiplier
    Parent.AddPoints(data.User, data.UserName, value)
    
def SendResponse(data, amount, value, message):
    global settings
    
    output_message = message
    if message == "":
        Parent.Log(ScriptName, "error, empty outcome message")
        return
    
    output_message = output_message.replace("$user", data.User)
    output_message = output_message.replace("$username", data.UserName)
    output_message = output_message.replace("$amount", str(amount))
    output_message = output_message.replace("$result", str(value))
    output_message = output_message.replace("$points", str(Parent.GetPoints(data.User)))
    output_message = output_message.replace("$currency", Parent.GetCurrencyName)
    output_message = output_message.replace("$pointswithcurrency", PointsWithCurrency(data))
    
    Parent.SendStreamMessage(output_message)
    
    return

def PointsWithCurrency(data):
    points = Parent.GetPoints(data.User)
    currency = Parent.GetCurrencyName()
    
    return str(points) + " " + currency
    
## Core Functions

#Init is a function called when the script is first loaded
def Init():
    global settings, outcomes_manager
    
    ImportModules()
    return

#Exec is a function called every time the bot gets a chat message
#In exec we are going to check if the message format matches any of our commands
#and handle them. If it is not a command, or it's not part of the script, it
#will just be ignored
def Execute(data):
    global settings
    if not settings.only_live or Parent.IsLive():
        if data.IsChatMessage() and data.GetParam(0).lower() == settings.gamble_command:
            DoGamble(data)
        #elif data.IsChatMessage() and data.GetParam(0).lower() == settings.jackpot_command:
        #    Parent.SendStreamMessage(str(settings.jackpot.amount))
    return

#Tick is called once every millisecond
def Tick():
    return

#ReloadSettings is called every time the 'Save Settings' button is clicked in
#in the bot in the script's UI
def ReloadSettings(jsonData):
    return

#Unload is called when the script gets unloaded.
#It is used for cleanup when the bot closes
def Unload():
    return

#ScriptToggled is called when the enabled state is changed in the bot UI by
#checking or unchecking the script's checkbox
def ScriptToggled(state):
    return
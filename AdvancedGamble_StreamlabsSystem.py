import os
import sys
import json

ScriptName = "Advanced Gamble"
Website = "http://www/github.com/negomir99/streamlabs/advanced-gamble"
Description = "This is an extention of the gamble script, offering more options and customization to the streamer"
Creator = "Negomir"
Version = "1.0.0.0"

#Init is a function called when the script is first loaded
def Init():
    return

#Exec is a function called every time the bot gets a chat message
#In exec we are going to check if the message format matches any of our commands
#and handle them. If it is not a command, or it's not part of the script, it
#will just be ignored
def Exec(data):
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

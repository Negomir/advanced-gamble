import os
import sys
import json

## Settings

settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")

class Settings:
    def __init__(self):
        if settingsFile and os.path.isfile(settingsFile):
            with codecs.open(settingsFile, encoding="utf-8-sig", mode="r") as f:
                self.__dict__ = json.load(f, encoding="utf-8-sig")
        else:
            #Global
            self.streamer = "negomir99"
            self.command = "!gamble"
            self.only_live = False
            #Cooldown
            self.command_permission = "Everyone"
            self.is_global_cooldown_on = False
            self.global_cooldown = 0
            self.is_user_cooldown_enabled = False
            self.user_cooldown = 0
            #Outputs
            self.win_jackpot_message = "$username rolled 100 and WON THE JACKPOT!! They now have $pointswithcurrency"
            self.win_message = "$username gambled $amount and rolled a $roll and won! They now have $pointswithcurrency"
            self.lose_message = "$username gambled $amount and rolled a $roll and lost! They now have $pointswithcurrencyname"
            self.not_enough_points = "$username you cannot gamble the points you don't have!"
            
## Chat Info

ScriptName = "Advanced Gamble"
Website = "https://github.com/Negomir/advanced-gamble"
Description = "This is an extention of the gamble script, offering more options and customization to the streamer"
Creator = "Negomir"
Version = "1.0.0.0"

## Global Vars

settings = None

## My Functions

def DoGamble(Parent, data):
    global settings
    if (data.User == "negomir99" or data.User == settings.streamer) and Parent.HasPersmission(data.User, settings.command_permission, ""):
        Parent.SendTwitchMessage("gamble")
    else:
        Parent.SendTwitchMessage("not allowed")
        
    return

## Core Functions

#Init is a function called when the script is first loaded
def Init():
    global settings
    settings = Settings()
    return

#Exec is a function called every time the bot gets a chat message
#In exec we are going to check if the message format matches any of our commands
#and handle them. If it is not a command, or it's not part of the script, it
#will just be ignored
def Execute(data):
    global settings
    if not settings.only_live or Parent.IsLive():
        if data.IsChatMessage() and data.GetParam(0).lower() == settings.command:
            if (data.User == "negomir99" or data.User == settings.streamer) and Parent.HasPersmission(data.User, settings.command_permission, ""):
                Parent.SendTwitchMessage("gamble")
            else:
                Parent.SendTwitchMessage("not allowed")
        
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
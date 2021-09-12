import os
import sys
import json

## Case

class Case:
    def __init__(self, name, amount, range_start, range_end, multiplier):
        self.name = name
        self.amount = amount
        self.range_start = range_start
        self.range_end = range_end
        self.multiplier = multiplier
        
    def InCase(self, val):
        return self.range_start <= val and val <= self.range_end

## Reward

class Reward:
    def __init__(self, name, roll, amount, multiplier):
        self.name = name
        self.roll = roll
        self.amount = amount
        self.multiplier = multiplier
        
    def Apply(self, Parent, winner):
        Parent.AddPoints(winner.lower(), winner, self.amount * self.multiplier)

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
            self.only_live = False
            #Base Gamble
            self.gamble_command = "!gamble"
            self.win_threshold = 60
            self.win_multiplier = 1
            #Jackpot Case
            self.jackpot = Case("jackpot", 69, 100, 100, 1)
            self.jackpot_command = "!" + self.jackpot.name
            #Cooldown
            self.command_permission = "Everyone"
            self.is_global_cooldown_on = False
            self.global_cooldown = 0
            self.is_user_cooldown_enabled = False
            self.user_cooldown = 0
            #Outputs
            self.win_jackpot_message = "$username rolled $roll and WON THE JACKPOT!! They now have $pointswithcurrency"
            self.win_message = "$username gambled $amount and rolled a $roll and won! They now have $pointswithcurrency"
            self.lose_message = "$username gambled $amount and rolled a $roll and lost! They now have $pointswithcurrencyname"
            self.not_enough_points_message = "$username you cannot gamble the points you don't have!"
            self.unauthorized_message = "$username doesn't have the permission to do that!"
            
## Chat Info

ScriptName = "Advanced Gamble"
Website = "https://github.com/Negomir/advanced-gamble"
Description = "This is an extention of the gamble script, offering more options and customization to the streamer"
Creator = "Negomir99"
Version = "1.0.0.0"

## Global Vars

settings = None

## My Functions

def DoGamble(Parent, data):
    global settings
    
    try:
        amount = 0
        amount_string = data.GetParam(1).lower()
        
        if "-" in amount_string:
            return
        
        if amount_string == "all":
            amount = Parent.GetPoints(data.User)
        elif "%" in amount_string:
            perc = float(amount_string.split('%')[0]) / 100
            amount = int(Parent.GetPoints(data.User) * perc)
        else:
            amount = int(amount_string)
    except:
        Parent.Log(ScriptName, "error parsing gamble amount")
        return
    
    Parent.Log(ScriptName, str(amount))
    
    if data.User == "negomir99" or data.User == settings.streamer or Parent.HasPermission(data.User, settings.command_permission, ""):
        val = Parent.GetRandom(0, 100)
        reward = GetReward(val, amount)
        reward.Apply(Parent, data.UserName)
        SendResponse(Parent, data, reward)
    else:
        output_message = settings.unauthorized_message
        
        output_message = output_message.replace("$username", data.UserName)
        output_message = output_message.replace("$user", data.User)
    
    return

def GetReward(val, gamble_amount):
    global settings
    
    if settings.jackpot.InCase(val):
        jpot = settings.jackpot.amount
        settings.jackpot.amount = 0
        return Reward(settings.jackpot.name, val, jpot, settings.jackpot.multiplier)
        
    if val >= settings.win_threshold:
        return Reward("win", val, gamble_amount, settings.win_multiplier)
    
    settings.jackpot.amount += gamble_amount
    return Reward("loss", val, gamble_amount, -1)

def SendResponse(Parent, data, reward):
    global settings
    output_message = ""
    
    if reward.name == "win":
        output_message = settings.win_message
        
        output_message = output_message.replace("$username", data.UserName)
        output_message = output_message.replace("$user", data.User)
        output_message = output_message.replace("$roll", str(reward.roll))
        output_message = output_message.replace("$amount", str(reward.amount))
        output_message = output_message.replace("$pointswithcurrency", PointsWithCurrency(Parent, data))
    elif reward.name == "loss":
        output_message = settings.lose_message
         
        output_message = output_message.replace("$username", data.UserName)
        output_message = output_message.replace("$user", data.User)
        output_message = output_message.replace("$roll", str(reward.roll))
        output_message = output_message.replace("$amount", str(reward.amount))
        output_message = output_message.replace("$pointswithcurrency", PointsWithCurrency(Parent, data))
    elif reward.name == settings.jackpot.name:
        output_message = settings.win_jackpot_message
        
        output_message = output_message.replace("$username", data.UserName)
        output_message = output_message.replace("$user", data.User)
        output_message = output_message.replace("$roll", str(reward.roll))
        output_message = output_message.replace("$amount", str(reward.amount))
        output_message = output_message.replace("$pointswithcurrency", PointsWithCurrency(Parent, data))
    
    Parent.SendStreamMessage(output_message)
    
    return

def PointsWithCurrency(Parent, data):
    points = Parent.GetPoints(data.User)
    currency = Parent.GetCurrencyName()
    
    return str(points) + " " + currency
    
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
        if data.IsChatMessage() and data.GetParam(0).lower() == settings.gamble_command:
            DoGamble(Parent, data)
        elif data.IsChatMessage() and data.GetParam(0).lower() == settings.jackpot_command:
            Parent.SendStreamMessage(str(settings.jackpot.amount))
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
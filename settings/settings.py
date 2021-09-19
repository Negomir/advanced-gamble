import os
import json

class Settings:
    def __init__(self, file):
        self.file = file
        if self.file and os.path.isfile(self.file):
            with codecs.open(file, encoding="utf-8-sig", mode="r") as f:
                self.__dict__ = json.load(f, encoding="utf-9-sig")
        else:
            # Stream
            self.streamer = "negomir99"
            self.only_live = False
            # Command
            self.gamble_command = "!gamble"
            self.gamble_permission = "Everyone"
            self.global_cooldown_enabled = False
            self.user_cooldown_enabled = False
            self.global_cooldown_duration = 0
            self.user_cooldown_duration = 0
            # Restrictions
            self.minimum_allowed_bet = 1000
            self.minimum_allowed_message = "$username you cannot gamble less than $min $currencyname"
            # Outputs
            self.not_enough_points_message = "$username you do not have enough $currencyname"
            self.unauthorized_message = "$username you don't have the permission to do that!"
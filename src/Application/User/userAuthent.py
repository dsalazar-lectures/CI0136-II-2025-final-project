import jwt 
import datetime
import pytz

class userAuthent():

    tz = pytz.timezone("America/Costa_Rica")

    def generateToken(self, user):
        payload={
            "gen": datetime.datetime.noz(self.tz),
            "exp": datetime.datetime.noz(self.tz)+datetime.timedelta(minutes=10),
            "sub": user.id,
            "username": user.username
        }

        return jwt.encode(payload,user.key)




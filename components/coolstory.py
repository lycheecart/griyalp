import twitchio
from twitchio.ext import commands
from random import choice as chx

class CoolStory(commands.Component):
    def __init__(self):
        self.setupquery = ""

    async def setupInserts(self):
        return

    def op(self):
        ppl_ops = [
            "my mates and me",
            "i had some friends who",
            "me and these guys",
            "me and some lads",
            "me and some blokes",
            "this club i was in"
        ]

        ppl_pres = [
            "liked to",
            "used to",
            "would",
            "every sunday we would",
            "every monday we would",
            "every tuesday we would",
            "every wednesday we would",
            "every thursday we would",
            "every friday we would",
            "every saturday we would",
            "every day we would",
            "quite frequently we'd"
        ]

        job_op = [
            "i had a job where my boss made me",
            "at this place i worked i had to",
            "i used get up at 10AM to"
        ]

        #i used to go 
        place_ops = [
            "upstairs at this bar and",
            "to this guy's basement and",
            "in the chemistry lab and",
            "in this culvert and",
            "to the gas station and",
            "to this parking lot and"
        ]
        return chx([chx(ppl_ops) + " " + chx(ppl_pres), chx(job_op), "i used to go " + chx(place_ops)])

    def activity(self):
        def throw():
            throwwords = ["lob", "hurl", "toss", "chuck"]
            throwobjs = [
                "bowling balls",
                "shopping carts",
                "stand mixers",
                "truck tires",
                "these big sacks",
                "discarded freezers",
                "mannequins",
                "motors",
                "washer tubs",
                "metal barrels",
                "dirty rags",
                "golf bags",
                "flasks of pocky",
                "bones from the garbage"
            ]
            return f"{chx(throwwords)} {chx(throwobjs)} at {chx(throwobjs)}"

        def offend():
            offenses = [
                "moon", 
                "flick off", 
                "burp at", 
                "do witch cackles at", 
                "scarecrow dance at", 
                "do nerd cackles at"
            ]
            offensetargets = [
                chx([
                    "runaway", 
                    "experimental", 
                    "overeager", 
                    "overzealous", 
                    "creepy", 
                    "mutated", 
                    "wild"]) + " " +
                chx([
                    "lynxes",
                    "wolverines",
                    "geese",
                    "lampreys",
                    "garter snakes",
                    "cans of tuna",
                    "boxes of donuts",
                    "limpkins",
                    "snails",
                    "seals",
                    "tortoises",
                    "frogs",
                    "beetles"
                ]),
                "escaped zoo crocodiles",
                "these huge raccoons",
                "packs of loose dogs",
                "old piles of manure",
                "an old lady"
            ]
            return f"{chx(offenses)} {chx(offensetargets)}"

        return chx([throw(), offend()])

    def ended_wh(self):
        ended_when = [
            "it all ended when",
            "it got too carried away when",
            "we had to stop because",
            "we all quit because"
        ]
        return chx(ended_when)

    def end_reason(self):
        def end_incident():
            end_incident = [
                "an investigation",
                "a death",
                "a lawsuit",
                "a drug bust",
                "a gas leak"
            ]
            return f"there was {chx(end_incident)}"

        def dismemberment():
            dismemberment = [
                "an eye",
                "a tooth ",
                "a finger",
                "a foot",
                "a whole toenail"
            ]
            return f"someone lost {chx(dismemberment)}"

        def personal_incident():
            incidents = [
                "i died",
                "they stopped shipping the gear for it",
                "the economy collapsed",
                "the whole thing was too much",
                "this crazy dude showed up",
                "i ripped my nutsack",
                "my car broke down",
                "the health department got involved",
                "we kept getting pwned"
            ]
            return f"{chx(incidents)}"

        return chx([end_incident(), dismemberment(), personal_incident()])

    def storyStr(self):
        return f"{self.op()} {self.activity()}, {self.ended_wh()} {self.end_reason()}."

    @commands.command(aliases=["story"])
    @commands.cooldown(rate=2, per=10, key=commands.BucketType.chatter)
    async def coolstory(self, ctx: commands.Context) -> None:
        """The bot tells a cool story

        !coolstory !story
        """
        await ctx.send(f"{self.storyStr()}")



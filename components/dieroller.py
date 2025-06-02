import twitchio
from twitchio.ext import commands
import random
import re

class Roller:
    def __init__(self):
        self.numPens = 0
        self.numExplosions = 0
        self.total = 0
        self.isPenetrating = False
        self.isExploding = False
        self.isSuperPenetrating = False
        self.resultStr = ""
        self.response = ""

    def refresh(self):
        self.numPens = 0
        self.numExplosions = 0
        self.total = 0
        self.isPenetrating = False
        self.isExploding = False
        self.isSuperPenetrating = False
        self.resultStr = ""

    def rollPen(self, faces, sign):
        decrStr = "-1"
        if sign < 0:
            decrStr = "+1"
        result = sign*random.randrange(1, faces + 1, 1)
        self.resultStr += ", pen[" + str(result) + decrStr + "]"
        self.total += result + -1*sign*1
        if abs(result) == faces:
            self.numPens += 1
            self.rollPen(faces, sign)

    def rollSuperPen(self, faces, sign):
        decrStr = "-1"
        if sign < 0:
            decrStr = "+1"
        result = sign*random.randrange(1, faces + 1, 1)
        self.resultStr += ", sPen[" + str(result) + decrStr + "]"
        self.total += result + -1*sign*1
        if abs(result) == faces:
            self.numPens += 1
            self.rollSuperPen(faces, sign)

    def rollExplosion(self, faces, sign):
        result = sign*random.randrange(1, faces + 1, 1)
        self.resultStr += ", expl[" + str(result) + "]"
        self.total += result
        if abs(result) == faces:
            self.numPens += 1
            self.rollExplosion(faces, sign)

    def roll(self, rolls, faces, sign=1):
        for i in range(rolls):
            result = sign*random.randrange(1, faces + 1, 1)
            self.resultStr += str(result)
            self.total += result
            if self.isPenetrating and abs(result) == faces:
                self.numPens += 1
                self.rollPen(faces, sign)
            elif self.isExploding and abs(result) == faces:
                self.numPens += 1
                self.rollExplosion(faces, sign)
            elif self.isSuperPenetrating and abs(result) >= faces-1:
                self.numPens += 1
                self.rollSuperPen(faces, sign)
            if i < rolls-1:
                self.resultStr += ", "
        self.response += self.resultStr + " "
        self.response += "(sum: " + str(self.total) + ") "

    def replyRoll(self, dieString):
        if "--" in dieString:
            self.response += "Warning: Replacing -- with +. "
            dieString = dieString.replace("--", "+")
        if "++" in dieString:
            self.response += "Warning: ++ found in roll request. "
            dieString = re.sub("\\++", "+", dieString)
        if "-+" in dieString:
            self.response += "Warning: -+ found in roll request. "
            dieString = re.sub("-\\+", "-", dieString)

        if dieString == "":
            self.response = "no die string"
        else:
            dieString = dieString.replace("-", "+-") #hack to delimit subractions and fix leading negative signs
            if dieString[0:2] == "+-": ###############
                dieString = dieString[1:] ############

            dieString = dieString.strip().lower().replace(" ", "")
            terms = re.split("\\+", dieString) 
            totalSum = 0
            totalPens = 0
            for term in terms:
                self.refresh()
                self.rollDieTerm(term)
                totalSum += self.total
                totalPens += self.numPens
            self.response += "Total Pens: " + str(totalPens) + ". "
            self.response += "Total Sum: " + str(totalSum) + "."
        return self.response

    def rollDieTerm(self, dieTerm):
        sign = 1
        badConditions = [
            dieTerm[-1] == "d",
            "d1p" in dieTerm,
            "d1P" in dieTerm,
            "d1e" in dieTerm,
            "d1E" in dieTerm,
            "d1u" in dieTerm,
            "d1U" in dieTerm,
            "d1b" in dieTerm,
            "d1B" in dieTerm,
            dieTerm == "-",
            dieTerm == ""
        ]
        if True in badConditions:
            self.response = "!!Bad die term!!: " + dieTerm + " " 
            return
        if dieTerm[0] == "-":
            sign = -1
            dieTerm = dieTerm[1:]
        signChar = "+"
        signPref = ""
        if sign < 0:
            signChar = "-"
            signPref = "-"
        digitMatch = re.match("^\\d+$", dieTerm)
        termIsConstant = False
        if digitMatch != None:
            termIsConstant = dieTerm == digitMatch.group(0)
        if termIsConstant:
            self.response += signChar + dieTerm + " "
            self.total += sign*int(dieTerm)
            return
        if dieTerm[0] == "d":
            dieTerm = "1" + dieTerm
        parts = re.split("[d]\\s*", dieTerm)
        numberOfRolls = int(parts[0])
        numberOfFaces = int(re.sub("[eEpPbBsS]", "", parts[1]))
        self.isExploding = "e" in parts[1] or "E" in parts[1]
        self.isPenetrating = "p" in parts[1] or "P" in parts[1]
        self.isSuperPenetrating = "b" in parts[1] or "s" in parts[1] or "B" in parts[1] or "S" in parts[1]
        self.response += "*roll " + signPref + parts[0] + "d" + parts[1] + "*: "
        """in case of d1p smartasses"""
        if self.isExploding and numberOfFaces < 2:
            self.isExploding = False
        if self.isSuperPenetrating and numberOfFaces < 3:
            self.isSuperPenetrating = False
        if self.isPenetrating and numberOfFaces < 2:
            self.isPenetrating = False
        """"""
        self.roll(numberOfRolls, numberOfFaces, sign)

class DieRoller(commands.Component):
    def __init__(self):
        self.setupquery = ""

    async def setupInserts(self):
        return

    @commands.command(aliases=["dieroll"])
    @commands.cooldown(rate=2, per=10, key=commands.BucketType.chatter)
    async def roll(self, ctx: commands.Context, *,  dieString:str = "") -> None:
        """Roll XdY or XdYp or XdYe: ex !roll 5d6e

        !roll !dieroll
        """
        if len(dieString) > 0:
            lastChar = dieString[-1]
            if lastChar in "+-":
                dieString+="0"

        if dieString.strip().replace(" ", "") == "":
            await ctx.reply("spins a marble", me=True)
        else:
            await ctx.reply(f"{Roller().replyRoll(dieString)}")


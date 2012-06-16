import random

class GenericRule(object):
    def __init__(self, symbol, subs=[], probs=[], 
                 draw2="True", draw3="True", 
                 prop=None, propFun=None):

        # Required whantot
        self.symbol = symbol
        self.subs   = subs
        self.probs  = probs

        sm = 0.0
        self.cdf = []
        for value in self.probs:
            sm += value
            self.cdf.append(sm) 

        # Drawing commands
        self.draw2 = draw2
        self.draw3 = draw3

        # Property to modify when called, and function to change it
        self.prop = prop
        self.propFun = propFun
        
    def apply(self):
        r = random.uniform(0.,1.)
        # print "r = ", r
        i = 0
        # while r > self.cdf[i]: i += 1
        for cdf in self.cdf: 
            if r > cdf: i+=1
        return self.subs[i]

    def _apply_property(self):
        if (self.prop == None) and (self.propFun == None):
            return
        print self.prop
        self.prop = self.propFun(self.prop)
        print self.prop

    def twoDraw(self, ctx):
        self._apply_property()
        eval(self.draw2)

    def threeDraw(self, ctx):
        self._apply_property()
        eval(self.draw3)
        
class BasicRule(GenericRule):
    pass

class EquallyLikely(GenericRule):
    pass

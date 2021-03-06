from pyparsing import ZeroOrMore, OneOrMore, Optional, Literal, Word, alphas, nums

'''
Created on 31 aug. 2013

Pyparsing grammar describing the trade section of EU4 save files

@author: Jeroen Kools
'''


# Terminals
eq = Literal("=").suppress()
begin = Literal("{").suppress()
stop = Literal("}").suppress()
quote = Literal('"').suppress()

name = quote + Word(alphas, alphas + nums + "_") + quote
yesno = Literal("yes") | Literal("no")
flt = Word(nums + ".-").setParseAction(lambda s, l, t: float(t[0]))
integer = Word(nums).setParseAction((lambda s, l, t: int(t[0])))

definitionsLine = Literal("definitions").suppress() + eq + name.setResultsName("name")
currentLine = Literal("current").suppress() + eq + flt.setResultsName("currentValue")
localValueLine = Literal("local_value").suppress() + eq + flt.setResultsName("localValue")
outgoingLine = Literal("outgoing").suppress() + eq + flt.setResultsName("outgoing")
valueAddedOutgoingLine = (Literal("value_added_outgoing") + eq + flt).suppress()
retentionLine = (Literal("retention") + eq + flt).suppress()
steerPowerLine = (Literal("steer_power") + eq + flt).suppress()
totalLine = (Literal("total").suppress() + eq + flt).suppress()  # total trade power
maxLine = (Literal("max") + eq + flt).suppress()
collectorPowerLine = (Literal("collector_power") + eq + flt).suppress()
pullPowerLine = (Literal("pull_power") + eq + flt).suppress()
retainPowerLine = (Literal("retain_power") + eq + flt).suppress()
highestPowerLine = (Literal("highest_power") + eq + flt).suppress()
valueLine = Literal("value").suppress() + eq + flt.setResultsName("incomingValue", True)
fromLine = Literal("from").suppress() + eq + integer.setResultsName("incomingFromNode", True)

countryLine = Literal("country") + eq + name
maxPowerLine = Literal("max_power") + eq + flt
provincePowerLine = Literal("province_power") + eq + flt
shipPowerLine = Literal("ship_power") + eq + flt
powerFractionLine = Literal("power_fraction") + eq + flt
powerFractionPushLine = Literal("power_fraction_push") + eq + flt
moneyLine = Literal("money") + eq + flt
steerPowerLine = Literal("steer_power") + eq + flt
typeLine = Literal("type") + eq + integer
actualAddedValueLine = Literal("actual_added_value").suppress() + eq + flt
hasTraderLine = Literal("has_trader") + eq + yesno
hasCapitalLine = Literal("has_capital") + eq + yesno
hasSubjectLine = Literal("has_subject") + eq + yesno

modifierSection = Literal("modifier") + eq + begin + \
        Literal("key") + eq + name + \
        Literal("duration") + eq + integer + \
        Literal("power") + eq + flt + stop

powerSection = Literal("power").suppress() + eq + begin + \
                (
                    countryLine +
                    currentLine +
                    maxPowerLine +
                    provincePowerLine +
                    shipPowerLine +
                    powerFractionLine +
                    powerFractionPushLine +
                    moneyLine +
                    totalLine +
                    steerPowerLine +
                    typeLine +
                    actualAddedValueLine +
                    hasTraderLine +
                    hasCapitalLine) + \
                    Optional(hasSubjectLine) + \
                    Optional(modifierSection) + \
                stop

tradegoodSection = Literal("trade_goods_size").suppress() + eq + begin + \
    OneOrMore(flt) + stop

incomingSection = (Literal("incoming").suppress() + eq + begin + \
    actualAddedValueLine + valueLine + fromLine + stop)

topProvincesSection = Literal("top_provinces").suppress() + eq + begin + OneOrMore(name) + stop
topProvincesValuesSection = Literal("top_provinces_values").suppress() + eq + begin + OneOrMore(flt) + stop
topPowerSection = Literal("top_power").suppress() + eq + begin + OneOrMore(name) + stop
topPowerValuesSection = Literal("top_power_values").suppress() + eq + begin + OneOrMore(flt) + stop

nodeSection = (Literal("node").suppress() + eq + begin + \
                 definitionsLine +
                 currentLine +
                 localValueLine +
                 outgoingLine +
                 valueAddedOutgoingLine +
                 retentionLine +
                 ZeroOrMore(steerPowerLine) +
                 totalLine +
                 maxLine +
                 collectorPowerLine +
                 pullPowerLine +
                 retainPowerLine +
                 highestPowerLine +
                ZeroOrMore(powerSection).suppress() +
                ZeroOrMore(incomingSection) +
                tradegoodSection +
                Optional(topProvincesSection) +
                Optional(topProvincesValuesSection) +
                Optional(topPowerSection) +
                Optional(topPowerValuesSection) +
                stop).setResultsName("Nodes", True)

tradeSection = begin + OneOrMore(nodeSection) + stop

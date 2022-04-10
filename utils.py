import math

def pf_calc(params, prev):
    if params["CURRENT"]!=0:
        params["CURRENT"]=(((params["CURRENT"]+2)/4)*.8)-0.35
    if params["SAMPLECOUNT"]==50:
        avgPeriod= params["PERIODSAMPLE"]/params["SAMPLECOUNT"]
        params["FREQUENCY"]=1000000/avgPeriod
        phaseDiff=params["PHASEANGLE"]/params["SAMPLECOUNT"]
        params["PHASEANGLE"]=((phaseDiff*360) / avgPeriod)
        params["POWERFACTOR"]=math.cos(params["PHASEANGLE"]*math.pi/180)
        params["POWER"]=(params["CURRENT"]*params["VOLTAGE"]*params["POWERFACTOR"])
        try:
            params["ENERGY"]=prev[-2]+params["POWER"]*0.02/3600
            params["TARIFF"]=prev[-1]+params["ENERGY"]*5.5/1000
        except:
            params["ENERGY"]=params["POWER"]*0.02/3600
            params["TARIFF"]=550+params["ENERGY"]*5.5/1000

    elif params["SAMPLECOUNT"]!=50 and prev is not None:
        params["TARIFF"]=prev[-1]
        params["ENERGY"]=prev[-2]
        params["POWER"]=prev[-3]
        params["FREQUENCY"] = prev[-4]
        params["POWERFACTOR"] = prev[-5]
        params["PHASEANGLE"] = prev[-6]

    else:
        params["FREQUENCY"]=0
        params["PHASEANGLE"]=0
        params["POWERFACTOR"]=1
        params["POWER"]=0
        params["ENERGY"]=0
        params["TARIFF"]=550
    return params

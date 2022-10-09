class candle:
    def __init__(self,openTime,closeTime,openPrice,closePrice,Low, High, Volume):
        self.openTime = openTime
        self.closeTime = closeTime
        self.openPrice = openPrice
        self.closePrice =closePrice
        self.Low = Low
        self.High =High
        self.Volume = Volume
    def getAmplitude(self):
        amplitude=float(self.closePrice)-float(self.openPrice)
        amplitudePercent=(amplitude/float(self.openPrice))*100
        return amplitudePercent


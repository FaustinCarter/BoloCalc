#python Version 2.7.2
import numpy     as np
import parameter as pr
import units     as un
import physics   as ph

class Detector:
    def __init__(self, log, ch, band=None):
        self.log  = log
        self.ch   = ch
        self.__ph = ph.Physics()

        #Store detector parameters
        self.bandCenter    = self.__paramSamp(ch.params['Band Center'],     ch.bandID)
        self.fbw           = self.__paramSamp(ch.params['Fractional BW'],   ch.bandID)
        self.detEff        = self.__paramSamp(ch.params['Det Eff'],         ch.bandID)
        self.psat          = self.__paramSamp(ch.params['Psat'],            ch.bandID)
        self.psatFact      = self.__paramSamp(ch.params['Psat Factor'],     ch.bandID)
        self.n             = self.__paramSamp(ch.params['Carrier Index'],   ch.bandID)
        self.Tc            = self.__paramSamp(ch.params['Tc'],              ch.bandID)
        self.TcFrac        = self.__paramSamp(ch.params['Tc Fraction'],     ch.bandID)
        self.nei           = self.__paramSamp(ch.params['SQUID NEI'],       ch.bandID)
        self.boloR         = self.__paramSamp(ch.params['Bolo Resistance'], ch.bandID)
        self.readN         = self.__paramSamp(ch.params['Read Noise Frac'], ch.bandID)
        self.flo, self.fhi = self.__ph.bandEdges(self.bandCenter, self.fbw)
        self.Tb            = ch.Tb
        if 'NA' in str(self.Tc): self.Tc = self.Tb*self.TcFrac

        #Load band
        if band is not None:
            eff  = band
            if eff is not None:
                eff = np.array([e if e > 0 else 0. for e in eff])
                eff = np.array([e if e < 1 else 1. for e in eff])
        else: 
            #Default to top hat band
            eff = [self.detEff if f > self.flo and f < self.fhi else 0. for f in ch.freqs]

        #Store detector optical parameters
        self.elem  = ["Detector"]
        self.emiss = [[0.000 for f in ch.freqs]]
        self.effic = [eff]
        self.temp  = [[self.Tb for f in ch.freqs]]

    #***** Private Methods *****
    def __paramSamp(self, param, bandID): 
        if not 'instance' in str(type(param)): return np.float(param)
        if self.ch.clcDet == 1: return param.getAvg(bandID=bandID)
        else:                   return param.sample(bandID=bandID, nsample=1)

#python Version 2.7.2
import numpy        as np
import observation  as ob
import scanStrategy as sc
import units        as un

class ObservationSet:
    def __init__(self, log, detArray, sky, scn, belv=0., nobs=1, elvDict=None):
        self.log      = log
        self.detArray = detArray
        self.sky      = sky
        self.scn      = scn
        self.belv     = belv
        self.nobs     = nobs
        self.elvDict  = elvDict
        
        #Store the elevation values and probabilities
        if self.elvDict is not None:
            self.elVals = np.array(elvDict.keys()  ).astype(np.float)
            self.elFrac = np.array(elvDict.values()).astype(np.float)
        else:
            self.elVals = None
            self.elFrac = None

        #Store observation objects
        self.observations = [ob.Observation(self.log, self, self.detArray, self.sky, self.scn, belv=self.belv) for n in range(nobs)]
        #Store sky temperatures and efficiencies
        self.temps  = np.array([obs.temp  for obs in self.observations])
        self.effics = np.array([obs.effic for obs in self.observations])

    # ***** Pubic Methods *****
    #Sample elevation distribution
    def pixElvSample(self):
        if self.elVals is not None and self.elFrac is not None: return np.random.choice(self.elVals, size=1, p=self.elFrac/np.sum(self.elFrac))[0]
        else:                                                   return 0.

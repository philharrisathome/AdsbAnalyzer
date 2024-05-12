from dashing import *

import ViewInterface
import AdsbAnalysisEngine

class CurrentAircraftView(ViewInterface.ViewInterface):

    __aae = None
    __panel = None

    def __init__(self, aae, panel):
        self.__aae = aae
        self.__panel = panel

    # Returns True on success, False on failed
    def create(self) -> bool:
        # Nothing to do
        return True

    def update(self) -> None:

        t = ''
        ids = self.__aae.currentAircraftIds()
        for k,v in ids.items():
            if 'callsign' in v:
                t = t + '{t.green}{} {t.bold_blue}({}){t.normal}\n'.format(k, v['callsign'], t=Terminal())
            else:
                t = t + '{t.green}{} {t.bold_blue}(.){t.normal}\n'.format(k, t=Terminal())

        self.__panel.text = t


from dashing import *

import ViewInterface
import AdsbAnalysisEngine

class AnalyzerStatisticsView(ViewInterface.ViewInterface):

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
        mc = self.__aae.messageCount()
        t = '{t.white}Message count: {t.orange}{}{t.normal}\n\n'.format(mc, t=Terminal())

        ha = self.__aae.highestAircraft()
        t = t + '{t.white}Highest aircraft: {t.green}{} {t.red}({}){t.normal}\n'.format(ha['hexId'], ha['altitude'], t=Terminal())

        la = self.__aae.lowestAircraft()
        t = t + '{t.white}Lowest aircraft: {t.green}{} {t.blue}({}){t.normal}\n'.format(la['hexId'], la['altitude'], t=Terminal())

        fa = self.__aae.fastestAircraft()
        t = t + '{t.white}Fastest aircraft: {t.green}{} {t.red}({}){t.normal}\n'.format(fa['hexId'], fa['groundSpeed'], t=Terminal())

        sa = self.__aae.slowestAircraft()
        t = t + '{t.white}Slowest aircraft: {t.green}{} {t.blue}({}){t.normal}\n'.format(sa['hexId'], sa['groundSpeed'], t=Terminal())

        self.__panel.text = t


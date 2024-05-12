from dashing import *

import CurrentAircraftView, AnalyzerStatisticsView, StatusView

class ViewManager:

    __ui = None

    def __init__(self, aae):
        self.__ui = HSplit(
                VSplit(
                    Text(title="Status".format(t=Terminal()), text="", border_color=7),
                    Text(title="Statistics".format(t=Terminal()), text="", border_color=7)
                ),
                Text(title="Current Aircraft".format(t=Terminal()), text="", border_color=7),
                title="{t.bold_white}ADS-B Analyzer{t.normal}".format(t=Terminal())
            )

        self.__vws = [
            StatusView.StatusView(aae, self.__ui.items[0].items[0]), 
            AnalyzerStatisticsView.AnalyzerStatisticsView(aae, self.__ui.items[0].items[1]), 
            CurrentAircraftView.CurrentAircraftView(aae, self.__ui.items[1])
            ]

    # Returns True on success, False on failed
    def create(self) -> bool:
        open_terminal()
        print(Terminal().home + Terminal().clear + Terminal().white)
        
        # Create all of the views
        for v in self.__vws:
            v.create()
        return True

    def close(self):
        print(Terminal().home + Terminal().clear + Terminal().white)

    def update(self) -> None:
        # Update all of the views
        for v in self.__vws:
            v.update()
        # Redraw the UI
        print(Terminal().home + Terminal().clear + Terminal().white)
        self.__ui.display()


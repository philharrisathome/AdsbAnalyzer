from datetime import datetime, timezone
from dashing import *
import time

import ViewInterface

class StatusView(ViewInterface.ViewInterface):

    __panel = None

    def __init__(self, aae, panel):
        self.__panel = panel

    # Returns True on success, False on failed
    def create(self) -> bool:
        # Nothing to do
        return True

    def update(self) -> None:
        now = time.time()
        t = "{t.white}Time now is: {t.bold_white}{}{t.normal}\n".format(self.ts(now), t=Terminal())

        self.__panel.text = t

    @staticmethod
    def ts(t):
        # Format timestamp
        dt = datetime.fromtimestamp(t, tz=timezone.utc)
        return dt.strftime("%d %b %Y %H:%M:%S %Z")
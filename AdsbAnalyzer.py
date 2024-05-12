import datetime as dt
import traceback
import sys

import SBSFileReceiver, SBSReceiver
import AdsbAnalysisEngine
import ViewManager

def main() -> int:

    try:

        # Open the receiver interface
        if True:
            rx = SBSReceiver.SBSReceiver({'ip': '192.168.1.7', 'port': 30003, 'logfile': 'adsbdata.txt'})
        else:
            rx = SBSFileReceiver.SBSFileReceiver({'logfile': 'adsbdata.txt', 'msgcount': 10, 'pause': 0.02})
        if not rx.open():
            print('ERROR: Failed to open receiver interface')
            return 1    # Error - could not open receiver

        # Create the managers
        aae = AdsbAnalysisEngine.AdsbAnalysisEngine()
        vm = ViewManager.ViewManager(aae)

        # Create the view
        vm.create()

        lastViewUpdate = dt.datetime.min
        while(True):
            # Process any received messages
            msg = rx.getMessages()
            for m in msg:
                aae.processMessage(m)

            if ((dt.datetime.now() - lastViewUpdate) > dt.timedelta(milliseconds=1000)):
                lastViewUpdate = dt.datetime.now()
                # Update view
                vm.update()

    except KeyboardInterrupt:
        rx.close()
        vm.close()
        return 0    # Success

    except Exception as exc:
        rx.close()
        vm.close()
        print(traceback.format_exc())
        return 1    # Error - Unknown exception

if __name__ == '__main__':
    sys.exit(main())

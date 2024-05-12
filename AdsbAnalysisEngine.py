from abc import ABC, abstractmethod

class AdsbAnalysisEngine:

    # Abstract base class
    class AnalyzerInterface(ABC):

        @abstractmethod
        def reset(self) -> None:
            pass

        @abstractmethod
        def update(self, header, data) -> None:
            pass

    # Local class for capturing general statistics
    class GeneralStatistics(AnalyzerInterface):
        messageCount = 0

        def __init__(self):
            pass

        def reset(self):
            self.messageCount = 0

        def update(self, header, data):
            self.messageCount = self.messageCount + 1

    # Local class for capturing aircraft observations
    class Observations(AnalyzerInterface):
        hexIds = {}

        def __init__(self):
            pass

        def reset(self):
            self.hexIds = {}

        def update(self, header, data):
            hexId = header['hexId']
            if not hexId in self.hexIds:
                self.hexIds[hexId] = {}
            
            self.hexIds[hexId]['lastSeen'] = header['time']
            for k, v in data.items():
                self.hexIds[hexId][k] = v

    # Local class for capturing extreme data values
    class LeaderBoard(AnalyzerInterface):
        fastestAircraft = {'hexId': '', 'groundSpeed': 0}
        slowestAircraft = {'hexId': '', 'groundSpeed': 1e6}
        highestAircraft = {'hexId': '', 'altitude': 0}
        lowestAircraft = {'hexId': '', 'altitude': 1e6}

        def __init__(self):
            pass

        def reset(self):
            self.fastestAircraft = {'hexId': '', 'groundSpeed': 0}
            self.slowestAircraft = {'hexId': '', 'groundSpeed': 1e6}
            self.highestAircraft = {'hexId': '', 'altitude': 0}
            self.lowestAircraft = {'hexId': '', 'altitude': 1e6}

        def update(self, header, data):
            # Record the fastest aircraft
            if ('groundSpeed' in data) and (data['groundSpeed'] > self.fastestAircraft['groundSpeed']):
                self.fastestAircraft['hexId'] = header['hexId']
                self.fastestAircraft['groundSpeed'] = data['groundSpeed']

            # Record the slowest aircraft
            if ('groundSpeed' in data) and (data['groundSpeed'] < self.slowestAircraft['groundSpeed']):
                self.slowestAircraft['hexId'] = header['hexId']
                self.slowestAircraft['groundSpeed'] = data['groundSpeed']

            # Record the highest aircraft
            if ('altitude' in data) and (data['altitude'] > self.highestAircraft['altitude']):
                self.highestAircraft['hexId'] = header['hexId']
                self.highestAircraft['altitude'] = data['altitude']

            # Record the lowest aircraft
            if ('altitude' in data) and (data['altitude'] < self.lowestAircraft['altitude']):
                self.lowestAircraft['hexId'] = header['hexId']
                self.lowestAircraft['altitude'] = data['altitude']

    #------------------------------------------------------------------------------------------

    __general = GeneralStatistics()
    __observations = Observations()
    __leaderBoard = LeaderBoard()

    # The collection of analyzers
    __analyzers = [__general, __observations, __leaderBoard]

    def __init__(self):
        pass

    def reset(self):
        for a in self.__analyzers:
            a.reset()

    def processMessage(self, msg):
        hd = self.extractMessageHeader(msg)
        header = hd[0]
        data = hd[1]

        # Only want to process MSG types, ignore everything else
        if header['sbsType'] != 'MSG':
            return
        
        # Extract the remaining data
        data = self.extractMessageData(data)

        # Update all of the analyzers
        for a in self.__analyzers:
            a.update(header, data)

    # See http://woodair.net/sbs/article/barebones42_socket_data.htm
    # Header is first 10 fields
    # Data is remaining fields
    # MSG,1,1,1,3951C1,1,2024/05/11,22:22:00.336,2024/05/11,22:22:00.365,AFR6736 ,,,,,,,,,,,0
    @staticmethod
    def extractMessageHeader(msg):
        fields = msg.split(',', 10)

        header = {}
        header['sbsType'] = fields[0]
        header['txType'] = int(fields[1])
        # Ignore fields 2,3
        header['hexId'] = fields[4]
        # Ignore field 5
        header['date'] = fields[6]
        header['time'] = fields[7]
        # Ignore fields 8,9

        data = fields[-1]

        return header, data

    # See http://woodair.net/sbs/article/barebones42_socket_data.htm
    # Header is first 10 fields
    # Data is remaining fields
    # MSG,1,1,1,3951C1,1,2024/05/11,22:22:00.336,2024/05/11,22:22:00.365,AFR6736 ,,,,,,,,,,,0
    @staticmethod
    def extractMessageData(msg):
        fields = msg.strip().split(',')

        data = {}
        if fields[0]: data['callsign'] = fields[0].strip()
        if fields[1]: data['altitude'] = float(fields[1])
        if fields[2]: data['groundSpeed'] = float(fields[2])
        if fields[3]: data['track'] = float(fields[3])
        if fields[4]: data['latitude'] = float(fields[4])
        if fields[5]: data['longitude'] = float(fields[5])
        if fields[6]: data['verticalRate'] = float(fields[6])
        # Ignore fields 7-10
        if fields[11]: data['isOnGround'] = bool(int(fields[11]))

        return data

    #------------------------------------------------------------------------------------------
    # Methods used by the views

    def messageCount(self):
        return self.__general.messageCount

    def currentAircraftIds(self):
        return self.__observations.hexIds
    
    def highestAircraft(self):
        return self.__leaderBoard.highestAircraft

    def lowestAircraft(self):
        return self.__leaderBoard.lowestAircraft

    def fastestAircraft(self):
        return self.__leaderBoard.fastestAircraft

    def slowestAircraft(self):
        return self.__leaderBoard.slowestAircraft

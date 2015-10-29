

import LogDateInfo


class LogNotes:
    def __init__(self, logTitle, notes, filterList):
        self.log = LogDateInfo.LogDateInfo(logTitle).GetLogStream()
        
        if notes == None:
            self.log += 'No notes found!\n'
            return self.log

        for index in range(0, len(notes)):
            self.log += '-----------------------------\t'+str(index)+'\t-----------------------------\n'

            for node in filterList:
                self.log += node.MakeLogStream(notes[index])

            self.log += '------------------------------------------------------------------\n\n\n'

    def GetLogStream(self):
        return self.log



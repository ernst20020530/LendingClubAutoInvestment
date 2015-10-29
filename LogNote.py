

import LogDateInfo


class LogNote(object):
    def __init__(self, logTitle, note, noteIndex, filterList):
        self.log = LogDateInfo.LogDateInfo(logTitle).GetLogStream()
        
        if note == None:
            self.log += 'No notes found!\n'
            return self.log

        self.log += '-----------------------------\t'+str(noteIndex)+'\t-----------------------------\n'

        for node in filterList:
            self.log += node.MakeLogStream(note)

        self.log += '------------------------------------------------------------------\n\n\n'

    def GetLogStream(self):
        return self.log




from LogLine import LogLine
from NotesSort import NotesSort
import threading


class FilterBase(object):

    sumPercentile = 'sumPercentile'

    def __init__(self, name, arg, logFile, monitorLog, fileLog):
        self.name = name
        self.arg = arg[name]
        self.monitorLog = monitorLog
        self.logFile = logFile
        self.fileLog = fileLog
        self.lock = threading.Lock()

    def EnableMonitorLog(self):
        self.lock.acquire()
        self.monitorLog = True
        self.lock.release()
       

    def DisableMonitorLog(self):
        self.lock.acquire()
        self.monitorLog = False
        self.lock.release()


    def GetMonitorLog(self):
        self.lock.acquire()
        monitorLog = self.monitorLog
        self.lock.release()
        return monitorLog


    def EnableFileLog(self):
        self.lock.acquire()
        self.fileLog = True
        self.lock.release()


    def DisableFileLog(self):
        self.lock.acquire()
        self.fileLog = False
        self.lock.release()


    def GetFileLog(self):
        self.lock.acquire()
        fileLog = self.fileLog
        self.lock.release()
        return fileLog


    def Start(self, notes):
        return notes


    def Filter(self, notes):
        return notes 


    def MakeLogStream(self, note):
        fields = self.GetShowFields()

        logline = LogLine(self.name)
        for f in fields:
            logline.logField(f,note)

        return logline.Get()


    def GetShowFields(self):
        pass

    def GetPercentileFields(self):
        pass


    def CalculatePercentiles(self, notes):
        if len(notes) == 0:
            return notes
        percentileFields = self.GetPercentileFields()
        if percentileFields == None:
            return notes
        else:
            for f in self.GetPercentileFields():
                notes = self.CalculateIndividualPercentile(notes, f.percentileField, f.descending)
            return notes

    
    def CalculateIndividualPercentile(self, notes, field, descending):
        ns = NotesSort(notes, self.logFile, self.monitorLog, self.fileLog)
        ns.SortOnPrimaryField(field, descending)
        notes = ns.notesFiltered

        perField = 'per_'+field

        length = len(notes)

        lastValue = notes[0][field]
        lastIndex = 0

        for i in range(0,length):
            #if the current value is equal to prior value, we need to assign same index value as prior
            if notes[i][field] == lastValue:
                notes[i][perField] = lastIndex / float(length)
            else:
                notes[i][perField] = i / float(length)
                lastValue = notes[i][field]
                lastIndex = i
            log = str(field) + '\t' + str(notes[i][field]) +'\t' + str(notes[i][perField])
            if self.GetMonitorLog():
                print(log)
            if self.GetFileLog():
                self.logFile.writelines(log)

        return notes


    def SumPercentiles(self, notes):
        percentileFields = self.GetPercentileFields()
        if percentileFields == None:
            return notes
        else:
            for f in self.GetPercentileFields():
                notes = self.SumIndividualPercentile(notes, f.percentileField, f.weight)
            return notes

    def SumIndividualPercentile(self, notes, field, weight):
        perField = 'per_'+field

        for n in notes:
            n[FilterBase.sumPercentile] += n[perField] *weight
            log = str(n['id']) + '\n' + str(field) + '\t' + str(n[perField]) +'\t' + str(n[FilterBase.sumPercentile])
            if self.GetMonitorLog():
                print(log)
            if self.GetFileLog():
                self.logFile.writelines(log)

        return notes




class PercentileNode:
    def __init__(self, 
                 percentileField,                           #string type for the field
                 descending,                                #True: if 0 is the most important       False: if max is most important
                 weight = 50):                              #weight for each percentile             range:0 ~ 100 default is 50
        self.percentileField = percentileField
        self.descending = descending

        if weight < 0:
            self.weight = 0
        elif weight > 100:
            self.weight = 1
        else:
            self.weight = weight / float(100)
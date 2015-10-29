


class NotesSort(object):
    def __init__(self, notesFiltered, logFile, monitorLog, fileLog):
        self.notesFiltered = notesFiltered
        self.logFile = logFile
        self.monitorLog = monitorLog
        self.fileLog = fileLog

    def SortOnPrimaryField(self, primaryField, descending):
        for i in range(1, len(self.notesFiltered)):
            for j in range(0,len(self.notesFiltered) - i):

                b = True
                if descending == True:
                    b = self.notesFiltered[j][primaryField] < self.notesFiltered[j +1][primaryField]
                else:
                    b = self.notesFiltered[j][primaryField] > self.notesFiltered[j +1][primaryField]

                if b:
                    tmp = self.notesFiltered[j]
                    self.notesFiltered[j] = self.notesFiltered[j +1]
                    self.notesFiltered[j +1] = tmp

        for i in self.notesFiltered:
            logStream = str(i[primaryField])+','+i['grade']
            if self.monitorLog:
                print(str(i[primaryField])+','+i['grade'])
            if self.fileLog:
                self.logFile.writelines(logStream)



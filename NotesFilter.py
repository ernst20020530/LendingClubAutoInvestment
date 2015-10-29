

from NotesSort import NotesSort


class NotesFilter(object):
    
    def __init__(self,notesListed, *args, **kwargs):
        super(NotesFilter, self).__init__(*args, **kwargs)
        self.notesListed = notesListed
        for i in self.notesListed:
            i['intDefaultRatio'] = i['intRate'] / i['expDefaultRate']




  




    def ShowAllNotesLeft(self, fields):
        for i in self.notesListed:
            string = ''
            for f in fields:
                string += f
                string += ':'
                string += str(i[f])
                string += '\t'
            print(string)




    def CreateNotesSort(self):
        return NotesSort(self.notesListed)





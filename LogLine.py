


class LogLine(object):
    def __init__(self, section):
        self.string = '<'+section+'>\t\t'

    def logField(self,field,note):
        self.string += '['+field+']:\t' + str(note[field]) + '\t'
        return self

    def logElement(self, variable, value):
        self.string += variable + ':\t' + str(value) + '\t'
        return self

    def logString(self, str):
        self.string += str
        return self


    def Get(self):
        self.string += '\n'
        return self.string






class Pather(object):
    def __init__(self):
        self.level = 1
        self.path = []
        self.optPath = []
    
    def StartRecord(self, level):
        self.level = level
        self.path = []
        self.optPath = None
        try:
            with open("data/path/" + str(level) + ".y", "r") as fp:
                path = fp.readlines()[0]
                path = path.split(',')
                self.optPath = [ int(p) for p in path]
        except: pass

    def AddRecord(self, dir):
        self.path.append( str(dir) )

    def DumpRecord(self):
        if self.optPath == None or len(self.path) < len(self.optPath):
            line = ','.join(self.path)
            with open("data/path/" + str(self.level) + ".y", "w") as fp:
                fp.write(line)
    
    def getRecords(self):
        return self.optPath or []
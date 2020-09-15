import time


class perfMonitor:
    def __init__(self):
        self.initTime = time.time()
        self.log = []

    def startProc(self, procType):
        sameType = 0
        for proc in self.log:
            if proc.procType == procType:
                sameType += 1
        return Process(procType, sameType)

    def endProc(self, process):
        process.end = time.time()
        self.log.append(process)

    def exit(self):
        exitTime = time.time()
        totalTime = exitTime - self.initTime
        countedTime = 0
        processList = []
        timeList = []
        for processTimed in self.log:
            if processTimed.procType in processList:
                timeList[processList.index(
                    processTimed.procType)] += processTimed.end - processTimed.start
            else:
                processList.append(processTimed.procType)
                timeList.append(processTimed.end - processTimed.start)
        print("Execution time breakdown (%.3fs):" % totalTime)
        for process in processList:
            processTime = timeList[processList.index(process)]
            countedTime += processTime
            print("%s: %.2f%% (%.3fs)" %
                  (process, 100 * processTime / totalTime, processTime))
        otherTime = totalTime - countedTime
        print("Other: %.2f%% (%.3fs)\n" %
              (100 * otherTime / totalTime, otherTime))


class Process:
    def __init__(self, procType, number):
        self.start = time.time()
        self.end = 0
        self.procType = procType
        self.number = number

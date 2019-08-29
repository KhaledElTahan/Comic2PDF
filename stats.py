import os

def countFiles(extensions):
    directories = [x[0] for x in os.walk(os.getcwd())]

    cnt = 0

    for directory in directories:
        for file in os.listdir(directory):
            for ext in extensions:
                if file.endswith(ext):
                    cnt = cnt + 1

    return cnt


def statistics():
    cbrCnt = countFiles(['.cbr'])
    rarCnt = countFiles(['.rar'])
    cbzCnt = countFiles(['.cbz'])
    zipCnt = countFiles(['.zip'])

    comicsCnt = cbrCnt + rarCnt + cbzCnt + zipCnt

    pdfCnt = countFiles(['.pdf'])

    print("Statistics::START")

    print("* Comics: {0}".format(comicsCnt))
    print("----  CBR: {0}".format(cbrCnt))
    print("----  RAR: {0}".format(rarCnt))
    print("----  CBZ: {0}".format(cbzCnt))
    print("----  ZIP: {0}".format(zipCnt))

    print("")
    
    print("* Pdf: {0}".format(pdfCnt))

    print("Statistics::END")


if __name__ == "__main__":	
    statistics()
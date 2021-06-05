import re
import json

def setJSON(jsonFileName, jsonText):
    with open(jsonFileName,'w') as jsonFile:
        jsonFile.write(json.dumps(jsonText, indent=2))
    return jsonFile.closed

def getVAGRANTFILE(vagrantFileName):
    with open(vagrantFileName) as VagrantFile:
        VagrantFile.read()
    return VagrantFile.closed

def printJSON(jsonFile):
    print(json.dumps(jsonFile, indent=2))

def calcNumberIndent(line):
    for i in range(len(line)):
        if line[i] != " ":
            break
    return i

def verifIndent(file):
    with open(file,"r") as vagrantfile:
        previousIndent = 0
        numberLine = 0
        for line in vagrantfile:
            numberLine += 1
            if not line.strip():
                continue
            newIndent = calcNumberIndent(line)
            diff = abs(newIndent - previousIndent)
            # print("Previous : ", previousIndent, "New : ", newIndent, "diff : ", diff)
            if diff != 2 and diff != 0:
                # return "Vérification de l'indentation: échec. Issue line {}.".format(numberLine)
                return numberLine
            previousIndent = newIndent
    # return "Vérification de l'indentation: succès."
    return True


def convertVAGRANTFILEtoJSON(file):
    with open(file,"r") as vagrantfile:
        jsonFile = {}
        indent = 0
        for line in vagrantfile:
            if not line.strip():
                continue

            indent = calcNumberIndent(line)

            if line.startswith("config.vm.define",indent):
                regex = re.compile("\s\".+\"\s")
                matchObject = regex.search(line)
                if matchObject:
                    nameVM = matchObject.group(0).strip()
                    jsonFile[nameVM] = { "cfg" : {}}
                    newVM = jsonFile[nameVM]["cfg"]

            if line.startswith("cfg.vm.",indent):
                regex = re.compile("cfg\.vm\.(\w+)[\s\=]+(.+)")
                matchObject = regex.search(line)

                if matchObject:
                    nameParamVM = matchObject.group(1).strip()
                    paramVM = matchObject.group(2).strip()

                    if nameParamVM == "provider":
                        if paramVM[1:11] == "virtualbox":
                            paramVM = "\"virtualbox\""
                            newVM[nameParamVM] = paramVM
                            newVM["vb"] = {}
                            newVB = newVM["vb"]
                    else:
                        if nameParamVM == "provision":
                            if nameParamVM not in newVM:
                                newVM[nameParamVM] = [paramVM]
                            else:
                                newVM[nameParamVM].append(paramVM)
                        else:
                            newVM[nameParamVM] = paramVM

            if line.startswith("vb.",indent):
                regex = re.compile("vb\.(\w+)[\s\=]+(.+)")
                matchObject = regex.search(line)

                if matchObject:
                    nameParamVB = matchObject.group(1).strip()
                    paramVB = matchObject.group(2).strip()
                    if nameParamVB == "customize":
                        if nameParamVB not in newVB:
                            newVB[nameParamVB] = [paramVB]
                        else:
                            newVB[nameParamVB].append(paramVB)
                    else:
                        newVB[nameParamVB] = paramVB

    return jsonFile


if __name__ == "__main__":
    vagrantFileName = "TEMP-vagrantfile"
    jsonFileName = "TEMP-jsonfile.json"
    result1 = verifIndent(vagrantFileName)
    print("Vérification de l'indentation : ", result1)
    jsonText = convertVAGRANTFILEtoJSON(vagrantFileName)
    printJSON(jsonText)
    result2 = setJSON(jsonFileName, jsonText)
    print("Ecriture du fichier ",jsonFileName," : ", result2)

"""
This decompiler converts a VagrantFile to a jsonFile.
"""

# IMPORT
import re
import json

# FUNCTIONS
def setJSON(jsonFileName, jsonText):
    """
    Function writing a python json in a json file with json format

    @param `jsonFileName`: name of the json file to write to
    @param `jsonText`: json text to write in the json file

    @return `jsonFile.closed`: boolean (True if the json file successfully closed else False)
    """
    with open(jsonFileName,'w') as jsonFile:
        jsonFile.write(json.dumps(jsonText, indent=2))
    return jsonFile.closed


def getVAGRANTFILE(vagrantFileName):
    """
    Function getting the content of a VagrantFile (not used but for potential future use)

    @param `vagrantFileName`: name of the vagrant file to get the content

    @return `vagrantText`: string with the vagrant content
    """
    with open(vagrantFileName) as vagrantFile:
        vagrantText = vagrantFile.read()
    return vagrantText


def printJSON(jsonText):
    """
    Function printing a python json in the console (useful for debug, not production)

    @param `jsonText`: json text to print

    """
    print(json.dumps(jsonTextndent=2))


def calcNumberIndent(line):
    """
    Function calculating the number of indents at the beginning of a given string

    @param `line`: string

    @return `numberIndent`: integer number of indents at the beginning of the given string
    """
    for numberIndent in range(len(line)):
        if line[numberIndent] != " ":
            break
    return numberIndent

def verifIndent(vagrantFileName):
    """
    Function verifying the correct indent format of a vagrant file

    @param `vagrantFileName`: name of the vagrant file to verify

    @return `True`: boolean if the vagrant file has correct indentation
    @return `indentErrorMessage` : string with the number of the line badly indented else
    """
    with open(vagrantFileName,"r") as vagrantfile:
        previousIndent = 0
        numberLine = 0
        for line in vagrantfile:
            numberLine += 1
            if not line.strip():
                continue
            newIndent = calcNumberIndent(line)
            diff = abs(newIndent - previousIndent)
            if diff != 2 and diff != 0:
                indentErrorMessage = "error line {}".format(numberLine)
                return indentErrorMessage
            previousIndent = newIndent
    return True


def convertVAGRANTFILEtoJSON(vagrantFileName):
    """
    Function converting a vagrant file in a python json

    @param `vagrantFileName`: name of the vagrant file to convert to json

    @return `jsonText: json
    """
    with open(vagrantFileName,"r") as vagrantfile:
        jsonText = {}
        indent = 0
        intro = True # position of reading first lines before configuration
        for line in vagrantfile:
            if not line.strip():
                continue

            indent = calcNumberIndent(line)

            if line.startswith("Vagrant.configure(",indent):
                intro = False

            if intro:
                if "intro" not in jsonText:
                    jsonText["intro"] = [line]
                else:
                    jsonText["intro"].append(line)

            if line.startswith("config.vm.define",indent):
                regex = re.compile("\s\".+\"\s")
                matchObject = regex.search(line)
                if matchObject:
                    nameVM = matchObject.group(0).strip()
                    jsonText[nameVM] = { "cfg" : {}}
                    newVM = jsonText[nameVM]["cfg"]


            if line.startswith("cfg.",indent):
                regex = re.compile("cfg\.((?:vm)?(?:winrm)?)\.(\w+)[\s\=]+(.+)")
                matchObject = regex.search(line)

                if matchObject:
                    vmOrWinrm = matchObject.group(1).strip()
                    nameParamVM = matchObject.group(2).strip()
                    paramVM = matchObject.group(3).strip()
                    if vmOrWinrm not in newVM:
                        newVM[vmOrWinrm] = {}

                    if nameParamVM == "provider":
                        if paramVM[1:11] == "virtualbox":
                            paramVM = "\"virtualbox\""
                            newVM[vmOrWinrm][nameParamVM] = paramVM
                            newVM[vmOrWinrm]["vb"] = {}
                            newVB = newVM[vmOrWinrm]["vb"]
                    else:
                        if nameParamVM == "provision":
                            if nameParamVM not in newVM[vmOrWinrm]:
                                newVM[vmOrWinrm][nameParamVM] = [paramVM]
                            else:
                                newVM[vmOrWinrm][nameParamVM].append(paramVM)
                        else:
                            newVM[vmOrWinrm][nameParamVM] = paramVM

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

    return jsonText


if __name__ == "__main__":
    vagrantFileName = "Saves/MODEL-VagrantFile"
    jsonFileName = "tmp/jsonfile.json"
    result1 = verifIndent(vagrantFileName)
    print("Vérification de l'indentation : ", result1)
    if result1 == True:
        jsonText = convertVAGRANTFILEtoJSON(vagrantFileName)
        # printJSON(jsonText)
        result2 = setJSON(jsonFileName, jsonText)
        print("Ecriture du fichier ",jsonFileName," : ", result2)

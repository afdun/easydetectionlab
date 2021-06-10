"""
This compiler converts a jsonFile to a VagrantFile.
"""

# IMPORT
import json


# FUNCTIONS
def getJSON(jsonFileName):
    """
    Function getting the content of a json file in a python json

    @param `jsonFileName`: name of the json file to get the content

    @return `jsonText`: json with the json content
    """
    with open(jsonFileName) as jsonFile:
        jsonText = json.load(jsonFile)
    return jsonText


def setVAGRANTFILE(vagrantFileName, vagrantText):
    """
    Function writing a vagrant text in a vagrant file

    @param `vagrantFileName`: name of the vagrant file to write to
    @param `vagrantText`: vagrant text to write in the vagrant file

    @return `vagrantFile.closed`: boolean (True if the vagrant file successfully closed else False)
    """
    with open(vagrantFileName,'w') as vagrantFile:
        vagrantFile.write(vagrantText)
    return vagrantFile.closed


def printJSON(jsonText):
    """
    Function printing a python json in the console (useful for debug, not production)

    @param `jsonText`: json text to print

    """
    print(json.dumps(jsonText,indent=2))



def convertJSONtoVAGRANTFILE(jsonFileName):
    """ Function converting a json file in vagrant text

    @param `jsonFileName`: name of the json file to convert to vagrant text

    @return `vagrantText`: string with the converted vagrant text
    """
    jsonText = getJSON(jsonFileName)
    vagrantText = ""
    if "intro" in jsonText:
        for line in jsonText["intro"]:
            vagrantText += line + "\n"
    vagrantText += "Vagrant.configure('2') do |config|\n"
    for nameVM, config in jsonText.items():
        if nameVM == "intro":
            continue
        
        vagrantText += "  config.vm.define {} do |cfg|\n".format(nameVM)
        for cfg,value in config.items():
            for vm,value2 in value.items():
                for setting,value3 in value2.items():
                    if setting == "provision":
                        for i in value3:
                            vagrantText += 4*' '+'.'.join((cfg,vm,setting))+' '+i+'\n'
                    elif setting == "vb":
                        for settingVB,value4 in value3.items():
                            if settingVB != "customize":
                                vagrantText += 6*' '+'.'.join((setting,settingVB))+' = '+value4+'\n'
                            else:
                                for i in value4:
                                    vagrantText += 6*' '+'.'.join((setting,settingVB))+' '+i+'\n'
                        vagrantText += 4*' '+"end\n"
                    elif setting == "provider":
                        vagrantText += 4*' '+'.'.join((cfg,vm,setting))+' '+value3+' do |vb, override|\n'
                    elif setting == "network":
                        vagrantText += 4*' '+'.'.join((cfg,vm,setting))+' '+value3+'\n'
                    else:
                        vagrantText += 4*' '+'.'.join((cfg,vm,setting))+' = '+value3+'\n'
        vagrantText += "  end\n"
        
    vagrantText += "end\n"
    return vagrantText

# MAIN
if __name__ == "__main__":
    jsonFileName = "Saves/DefaultInfrastructure.json" # Source file
    vagrantFileName = "tmp/Vagrantfile" # End file
    vagrantText = convertJSONtoVAGRANTFILE(jsonFileName) # Conversion of source file into vagrant
    # print(vagrantText) # For debug only
    result = setVAGRANTFILE(vagrantFileName, vagrantText) # Set the conversion result in the end file
    print("Ecriture du fichier ", vagrantFileName, " : ", result)

import json

dic = {
  "'logger'": {
    "cfg": {
        "vm":{
          "box": "'bento/ubuntu-18.04'",
          "hostname": "'logger'",
          "provision": [
            ":shell, path: 'logger_bootstrap.sh'",
          ],
          "network": [
            ":private_network, ip: '192.168.38.105', gateway: '192.168.38.1', dns: '8.8.8.8'"
          ],
          "provider": "'virtualbox'",
          "vb": {
            "gui": "true",
            "name": "'logger'",
            "customize": [
              "['modifyvm',:id,'--memory',1024]",
              "['modifyvm', :id, '--cpus', 1]",
              "['modifyvm', :id, '--vram', '32']",
              "['modifyvm', :id, '--nicpromisc2', 'allow-all']",
              "['modifyvm', :id, '--clipboard', 'bidirectional']",
              "['modifyvm', :id, '--natdnshostresolver1', 'on']",
              "['setextradata', 'global', 'GUI/SuppressMessages', 'all' ]",
            ]
          }
        }
      }
    },
    "'wef'": {
        "cfg": {
            "vm": {
                "box": "'detectionlab/win2016'",
                "hostname": "'wef'",
                "boot_timeout": "1000",
                "communicator": "'winrm'",
                "network": [
                    ":private_network, ip: '192.168.38.103', gateway: '192.168.38.1', dns: '192.168.38.102'"
                ],
                "provision": [
                    "'shell', path: 'scripts/fix-second-network.ps1', privileged: true, args: '-ip 192.168.38.103 -dns 8.8.8.8 -gateway 192.168.38.1'",
                    "'shell', path: 'scripts/provision.ps1', privileged: false",
                    "'reload'",
                    "'shell', path: 'scripts/provision.ps1', privileged: false",
                    "'shell', path: 'scripts/download_palantir_wef.ps1', privileged: false",
                    "'shell', inline: 'wevtutil el | Select-String -notmatch 'Microsoft-Windows-LiveId' | Foreach-Object {wevtutil cl '$_'}', privileged: false",
                    "'shell', path: 'scripts/install-wefsubscriptions.ps1', privileged: false",
                    "'shell', path: 'scripts/install-splunkuf.ps1', privileged: false",
                    "'shell', path: 'scripts/install-windows_ta.ps1', privileged: false",
                    "'shell', path: 'scripts/install-utilities.ps1', privileged: false",
                    "'shell', path: 'scripts/install-redteam.ps1', privileged: false",
                    "'shell', path: 'scripts/install-evtx-attack-samples.ps1', privileged: false",
                    "'shell', path: 'scripts/install-choco-extras.ps1', privileged: false",
                    "'shell', path: 'scripts/install-osquery.ps1', privileged: false",
                    "'shell', path: 'scripts/install-sysinternals.ps1', privileged: false",
                    "'shell', path: 'scripts/install-velociraptor.ps1', privileged: false",
                    "'shell', path: 'scripts/configure-pslogstranscriptsshare.ps1', privileged: false",
                    "'shell', path: 'scripts/install-autorunstowineventlog.ps1', privileged: false",
                    "'shell', inline: 'Set-SmbServerConfiguration -AuditSmb1Access $true -Force', privileged: false",
                    "'shell', path: 'scripts/install-microsoft-ata.ps1', privileged: false",
                    "'shell', inline: 'cscript c:\\windows\\system32\\slmgr.vbs /dlv', privileged: false"
                ],
                "provider": "'virtualbox'",
                "vb": {
                    "gui": "true",
                    "name": "'wef.windomain.local'",
                    "default_nic_type": "'82545EM'",
                    "customize": [
                        "['modifyvm', :id, '--memory', 2048]",
                        "['modifyvm', :id, '--cpus', 1]",
                        "['modifyvm', :id, '--vram', '32']",
                        "['modifyvm', :id, '--clipboard', 'bidirectional']",
                        "['modifyvm', :id, '--natdnshostresolver1', 'on']",
                        "['setextradata', 'global', 'GUI/SuppressMessages', 'all' ]"
                    ]
                }
            },
            "winrm": {
                "basic_auth_only": "true",
                "timeout": "300",
                "retry_limit": "20"
            }
        }
    }
}

"""
config.vm.define "wef" do |cfg|
cfg.vm.box = "detectionlab/win2016"
cfg.vm.hostname = "wef"
cfg.vm.boot_timeout = 1000
cfg.vm.communicator = "winrm"
cfg.winrm.basic_auth_only = true
cfg.winrm.timeout = 300
cfg.winrm.retry_limit = 20
cfg.vm.network :private_network, ip: "192.168.38.103", gateway: "192.168.38.1", dns: "192.168.38.102"

cfg.vm.provision "shell", path: "scripts/fix-second-network.ps1", privileged: true, args: "-ip 192.168.38.103 -dns 8.8.8.8 -gateway 192.168.38.1"
cfg.vm.provision "shell", path: "scripts/provision.ps1", privileged: false
cfg.vm.provision "reload"
cfg.vm.provision "shell", path: "scripts/provision.ps1", privileged: false
cfg.vm.provision "shell", path: "scripts/download_palantir_wef.ps1", privileged: false
cfg.vm.provision "shell", inline: 'wevtutil el | Select-String -notmatch "Microsoft-Windows-LiveId" | Foreach-Object {wevtutil cl "$_"}', privileged: false
cfg.vm.provision "shell", path: "scripts/install-wefsubscriptions.ps1", privileged: false
cfg.vm.provision "shell", path: "scripts/install-splunkuf.ps1", privileged: false
cfg.vm.provision "shell", path: "scripts/install-windows_ta.ps1", privileged: false
cfg.vm.provision "shell", path: "scripts/install-utilities.ps1", privileged: false
cfg.vm.provision "shell", path: "scripts/install-redteam.ps1", privileged: false
cfg.vm.provision "shell", path: "scripts/install-evtx-attack-samples.ps1", privileged: false
cfg.vm.provision "shell", path: "scripts/install-choco-extras.ps1", privileged: false
cfg.vm.provision "shell", path: "scripts/install-osquery.ps1", privileged: false
cfg.vm.provision "shell", path: "scripts/install-sysinternals.ps1", privileged: false
cfg.vm.provision "shell", path: "scripts/install-velociraptor.ps1", privileged: false
cfg.vm.provision "shell", path: "scripts/configure-pslogstranscriptsshare.ps1", privileged: false
cfg.vm.provision "shell", path: "scripts/install-autorunstowineventlog.ps1", privileged: false
cfg.vm.provision "shell", inline: "Set-SmbServerConfiguration -AuditSmb1Access $true -Force", privileged: false
cfg.vm.provision "shell", path: "scripts/install-microsoft-ata.ps1", privileged: false
cfg.vm.provision "shell", inline: 'cscript c:\windows\system32\slmgr.vbs /dlv', privileged: false



cfg.vm.provider "virtualbox" do |vb, override|
vb.gui = true
vb.name = "wef.windomain.local"
vb.default_nic_type = "82545EM"
vb.customize ["modifyvm", :id, "--memory", 2048]
vb.customize ["modifyvm", :id, "--cpus", 1]
vb.customize ["modifyvm", :id, "--vram", "32"]
vb.customize ["modifyvm", :id, "--clipboard", "bidirectional"]
vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
vb.customize ["setextradata", "global", "GUI/SuppressMessages", "all" ]
end
"""



def getJSON(fileName):
    with open(fileName) as jsonFile:
        infraJSON = json.load(jsonFile)
    return infraJSON

def setVAGRANTFILE(vagrantFileName, vagrantText):
    with open(vagrantFileName,'w') as vagrantFile:
        vagrantFile.write(vagrantText)
    return vagrantFile.closed

def printJSON(textJSON):
    print(json.dumps(textJSON,indent=2))

def configVM(name,config,vagrantFile):
    vagrantFile += "  config.vm.define {} do |cfg|\n".format(name)
    for cfg,value in config.items():
        for vm,value2 in value.items():
            for setting,value3 in value2.items():
                if setting == "provision" or setting == "network":
                    for i in value3:
                        vagrantFile += 4*' '+'.'.join((cfg,vm,setting))+' '+i+'\n'
                elif setting == "vb":
                    for settingVB,value4 in value3.items():
                        if settingVB != "customize":
                            vagrantFile += 6*' '+'.'.join((setting,settingVB))+' = '+value4+'\n'
                        else:
                            for i in value4:
                                vagrantFile += 6*' '+'.'.join((setting,settingVB))+' '+i+'\n'
                    vagrantFile += 4*' '+"end\n"
                elif setting == "provider":
                    vagrantFile += 4*' '+'.'.join((cfg,vm,setting))+' '+value3+' do |vb, override|\n'
                else:
                    vagrantFile += 4*' '+'.'.join((cfg,vm,setting))+' = '+value3+'\n'
    vagrantFile += "  end\n"
    return vagrantFile


"""
    Function that converts the JSON infrastructure in a VagrantFile
    @return result : boolean (True if successfully created VagrantFile, False else)
"""
def convertJSONtoVAGRANTFILE(jsonFile):
    vagrantFile = "Vagrant.configure('2') do |config|\n"
    infraJSON = getJSON('infra.json')
    for nameVM, config in infraJSON.items():
        vagrantFile = configVM(nameVM,config,vagrantFile)
    vagrantFile += "end\n"
    return vagrantFile

if __name__ == "__main__":
    # printJSON(dic)
    jsonFile = "infra.json"
    vagrantFileName = "VagrantFile"
    vagrantText = convertJSONtoVAGRANTFILE(jsonFile)
    print(vagrantText)
    result = setVAGRANTFILE(vagrantFileName, vagrantText)
    print("Ecriture du fichier ", vagrantFileName, " : ", result)

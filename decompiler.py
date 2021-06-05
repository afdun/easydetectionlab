import re
import json

def printJSON(JSONfile):
    print(json.dumps(JSONfile, indent=2))

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
                return "Vérification de l'indentation: échec. Issue line {}.".format(numberLine)
            previousIndent = newIndent
    return "Vérification de l'indentation: succès."


def decompile(file):
    with open(file,"r") as vagrantfile:
        JSONfile = {}
        indent = 0
        for line in vagrantfile:
            if not line.strip():
                continue
            # print(calcNumberIndent(line))
            # if line.startswith(" "*indent):
                # print("!!")
            # if not line.startswith(" "*indent):
                # numberIndent = calcNumberIndent(line)
                # print("numberIndent : ", numberIndent)
                # if numberIndent == indent-2 or numberIndent == indent+2:
                # indent = numberIndent
                # else:
                    # return "Erreur d'indentation dans le VagrantFile à transformer en JSON."
            indent = calcNumberIndent(line)
            # print(line, indent, line.startswith("config.vm.define",indent))
            if line.startswith("config.vm.define",indent):
                regex = re.compile("\s\".+\"\s")
                matchObject = regex.search(line)
                if matchObject:
                    nameVM = matchObject.group(0).strip()
                    # print(nameVM)
                    JSONfile[nameVM] = { "cfg" : {}}
                    newVM = JSONfile[nameVM]["cfg"]

            if line.startswith("cfg.vm.",indent):
                regex = re.compile("cfg\.vm\.(\w+)[\s\=]+(.+)")
                matchObject = regex.search(line)

                if matchObject:
                    nameParamVM = matchObject.group(1).strip()
                    paramVM = matchObject.group(2).strip()
                    # print(nameVM)
                    newVM[nameParamVM] = paramVM

    printJSON(JSONfile)
    return "Succès de la transformation du VagrantFile en JSON."

def test(file):
    with open(file,"r") as vagrantfile:
        st = vagrantfile.read().split("  config.")
        n = 0
        for i in st:
            st[n] = i.split("  cfg.")
            n += 1
    print(st)

if __name__ == "__main__":
    # res = verifIndent("TEMP-vagrantfile")
    # print(res)
    result = decompile("TEMP-vagrantfile")
    print(result)
    # test("TEMP-vagrantfile")



"""
a = "config.vm.define 'wef' do |cfg|
  cfg.vm.box = 'detectionlab/win2016'
  cfg.vm.hostname = 'wef'
  cfg.vm.boot_timeout = 1000
  cfg.vm.communicator = 'winrm'
  cfg.winrm.basic_auth_only = true
  cfg.winrm.timeout = 300
  cfg.winrm.retry_limit = 20
  cfg.vm.network :private_network, ip: '192.168.38.103', gateway: '192.168.38.1', dns: '192.168.38.102'

  cfg.vm.provision 'shell', path: 'scripts/fix-second-network.ps1', privileged: true, args: '-ip 192.168.38.103 -dns 8.8.8.8 -gateway 192.168.38.1'
  cfg.vm.provision 'shell', path: 'scripts/provision.ps1', privileged: false
  cfg.vm.provision 'reload'
  cfg.vm.provision 'shell', path: 'scripts/provision.ps1', privileged: false
  cfg.vm.provision 'shell', path: 'scripts/download_palantir_wef.ps1', privileged: false
  cfg.vm.provision 'shell', inline: 'wevtutil el | Select-String -notmatch 'Microsoft-Windows-LiveId' | Foreach-Object {wevtutil cl '$_'}', privileged: false
  cfg.vm.provision 'shell', path: 'scripts/install-wefsubscriptions.ps1', privileged: false
  cfg.vm.provision 'shell', path: 'scripts/install-splunkuf.ps1', privileged: false
  cfg.vm.provision 'shell', path: 'scripts/install-windows_ta.ps1', privileged: false
  cfg.vm.provision 'shell', path: 'scripts/install-utilities.ps1', privileged: false
  cfg.vm.provision 'shell', path: 'scripts/install-redteam.ps1', privileged: false
  cfg.vm.provision 'shell', path: 'scripts/install-evtx-attack-samples.ps1', privileged: false
  cfg.vm.provision 'shell', path: 'scripts/install-choco-extras.ps1', privileged: false
  cfg.vm.provision 'shell', path: 'scripts/install-osquery.ps1', privileged: false
  cfg.vm.provision 'shell', path: 'scripts/install-sysinternals.ps1', privileged: false
  cfg.vm.provision 'shell', path: 'scripts/install-velociraptor.ps1', privileged: false
  cfg.vm.provision 'shell', path: 'scripts/configure-pslogstranscriptsshare.ps1', privileged: false
  cfg.vm.provision 'shell', path: 'scripts/install-autorunstowineventlog.ps1', privileged: false
  cfg.vm.provision 'shell', inline: 'Set-SmbServerConfiguration -AuditSmb1Access $true -Force', privileged: false
  cfg.vm.provision 'shell', path: 'scripts/install-microsoft-ata.ps1', privileged: false
  cfg.vm.provision 'shell', inline: 'cscript c:\windows\system32\slmgr.vbs /dlv', privileged: false



  cfg.vm.provider 'virtualbox' do |vb, override|
    vb.gui = true
    vb.name = 'wef.windomain.local'
    vb.default_nic_type = '82545EM'
    vb.customize ['modifyvm', :id, '--memory', 2048]
    vb.customize ['modifyvm', :id, '--cpus', 1]
    vb.customize ['modifyvm', :id, '--vram', '32']
    vb.customize ['modifyvm', :id, '--clipboard', 'bidirectional']
    vb.customize ['modifyvm', :id, '--natdnshostresolver1', 'on']
    vb.customize ['setextradata', 'global', 'GUI/SuppressMessages', 'all' ]
  end"

  print(a)
"""

dic = {
"logger": {
"cfg": {
  "box": "bento/ubuntu-18.04",
  "hostname": "logger",
  "provision": [("shell", "logger_bootstrap.sh")],
  "network": [(":private_network"), ("ip", "192.168.38.105"), ("gateway","192.168.38.1"), ("dns","8.8.8.8")],
  "provider": "virtualbox",
  "vb": {
  "gui": "true",
  "name": "logger",
  "customize": [["modifyvm", ":id", "--memory", 1024],
  ["modifyvm", ":id", "--cpus", 1],
  ["modifyvm", ":id", "--vram", "32"],
  ["modifyvm", ":id", "--nicpromisc2", "allow-all"],
  ["modifyvm", ":id", "--clipboard", "bidirectional"],
  ["modifyvm", ":id", "--natdnshostresolver1", "on"],
  ["setextradata", "global", "GUI/SuppressMessages", "all" ]]
  }
}
}
}

print(dic)

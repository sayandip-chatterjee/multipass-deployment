# 🚀 Multipass VM Setup Script

This script automates the installation and configuration of
[Multipass](https://multipass.run) and makes it easier to launch Ubuntu
VMs with customizable resources and networking.

------------------------------------------------------------------------

## 📑 Table of Contents

- [🔍 Features](#-features)
- [⚙️ Prerequisites](#️-prerequisites)
- [📦 Installation & Usage](#-installation--usage)
- [🌐 Networking Configurations](#-networking-configurations)
- [Cloud Init YAML](#-cloud-init-yaml)

------------------------------------------------------------------------

## 🔍 Features

-   ✅ Automatically installs **Multipass** if not found
    (Windows/Linux).
-   ✅ Interactive prompts for **CPU, memory, disk** configuration.
-   ✅ Manual Options to use **default NAT** or **bridged networking** with **single/multiple NICs** or **customised network configuration**.
-   ✅ Simple progress messages and interactive flow.

------------------------------------------------------------------------

## ⚙️ Prerequisites

- OS : Ubuntu (tested on **22.04+**) _or_ Windows (tested on **Windows11**)
- Interpreter/Runtime : **Python 3.8+** (MUST be installed in the system)
- Internet connection (to fetch Multipass if not installed).

------------------------------------------------------------------------

## 📦 Installation & Usage

[LINUX] Clone the repository and run the setup script:
```bash
git clone https://github.com/sayandip-chatterjee/multipass-deployment.git
cd multipass-deployment/
python3 setup_multipass.py
```
    
[WINDOWS] Ensure all the steps are done as mentioed:
```bash
In the Windows machine BIOS setup, make sure that virtualization is turned on

Install git bash - https://git-scm.com/downloads/win and close the git bash window, do not clone yet.

Install python3.8 from Microsoft Store

Go to Windows Features from the Start Menu -> Search and make sure You enable the
"HyperV", "Virtual Machine Platform", and the "Windows Hypervisor Platform" to run the VM.

Restart the machine.

Open powershell (NOT AS Administrator)

git clone https://github.com/sayandip-chatterjee/multipass-deployment.git
cd multipass-deployment/
python3 setup_multipass.py
```

## 🌐 Networking Configurations

In Multipass, if you don’t specify a network (--network), the VM is attached to the default NAT network that Multipass creates.
NOTE : I found using cloud-init.yaml approach is better than manual commands below.

```bash
multipass launch --help
...
--network <spec>    Add a network interface to the instance, where <spec> is in the "key=value,key=value" format,
                    --network name=mpqemubr0,mode=manual,mac=xx:xx:xx:xx:xx:xx
                    with the following keys available:
                        name: the network to connect to (required), use the `multipass networks` command for 
                              a list of possible values, or use 'bridged' to use the interface configured via 
                             `multipass set local.bridged-network`.
                        mode: auto|manual (default: auto)
                        mac: hardware address (default: random).
--bridged           Adds one `--network bridged` network.
...

[For multiple NICs]

multipass launch --name testvm ... 
  --network name=eth0,mode=bridged,mac=52:54:00:aa:bb:cc 
  --network name=default,mode=nat
```

Multipass networking capabilities may vary by OS and backend.

### 1. NAT (default)

-   VM gets a private IP in a Multipass-managed NAT.
-   Outbound internet works.
-   Only accessible from host via `multipass shell` or
    `multipass exec`.
-   Other devices on your LAN cannot reach it.

### 2. Bridged

-   VM is attached to a host network adapter (e.g., `eth0`, `wlp2s0`).
-   VM gets an IP from your LAN, just like a physical machine.
-   Accessible directly from other devices on the LAN.
-   Requires choosing a valid adapter from `multipass networks`.

------------------------------------------------------------------------

## Cloud Init YAML

```bash
multipass launch 22.04 --name testvm --cloud-init cloud-init.yaml
```

Explanation of Sections

- hostname/locale/timezone → Sets identity of the VM.
- users → Creates a devuser with sudo, SSH key, and password login enabled.
- network → Example static IP config (you can remove for DHCP).
- package_update/upgrade → Updates and installs useful packages (Docker, Python, Node.js).
- apt sources → Adds a custom repo (Docker in this case).
- write_files → Writes files inside VM (motd, aliases).
- runcmd → Commands executed at first boot.
- final_message → Prints a friendly message after cloud-init finishes.

------------------------------------------------------------------------

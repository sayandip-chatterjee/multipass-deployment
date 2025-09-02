# Multipass VM Setup Script

This script automates the installation and configuration of
[Multipass](https://multipass.run) and makes it easier to launch Ubuntu
VMs with customizable resources and networking.

------------------------------------------------------------------------

## Features

-   ✅ Automatically installs **Multipass** if not found
    (Windows/Linux).
-   ✅ Interactive prompts for **CPU, memory, disk** configuration.
-   ✅ Option to use **default NAT** or **bridged networking** or customised network configuration.
-   ✅ Simple progress messages and interactive flow.

------------------------------------------------------------------------

## Prerequisites

-   **Windows 10/11** with Hyper-V enabled (or WSL for basic checks, but
    not recommended).\
-   **Linux** with `snapd` available.\
-   Internet connection (to fetch Multipass if not installed).

------------------------------------------------------------------------

## Networking Modes

The script allows you to choose between two networking modes:

### 1. NAT (default)

-   VM gets a private IP in a Multipass-managed NAT.\
-   Outbound internet works.\
-   Only accessible from host via `multipass shell` or
    `multipass exec`.\
-   Other devices on your LAN cannot reach it.

### 2. Bridged

-   VM is attached to a host network adapter (e.g., `eth0`, `wlp2s0`).\
-   VM gets an IP from your LAN, just like a physical machine.\
-   Accessible directly from other devices on the LAN.\
-   Requires choosing a valid adapter from `multipass networks`.

------------------------------------------------------------------------

## Usage

1.  Clone or download this script.\

2.  Make it executable:

    ``` bash
    chmod +x multipass_setup.py
    ```

3.  Run it:

    ``` bash
    ./multipass_setup.py
    ```

4.  Follow the interactive prompts:

    -   Enter a **VM name**.\
    -   Choose between **default config** or **custom config**.\
    -   If custom, set CPUs, memory, disk, and networking mode (NAT or
        Bridged).

------------------------------------------------------------------------

## Example Run

    $ ./multipass_setup.py

    Disclaimer: Deactivate any SECURED network before proceeding...
    Press ENTER to continue...

    Please type a unique name for your VM instance: test-vm

    Would you like to use default configuration? (2 CPU, 4G RAM, 20G Disk, default network)
    Type 'yes' to use defaults, or 'no' to customize: no

    Enter number of CPUs [default 2]: 4
    Enter memory (e.g., 4G) [default 4G]: 8G
    Enter disk size (e.g., 20G) [default 20G]: 40G

    Choose networking mode:
    1. NAT (default) - VM will use Multipass-managed NAT (isolated).
    2. Bridged      - VM will be directly attached to your LAN adapter.

    Enter choice [1/2, default 1]: 2

    [+] Available host adapters for bridging:
    Name      Type       Description
    eth0      ethernet   Intel(R) Ethernet Connection
    wlp2s0    wifi       Intel(R) Wireless-AC 9560

    Enter adapter name to bridge (e.g., eth0, wlp2s0): eth0

The script then launches your VM with the specified configuration.

------------------------------------------------------------------------

## Notes

-   NAT mode is simpler and always works.\
-   Bridged mode requires a supported physical adapter.\
-   Multipass networking capabilities may vary by OS and backend.

# Getting Started with PiDNS

PiDNS bundles a lightweight Flask dashboard with DNS and DHCP services that run well on Raspberry Pi hardware and other low-resource systems. Follow the steps below to install the project and explore the dashboard before deploying it to a dedicated device.

## 1. Prepare Your Host System

Ensure the host has Python 3.8 or newer plus the tooling needed to create a virtual environment:

```bash
sudo apt update && sudo apt install python3 python3-venv git -y
```

These packages provide the interpreter, virtual environment support, and Git so you can clone the repository.

## 2. Clone the Repository

Download PiDNS and change into the project directory:

```bash
git clone https://github.com/yourusername/PiDNS.git
cd PiDNS
```

## 3. Configure Secure Dashboard Credentials

PiDNS requires strong dashboard credentials before it will launch. Set them as environment variables so the dashboard can read them at startup:

```bash
export PIDNS_USERNAME="choose-a-unique-username"
export PIDNS_PASSWORD="use-a-strong-password-with-12+-characters"
```

Store these values securely if you need them to persist across reboots (for example in `/etc/environment`).

## 4. Create a Virtual Environment and Install Dependencies

Run the dashboard inside a Python virtual environment to isolate dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 5. Launch the Dashboard

Start the Flask application:

```bash
python app/app.py
```

By default the web UI is available at `http://<host-ip>:8080`. Sign in with the credentials you exported earlier to reach the overview, device list, and other dashboard pages.

## 6. Optional: Use the Silent Installer

If you prefer an automated setup, PiDNS ships with a silent installer script that accepts device and container targets:

```bash
./scripts/install.sh --device pi-4 --container docker --silent
```

Consult the script's help output for additional options tailored to different hardware or container runtimes.

## Trying PiDNS Before Using Real Hardware

PiDNS does not provide a hosted demo environment, but you can test it without touching production devices:

- **Run locally on a PC or laptop.** The dashboard and supporting services run on Linux desktops or servers with modest resources, so you can experiment on your workstation before migrating to a Raspberry Pi.
- **Use a container runtime.** Docker, Podman, and LXC are first-class deployment targets; running PiDNS in a container lets you validate configuration changes in an isolated environment.
- **Virtual machines or cloud instances.** Any VM with Python 3.8+ can host the application for evaluation as long as you can forward port 8080 to your browser.

Once you are satisfied with the configuration, move the same setup to your Raspberry Pi or other network appliance.

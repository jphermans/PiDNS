# PiDNS 🔐📡

<p align="center">
  <img src="app/static/images/pidns-logo.svg" alt="PiDNS Logo" width="220" />
</p>

<p align="center">
  <em>Secure, lightweight DNS and DHCP services with a friendly dashboard for Raspberry Pi and beyond.</em>
</p>

<p align="center">
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.8%2B-blue.svg" alt="Python 3.8+"></a>
  <a href="https://www.docker.com/"><img src="https://img.shields.io/badge/docker-ready-0d6efd.svg" alt="Docker Ready"></a>
  <a href="https://podman.io/"><img src="https://img.shields.io/badge/podman-ready-6f42c1.svg" alt="Podman Ready"></a>
  <a href="https://linuxcontainers.org/"><img src="https://img.shields.io/badge/lxc-ready-20c997.svg" alt="LXC Ready"></a>
</p>

---

## 🌈 Overview

PiDNS is a vibrant yet low-footprint DNS and DHCP server toolkit designed with the Raspberry Pi Zero 2 W in mind. The bundled Flask dashboard delivers real-time visibility into your network, optional ad blocking, and easy integration with containerized environments.

## ✨ Features

- 🛡️ **Secure Dashboard** – Password-protected interface with enforced strong credentials.
- 📊 **Live Device Monitoring** – Real-time device list with vendor lookup and connection details.
- 🧠 **Smart Caching** – Lightweight parsing of `dnsmasq` leases for speedy updates.
- 📦 **Container Friendly** – First-class support for Docker, Podman, and LXC deployments.
- 🧽 **Ad-blocking Ready** – Integrate with your preferred blocklists to keep the web clean.
- ⚙️ **Resource Tuned** – Crafted for low-memory boards yet scalable to larger systems.

## 🧭 Supported Hardware

| Device | Recommended Specs |
| ------ | ----------------- |
| 🍓 Raspberry Pi Zero W | 512 MB RAM · 1 core |
| 🍓 Raspberry Pi Zero 2 W | 512 MB RAM · 1 core |
| 🍓 Raspberry Pi 3 | 1 GB RAM · 4 cores |
| 🍓 Raspberry Pi 4 | 2–8 GB RAM · 4 cores |
| 🍓 Raspberry Pi 5 | 4–8 GB RAM · 4 cores |
| 💻 Low-resource PC | ≤1 GB RAM · ≤2 cores |
| 🖥️ Standard PC | >1 GB RAM · >2 cores |

## 🚀 Quick Start

### 1. Prepare the Environment

```bash
sudo apt update && sudo apt install python3 python3-venv git -y
```

### 2. Clone the Repository

```bash
git clone https://github.com/yourusername/PiDNS.git
cd PiDNS
```

### 3. Configure Secure Credentials ✅

Set **strong** dashboard credentials before launching PiDNS. Weak defaults are blocked to keep your network safe.

```bash
export PIDNS_USERNAME="choose-a-unique-username"
export PIDNS_PASSWORD="use-a-strong-password-with-12+-characters"
```

> 💡 **Tip:** Store these values securely (for example, in `/etc/environment` or a systemd override file) so they persist across reboots.

### 4. Launch the Dashboard

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app/app.py
```

The dashboard is now available at **http://<host-ip>:8080**. Log in with the credentials you configured in the previous step.

## 🤖 Optional: Silent Installer

Automate setup with the bundled script:

```bash
./scripts/install.sh --device pi-4 --container docker --silent
```

## 🖼️ Dashboard Preview

| Overview | Device List |
| -------- | ----------- |
| ![Dashboard Overview](https://github.com/yourusername/PiDNS/raw/main/docs/screenshots/dashboard.png) | ![Device Details](https://github.com/yourusername/PiDNS/raw/main/docs/screenshots/device-details.png) |

## 📚 Documentation & Support

- 📘 [Comprehensive documentation](comprehensive_documentation.md)
- 🛠️ [Installation script reference](installation_script_modification_plan.md)
- 🧪 [Testing plan](testing_plan.md)
- 💬 [GitHub Discussions](https://github.com/yourusername/PiDNS/discussions)
- 🐞 [Issue tracker](https://github.com/yourusername/PiDNS/issues)

## 🤝 Contributing

Contributions are welcome! Please review the guidelines in `CONTRIBUTING.md` (coming soon) and open pull requests for enhancements or fixes.

## 🙌 Acknowledgements

- 🧭 [dnsmasq](http://www.thekelleys.org.uk/dnsmasq/doc.html) for the DNS/DHCP engine
- 🌐 [Flask](https://flask.palletsprojects.com/) for the web framework
- 🎨 [Bootstrap](https://getbootstrap.com/) for design inspiration
- 🧩 The Raspberry Pi Foundation for the hardware we love

## ⚖️ License

Released under the [MIT License](LICENSE). Enjoy and stay secure! 🔐

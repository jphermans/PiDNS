# PiDNS - Lightweight DNS and DHCP Server for Raspberry Pi

![PiDNS Logo](https://github.com/yourusername/PiDNS/raw/main/docs/images/pidns-logo.png)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![Podman](https://img.shields.io/badge/podman-ready-blue.svg)](https://podman.io/)
[![LXC](https://img.shields.io/badge/lxc-ready-blue.svg)](https://linuxcontainers.org/)

PiDNS is a lightweight, easy-to-use DNS and DHCP server solution designed for Raspberry Pi and other low-resource devices. It provides a web-based dashboard for monitoring and managing network devices, with support for ad-blocking capabilities.

## Features

- **DNS and DHCP Server**: Provides DNS and DHCP services for local networks
- **Web Dashboard**: User-friendly web interface for monitoring and management
- **Device Monitoring**: Real-time monitoring of connected devices
- **Ad-blocking**: Built-in ad-blocking capabilities
- **Container Support**: Support for Docker, Podman, and LXC containers
- **Multi-Device Support**: Optimized for various Raspberry Pi models and PCs
- **Resource Optimization**: Configurable resource usage based on device capabilities

## Supported Devices

- **Raspberry Pi Zero W** (512MB RAM, 1-core CPU)
- **Raspberry Pi Zero 2W** (512MB RAM, 1-core CPU)
- **Raspberry Pi 3** (1GB RAM, 4-core CPU)
- **Raspberry Pi 4** (2-8GB RAM, 4-core CPU)
- **Raspberry Pi 5** (4-8GB RAM, 4-core CPU)
- **Low-Resource PC** (≤1GB RAM, ≤2 cores)
- **Standard PC** (>1GB RAM, >2 cores)

## Supported Container Runtimes

- **Docker**: Most popular container platform with wide community support
- **Podman**: Daemonless, rootless containers with better security
- **LXC**: Lightweight OS-level virtualization with better performance
- **None**: Install directly on the host system without containers

## Quick Start

### Prerequisites

- Raspberry Pi OS (formerly Raspbian) or Debian-based Linux distribution
- Python 3.7 or higher
- Minimum 512MB RAM (1GB recommended)
- Minimum 4GB free storage (8GB recommended)
- Ethernet or Wi-Fi connection

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/PiDNS.git
   cd PiDNS
   ```

2. **Run the installation script**
   ```bash
   ./scripts/install.sh
   ```

3. **Follow the prompts**
   - Select your device type
   - Select your container type
   - Confirm the installation

4. **Access the dashboard**
   - Open a web browser and navigate to `http://<pi-ip-address>:8080`
   - Log in with the default username `admin` and password `password`
   - Change the default password after logging in

### Silent Installation

For automated installations, you can use the silent mode:

```bash
./scripts/install.sh --device pi-4 --container docker --silent
```

## Screenshots

### Dashboard
![Dashboard](https://github.com/yourusername/PiDNS/raw/main/docs/screenshots/dashboard.png)

### Device Details
![Device Details](https://github.com/yourusername/PiDNS/raw/main/docs/screenshots/device-details.png)

### Ad-blocking
![Ad-blocking](https://github.com/yourusername/PiDNS/raw/main/docs/screenshots/ad-blocking.png)

## Documentation

For detailed documentation, please see the [comprehensive documentation](comprehensive_documentation.md).

## Contributing

We welcome contributions! Please see our [contributing guidelines](CONTRIBUTING.md) for details.

## License

PiDNS is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support

- **Documentation**: [comprehensive documentation](comprehensive_documentation.md)
- **Issues**: [GitHub Issues](https://github.com/yourusername/PiDNS/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/PiDNS/discussions)
- **Community Forum**: [PiDNS Community Forum](https://forum.pidns.org/)

## Acknowledgments

- [dnsmasq](http://www.thekelleys.org.uk/dnsmasq/doc.html) for providing the DNS and DHCP server
- [Flask](https://flask.palletsprojects.com/) for providing the web framework
- [Bootstrap](https://getbootstrap.com/) for providing the UI framework
- [jQuery](https://jquery.com/) for providing the JavaScript library
- The Raspberry Pi Foundation for creating the Raspberry Pi
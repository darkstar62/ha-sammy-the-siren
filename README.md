# Sammy the Siren for Home Assistant
[![](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![](https://img.shields.io/badge/HACS-Default-yellow.svg)](https://hacs.xyz/)

![Repo Logo](https://raw.githubusercontent.com/darkstar62/ha-sammy-the-siren/main/assets/sammy_the_siren.png)

A Home Assistant integration for controlling 3D printed air-raid sirens
using the custom [Siren](https://github.com/darkstar62/siren) firmware
through its RESTful API.

This is a first release and bound to have rough edges!  Feedback and contributions are greatly
appreciated. If you find this project useful, consider giving it a ⭐star to show your support!

## Installation

Home Assistant Core must be newer than version `2026.2.0`.

Choose your preferred installation method, and reboot Home Assistant afterward.

### Method 1: Through HACS

Navigate to "HACS" > "Sammy the Siren" or use the My button below.

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=darkstar62&repository=ha-sammy-the-siren&category=integration)

### Method 2: Manually

Download the repo and copy the folder `/custom_components/sammy_the_siren` into
your Home Assistant's `/config/custom_components` directory.

## Configuration

You nees the hostname of your siren controller.  The port is 12346 unless you've
chamged it by hand.

To add the integration, navigate to "Settings"  > "Devices & services"  > "Add integration"  > "Sammy
the Siren" or use the My button below. Then, follow the config flow.

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=sammy_the_siren)

Notes:
1. If you can't find it in the integration list, make sure you've successfully installed the integration and rebooted. If so, try clearing the browser cache.
2. If your API location is an IP address, make sure it's static or assign a static DHCP lease for it. Location changes will require you to re-add the integration.
3. This integration omly supports http.

## Usage

Upon successful configuration, you'll get one 'Siren' entity which can be used to:

 - turn the siren on and off (default tone is 'alert')
 - select different tones depending on siren capabilities
 - aet a tone for a duration.

## Feedback
To report an issue, please include details about your siren configuration, along with
debug logs of this integration.  You can enable debug logging in the UI (if possible)
or add the following to your Home Assistant configuration:
```
logger:
  default: warning
  logs:
    custom_components.sammy_the_siren: debug
    custom_components.sammy_the_siren.siren: debug
```

## Disclaimer

This integration is solely for controlling 3D-printed air-raid sirens and is not responsible for any actions taken by users while using such sirens. The user is fully responsible for ensuring that their use of the siren complies with all applicable laws and regulations.  Neither the owner nor the contributors to this repository make any warranties regarding the accuracy, legality, or appropriateness of the siren or its use.

By using this integration, you acknowledge and agree to this disclaimer.

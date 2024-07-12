[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![Community Support](https://badgen.net/badge/support/community/cyan?icon=awesome)](https://github.com/nginxinc/mtbChef/GitOps-NMS/blob/main/SUPPORT.md)
<!-- [![Commercial Support](https://badgen.net/badge/support/commercial/cyan?icon=awesome)](<Insert URL>) -->

# Demo: Managing NGINX with NGINX One using GitOps
This repository provides a sample Github Actions script that allows NGINX One users to manage versioning and deployment of NGINX configurations via Github actions.

## NGINX Configurations
Configuration files are stored for each instance in this repository file structure.  See ```app-nyc-01``` for sample NGINX configurations found in nginx.conf

## Github Actions
The repository is configured to run the ```GitOps-NMS/.github/workflows/push-to-n1sc.yml``` Github Action on any commit and pull-request merge to the main branch. The script works by:

- Defining configuration files for a given instance in the repository
- Encoding configuration files to base64
- Pulling values from repository configuration variables (see table below)
- Generating a timestamp
- Incorporating all of these elements and sending an API call to the NGINX Management Suite instance accessible via the internet

### Github Action Configuration Variables
The ```push-to-nms.yml``` Github Action can be configured by changing the  variables within the Github Repository Settings:

## License

[Apache License, Version 2.0](https://github.com/mtbChef/GitOps-NMS/blob/main/LICENSE)

&copy; [F5, Inc.](https://www.f5.com/) 2023

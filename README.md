[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![Community Support](https://badgen.net/badge/support/community/cyan?icon=awesome)](https://github.com/nginxinc/mtbChef/GitOps-NMS/blob/main/SUPPORT.md)
<!-- [![Commercial Support](https://badgen.net/badge/support/commercial/cyan?icon=awesome)](<Insert URL>) -->

# Demo: Managing NGINX with NGINX One using GitOps
This repository provides a sample Github Actions script that allows NGINX One users to manage versioning and deployment of NGINX configurations via Github actions.

## TLDR;
1. Set your F5 Distributed Cloud bearer token in the Actions secrets
2. Using NGINX One Cloud Console, note your instance_id in the details, and note the first few lines of the nginx.conf file.
3. Set your N1SC_INSTANCE in the Actions Variables to be your instance_id, for example inst_23xYZTyZSpqa5UNi-eFcyw
4. Set your N1SC_HOSTNAME the Actions variables, for example nginxone-team.staging.volterra.us 
6. In this repo, edit app-nyc-01/etc/nginx/nginx.conf and add a comment near the top, and commit. 
7. That will trigger the actions workflow, you can go and view this running under Actions
8. Repeat step 2, and note the comment at the top of the file indicating the nginx.conf file has been updated by this project.
   

## NGINX Configurations
Configuration files are stored for each instance in this repository file structure.  See ```app-nyc-01``` for sample NGINX configurations found in nginx.conf

## Github Actions
The repository is configured to run the ```GitOps-NMS/.github/workflows/push-to-n1sc.yml``` Github Action on any commit and pull-request merge to the main branch. The script works by:

- Defining configuration files for a given instance in the repository
- Encoding configuration files to base64
- Pulling values from repository configuration variables (see table below)
- Generating a timestamp
- Incorporating all of these elements and sending an API call to the NGINX Management Suite instance accessible via the internet

## License

[Apache License, Version 2.0](https://github.com/mtbChef/GitOps-NMS/blob/main/LICENSE)

&copy; [F5, Inc.](https://www.f5.com/) 2023

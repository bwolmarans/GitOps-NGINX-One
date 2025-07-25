[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![Community Support](https://badgen.net/badge/support/community/cyan?icon=awesome)](https://github.com/nginxinc/mtbChef/GitOps-NMS/blob/main/SUPPORT.md)
<!-- [![Commercial Support](https://badgen.net/badge/support/commercial/cyan?icon=awesome)](<Insert URL>) -->

# Example of using the NGINX One Console REST API 
This repository provides an example in Python of using the NGINX One Console API. There is a Github Actions script that pulls parameteres from this repository, including an nginx.conf config file, and passes those to the Python script, but the Python script is not tightly coupled to this and the Python script has no dependency on Github Actions and therefore can be taken and run outside of Github.

## Python Script

The Python script is named nginx_one_console_api_python_example.py and expects some command-line parameters passed in such as namespace, tenant, and a few more.
It can be run outside of this repository.
Use -h or --help to see the usage.
The python script does the following:

- Accepts the parameters
- Locates the nginx instance ID based on the nginx instance hostname provided by doing an API call to the NGINX One Console to get a list of all instances, finding the hostname, and matching that to the instance ID
- Does a patch using nginx.conf which is passed in base64'd as a parameter
- Checks for success of the publication


## TLDR;
1. Set your F5 Distributed Cloud API token in the Actions secrets as XC_API_TOKEN
2. Using NGINX One Cloud Console, note your NGINX instance hostname
3. Set your N1C_TENANT_FQDN, NGINX_INSTANCE_HOSTNAME, and your N1C_NAMESPACE in the Actions variables, for example nginxone-team.staging.volterra.us as the tenant fqdn.
6. Clone the repo, and make a change to app-nyc-02/etc/nginx/nginx.conf and add a comment near the top, and commit. 
7. That will trigger the actions workflow, you can go and view this running under Actions
  

## NGINX Configurations
Configuration files are stored for each instance in this repository file structure.  See ```app-nyc-02``` for sample NGINX configurations found in nginx.conf

## Github Actions
The repository is configured to run the ```GitOps-NMS/.github/workflows/n1c_config_update_gitops_example.yml``` Github Action on push to the main branch. The script works by:

- Defining configuration files for a given instance in the repository
- Encoding configuration files to base64
- Pulling values from repository configuration variables (see table below)
- Generating a timestamp
- Incorporating all of these elements and sending these as parameters to the Python script


## License

[Apache License, Version 2.0](https://github.com/mtbChef/GitOps-NMS/blob/main/LICENSE)

&copy; [F5, Inc.](https://www.f5.com/) 2023

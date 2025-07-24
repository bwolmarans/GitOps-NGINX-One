# NGINX One Console API Example
# -----------------------------
# This script demonstrates how to interact with the NGINX One Console API to update the NGINX configuration.
# It includes functions to list instances, patch the NGINX configuration, get the current configuration,
# and check the status of a publication.    
# This script is intended to be run in a GitOps context, where it can be triggered by changes in a Git repository.
# This is only intended to patch /etc/nginx/nginx.conf, but can be extended to patch other files.
# This uses command line parameters to pass in the NGINX One Console hostname, namespace, instance ID, API token, and the base64 encoded NGINX configuration file.
# use --help to get the command line options.
#

import requests
import argparse
import json
import sys
from time import sleep 

def n1c_response_error_check(response_text):
    if "credential invalid" in response_text:
        print("ERROR: your API Authentication failed.  Check that your XC authentication token is")
        print("       the right one for your NGINX One Console Tenant")
        print("----------------------------------------------------------------------------------")
        print(response_text)
        sys.exit(2) 

def n1c_list_instances(api_base_path, headers):
    try:
        response = requests.get(api_base_path + "/instances", headers=headers)
        response_text = response.text
        n1c_response_error_check(response_text)
        return response_text
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)

def n1c_find_instance_by_hostname(nginx_instance_list, nginx_instance_hostname):
    try:
        instances = json.loads(nginx_instance_list)
        for instance in instances['items']:
            if instance['hostname'] == nginx_instance_hostname:
                return instance['object_id']
        print(f"Instance with hostname {nginx_instance_hostname} not found.")
        sys.exit(3)
    except json.JSONDecodeError as e:
        print("Error decoding JSON response:", e)
        sys.exit(1)
    except KeyError as e:
        print("Key error:", e)
        sys.exit(1)

def n1c_patch_nginx_config(api_base_path, headers, nginx_instance_id, payload):
    try:
        response = requests.patch(api_base_path + "/instances/" + nginx_instance_id + "/config" , headers=headers, json=payload)
        if response.status_code >= 200 and response.status_code < 300:
            response_text = response.text
            n1c_response_error_check(response_text)
            data = json.loads(response_text)
            publication_id = data['object_id']
            publication_status = data['status']
            return publication_id

        else:
            print(f"Something unexpected happened. The patch has probably failed. HTTP Status Code: {response.status_code}")
            print("Response:", response.text)

    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)

def n1c_get_nginx_config(api_base_path, headers, nginx_instance_id):
    try:
        response = requests.get(api_base_path + "/instances/" + nginx_instance_id + "/config" , headers=headers)
        response_text = response.text
        n1c_response_error_check(response_text)
        return response.text
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)

def n1c_check_publication_status(api_base_path, headers, nginx_instance_id, publication_id):
    try:
        response = requests.get(api_base_path + "/instances/" + nginx_instance_id + "/publications/" + publication_id, headers=headers)
        if response.status_code >= 200 and response.status_code < 300:
            response_text = response.text
            n1c_response_error_check(response_text)
            data = json.loads(response_text)
            if data['status'] == "succeeded":
                return "succeeded"
            elif data['status'] == "failed":
                x = "failed for the reason: " + data['status_cause']['message']
                return x
            elif data['status'] == "pending": 
                return "pending"
        else:
            print(f"Something unexpected happened. HTTP Status Code: {response.status_code}")
            print("Response:", response.text)

    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Python example for using the NGINX One Console Rest API')
    parser.add_argument('--n1c_tenant_fqdn', help='The F5 Distribted Cloud Tenant FQDN', default='nginx-tenant1.staging.volterra.us')
    parser.add_argument('--n1c_namespace', help="The F5 Distribted Cloud n1c_namespace within your tenant", default='default')
    parser.add_argument('--nginx_instance_id', help='The nginx instance uid from NGINX One Console. Not needed if nginx instance hostname specified.', default='your NGINX instance ID here')
    parser.add_argument('--xc_api_token', help='The F5 Distribted Cloud API Token', default='your XC API Token here')
    parser.add_argument('--nginx_config_file', help='The /etc/nginx/nginx.conf file, base64d', default='your base64d nginx config here')  
    parser.add_argument('--nginx_instance_hostname', help='The hostname of the NGINX instance.  If not provided will attempt to use nginx instance id.', default='nothing here, use the instance id')
    args = parser.parse_args()

    n1c_tenant_fqdn = args.n1c_tenant_fqdn
    n1c_namespace = args.n1c_namespace
    nginx_instance_id = args.nginx_instance_id
    xc_api_token = args.xc_api_token
    nginx_config_file = args.nginx_config_file
    nginx_config_file_size = len(nginx_config_file)
    nginx_instance_hostname = args.nginx_instance_hostname

    auth_string = "APIToken " + xc_api_token
    headers = {
        "Authorization": auth_string,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    api_base_path = f"https://{n1c_tenant_fqdn}/api/nginx/one/namespaces/{n1c_namespace}"
    
    if nginx_instance_hostname != "nothing here, use the instance id":
        print("NGINX Instance Hostname " + nginx_instance_hostname + " provided, using this as a key to find the NGINX Instance ID")
        nginx_instance_list = n1c_list_instances(api_base_path, headers)
        nginx_instance_id = n1c_find_instance_by_hostname(nginx_instance_list, nginx_instance_hostname)
    else:
        print("No NGINX Instance Hostname, attemping to use NGINX Instance ID instead: " + nginx_instance_id)
    
    # Uncomment this block to see the current NGINX instance config
    #x = n1c_get_nginx_config(api_base_path, headers, nginx_instance_id)
    #print("------------------------------------------------------------------------------------")
    #print("Current NGINX Instance Config:")
    #print("------------------------------------------------------------------------------------")
    #print(json.dumps(x, indent=2))
    #print("------------------------------------------------------------------------------------")
    
    payload = {"aux": [], "conf_path": "/etc/nginx/nginx.conf", "configs": [ { "files": [ { "contents": nginx_config_file, "mtime": "1970-01-01T00:00:00Z", "name": "nginx.conf", "size": nginx_config_file_size } ], "name": "/etc/nginx" } ] }
    
    print("Attempting to patch nginx.conf on NGINX Instance Hostname " + nginx_instance_hostname + " which is NGINX Instance ID " + nginx_instance_id)
    publication_id = n1c_patch_nginx_config(api_base_path, headers, nginx_instance_id, payload)
    
    # Wait for the publication to be processed
    for x in range(6):
        sleep (5)  
        status = n1c_check_publication_status(api_base_path, headers, nginx_instance_id, publication_id)
        print("publication status for publication ID " + publication_id + " is: " + status )
        if status == "succeeded":
            print("NGINX configuration for NGINX Instance " + nginx_instance_hostname + " successfully updated.")
            break
        elif "failed" in status:
            sys.exit(2)
            
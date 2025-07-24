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
            return data['status']
        else:
            print(f"Something unexpected happened. HTTP Status Code: {response.status_code}")
            print("Response:", response.text)

    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='GitOps for NGINX One Console')
    parser.add_argument('--n1c_hostname', help='The F5 Distribted Cloud Tenant FQDN', default='nginx-tenant1.staging.volterra.us')
    parser.add_argument('--n1c_namespace', help="The F5 Distribted Cloud n1c_namespace within your tenant", default='default')
    parser.add_argument('--nginx_instance_id', help='The nginx instance uid from NGINX One Console', default='xxxxxxxxxxxxx')
    parser.add_argument('--xc_api_token', help='The F5 Distribted Cloud API Token', default='xxxxxxxxxxxxxxxx')
    parser.add_argument('--nginx_config_file', help='The nginx.conf, i.e. could come from the repo IaaC on push', default='xxxxxxxxxxxxxxxx')
    
    args = parser.parse_args()


    n1c_hostname = args.n1c_hostname
    n1c_namespace = args.n1c_namespace
    nginx_instance_id = args.nginx_instance_id
    xc_api_token = args.xc_api_token
    nginx_config_file = args.nginx_config_file
    nginx_config_file_size = len(nginx_config_file)

    auth_string = " APIToken " + xc_api_token
    headers = {
        "Authorization": auth_string,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    api_base_path = f"https://{n1c_hostname}/api/nginx/one/namespaces/{n1c_namespace}"
    
    nginx_instance_list = n1c_list_instances(api_base_path, headers)
    
    # Uncomment this block to see the current NGINX instance config
    #x = n1c_get_nginx_config(api_base_path, headers, nginx_instance_id)
    #print("------------------------------------------------------------------------------------")
    #print("Current NGINX Instance Config:")
    #print("------------------------------------------------------------------------------------")
    #print(json.dumps(x, indent=2))
    #print("------------------------------------------------------------------------------------")
    
    payload = {"aux": [], "conf_path": "/etc/nginx/nginx.conf", "configs": [ { "files": [ { "contents": nginx_config_file, "mtime": "1970-01-01T00:00:00Z", "name": "nginx.conf", "size": nginx_config_file_size } ], "name": "/etc/nginx" } ] }
    
    
    publication_id = n1c_patch_nginx_config(api_base_path, headers, nginx_instance_id, payload)
    sleep (5)  # Wait for the publication to be processed
    print("Checking publication status for publication ID:", publication_id)
    status = n1c_check_publication_status(api_base_path, headers, nginx_instance_id, publication_id)
    print(status)

    

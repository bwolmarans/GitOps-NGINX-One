import requests
import argparse
import json
import sys
import os
from urllib.parse import urljoin
import pprint
from requests.auth import HTTPBasicAuth

#- name: check publication status1
#run: |
#    curl -X GET https://${{ vars.N1SC_HOSTNAME }}/api/nginx/one/n1c_namespaces/default/instances/${{ vars.N1SC_INSTANCE }}/publications/${{ env.PUBLICATION_ID }}  -H 'Authorization: Bearer APIToken ${{ secrets.xc_bearer_token }}' -o response.json
#    cat response.json | jq -c .status

def n1c_list_instances(api_base_path, headers):
    try:
        response = requests.get(api_base_path + "/instances", headers=headers)
        # Check if the response was successful
        response_text = response.text
        print("Response received:", response_text)
        # Check if the response contains the word "xxx"
        if "online" in response_text:
            print("great")
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)

def n1c_patch_nginx_config(api_base_path, headers, nginx_instance_id, payload):
    print("\n\n\n\n\n")
    print(payload)
    print("\n\n\n\n\n")
    try:
        response = requests.patch(api_base_path + "/instances/" + nginx_instance_id + "/config" , headers=headers, json=payload)
        # Check if the response was successful
        if response.status_code == 200:
            response_text = response.text
            print("Response received:", response_text)
            # Check if the response contains the word "xxx"
            if "online" in response_text:
                print("great")
        else:
            print(f"Failed to Patch message. HTTP Status Code: {response.status_code}")
            print("Response:", response.text)

    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)

def n1c_get_nginx_config(api_base_path, headers, nginx_instance_id):
    try:
        response = requests.get(api_base_path + "/instances/" + nginx_instance_id + "/config" , headers=headers)
        # Check if the response was successful
        if response.status_code == 200:
            response_text = response.text
            print("Response received:", response_text)
            # Check if the response contains the word "xxx"
            if "online" in response_text:
                print("great")
            return response.text
        else:
            print(f"Failed. HTTP Status Code: {response.status_code}")
            print("Response:", response.text)
            return response.text
        
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='GitOps for NGINX One Console')
    parser.add_argument('--n1c_hostname', help='The F5 Distribted Cloud Tenant FQDN', default='nginx-tenant1.staging.volterra.us')
    parser.add_argument('--n1c_namespace', help="The F5 Distribted Cloud n1c_namespace within your tenant", default='default')
    parser.add_argument('--nginx_instance_id', help='The nginx instance uid from NGINX One Console', default='xxxxxxxxxxxxx')
    parser.add_argument('--xc_bearer_token', help='The F5 Distribted Cloud API Bearer Token', default='xxxxxxxxxxxxxxxx')
    parser.add_argument('--nginx_config_file', help='The nginx.conf, i.e. could come from the repo IaaC on push', default='xxxxxxxxxxxxxxxx')
    
    args = parser.parse_args()



    n1c_hostname = args.n1c_hostname
    n1c_namespace = args.n1c_namespace
    nginx_instance_id = args.nginx_instance_id
    xc_bearer_token = args.xc_bearer_token
    nginx_config_file = args.nginx_config_file
    nginx_config_file_size = len(nginx_config_file)

    auth_string = "Bearer APIToken " + xc_bearer_token
    headers = {
        "Authorization": auth_string,
        "Accept": "application/json"
    }

    #print(headers)

    # Define the payload (data) to post
    payload = {"aux": [], "conf_path": "/etc/nginx/nginx.conf", "configs": [ { "files": [ { "contents": nginx_config_file, "mtime": "1970-01-01T00:00:00Z", "name": "nginx.conf", "size": nginx_config_file_size } ], "name": "/etc/nginx" } ] }
    
    api_base_path = f"https://{n1c_hostname}/api/nginx/one/namespaces/default"
    
    n1c_list_instances(api_base_path, headers)
    x = n1c_get_nginx_config(api_base_path, headers, nginx_instance_id)
    print("------------------------------------------------------------------------------------")
    print("Current NGINX Instance Config:")
    print("------------------------------------------------------------------------------------")
    print(json.dumps(x, indent=2))
    print("------------------------------------------------------------------------------------")
    print("PAYLOAD")
    print("------------------------------------------------------------------------------------")
    print(payload)
    print("\n\n\n\n\n")

    
    
    #n1c_patch_nginx_config(api_base_path, headers, nginx_instance_id, payload)
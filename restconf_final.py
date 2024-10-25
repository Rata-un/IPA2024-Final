import json
import requests
requests.packages.urllib3.disable_warnings()

# Router IP Address is 10.0.15.181-184
api_url = "https://10.0.15.184/restconf/data"

# the RESTCONF HTTP headers, including the Accept and Content-Type
# Two YANG data formats (JSON and XML) work with RESTCONF 
headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}
basicauth = ("admin", "cisco")


def create(student_id):
    loopback_interface = f"Loopback{student_id}"
    ip_suffix = student_id[-3:]
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": loopback_interface,
            "description": "created loopback by RESTCONF",
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": f"172.30.{ip_suffix}.1",
                        "netmask": "255.255.255.0"
                    }
                ]
            },
            "ietf-ip:ipv6": {}
        }
    }  

    print(json.dumps(yangConfig, indent=2))

    resp = requests.put(
        api_url + f"/ietf-interfaces:interfaces/interface={loopback_interface}", 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if resp.status_code == 204:
        return f"Cannot create: Interface loopback {student_id} already exists"
    elif(resp.status_code >= 200 and resp.status_code <= 299): 
        print("STATUS OK: {}".format(resp.status_code))
        return f"Interface loopback {student_id} is created successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))


def delete(student_id):
    loopback_interface = f"Loopback{student_id}"
    resp = requests.delete(
        api_url + f"/ietf-interfaces:interfaces/interface={loopback_interface}", 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return f"Interface {loopback_interface} is deleted successfully."
    elif resp.status_code == 404:
        return f"Cannot delete: Interface loopback {student_id}"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))


def enable(student_id):
    loopback_interface = f"Loopback{student_id}"
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": loopback_interface,
            "enabled": True 
        }
    }

    resp = requests.patch(
        api_url + f"/ietf-interfaces:interfaces/interface={loopback_interface}", 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return f"Interface {loopback_interface} is enabled successfully."
    elif resp.status_code == 404:
        return f"Cannot enable: Interface loopback {student_id}"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))


def disable(student_id):
    loopback_interface = f"Loopback{student_id}"
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": loopback_interface, 
            "enabled": False
        }
    }

    resp = requests.patch(
        api_url + f"/ietf-interfaces:interfaces/interface={loopback_interface}",  
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return f"Interface {loopback_interface} is shutdowned successfully."
    elif resp.status_code == 404:
        return f"Cannot disable: Interface loopback {student_id}"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))


def status(student_id):
    loopback_interface = f"Loopback{student_id}"
    api_url_status = f"https://10.0.15.184/restconf/data/ietf-interfaces:interfaces-state/interface={loopback_interface}"


    resp = requests.get(
        api_url_status,
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        response_json = resp.json()
        admin_status = response_json['ietf-interfaces:interface']['admin-status']
        oper_status = response_json['ietf-interfaces:interface']['oper-status']
        if admin_status == 'up' and oper_status == 'up':
            return f"Interface {loopback_interface} is enabled."
        elif admin_status == 'down' and oper_status == 'down':
            return f"Interface {loopback_interface} is disabled."
    elif(resp.status_code == 404):
        print("STATUS NOT FOUND: {}".format(resp.status_code))
        return f"No Interface {loopback_interface}."
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return f"Error retrieving status for interface {loopback_interface}."

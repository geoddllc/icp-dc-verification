import requests
import ipaddress

def get_data_center_info(dc_id):
    data_center_url = f"https://ic-api.internetcomputer.org/api/v3/data-centers/{dc_id}"
    response = requests.get(data_center_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get data center info. Status code: {response.status_code}")
        return None

def get_nodes_info(dc_id):
    nodes_url = f"https://ic-api.internetcomputer.org/api/v3/nodes?dc_id={dc_id}"
    response = requests.get(nodes_url)
    if response.status_code == 200:
        return response.json().get("nodes", [])
    else:
        print(f"Failed to get nodes info. Status code: {response.status_code}")
        return []

def get_rdap_url(region, subnet):
    if region == "Asia":
        return f"https://rdap.apnic.net/ip/{subnet}"
    elif region == "America":
        return f"https://rdap.arin.net/registry/ip/{subnet}"
    elif region == "Europe":
        return f"https://rdap.db.ripe.net/ip/{subnet}"
    else:
        print(f"Unsupported region: {region}")
        return None

def get_rdap_info(rdap_url):
    if not rdap_url:
        return None

    response = requests.get(rdap_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get RDAP info for {rdap_url}. Status code: {response.status_code}")
        return None

def extract_country_from_rdap(region, rdap_info):
    try:
        if region == "Asia":
            return rdap_info.get("country", "").upper()
        elif region == "America":
            return rdap_info.get("entities", [])[0].get("vcardArray", [])[1][3][3].upper()
        elif region == "Europe":
            return rdap_info.get("handle", "").split("-")[-1].upper()
        else:
            return ""
    except Exception as e:
        print(f"Failed to extract country from RDAP info. Error: {e}")
        return ""

def main(dc_id):
    # Step 1: Get data center details
    data_center_info = get_data_center_info(dc_id)
    if not data_center_info:
        return

    region, dc_country = data_center_info.get("region").split(",")[0], data_center_info.get("region").split(",")[1]
    print(f"Data Center Country: {dc_country}, Region: {region}")

    # Step 2: Get nodes details
    nodes_info = get_nodes_info(dc_id)
    if not nodes_info:
        return

    correct_nodes = 0
    issues = 0
    invalid_nodes = []

    # Step 3: Check each node's subnet and RDAP info
    for node in nodes_info:
        ip_address = node["ip_address"]
        node_id = node["node_id"]
        
        try:
            # Extract the /64 subnet for the IP address
            ip_obj = ipaddress.IPv6Address(ip_address)
            subnet = ipaddress.IPv6Network(f"{ip_obj}/64", strict=False)
            
            print(f"Checking IP: {ip_address}, Subnet: {subnet}")
            
            # Step 4: Determine the correct RDAP URL based on the region
            rdap_url = get_rdap_url(region, subnet)
            if not rdap_url:
                continue
            
            # Step 5: Perform RDAP lookup
            rdap_info = get_rdap_info(rdap_url)
            if rdap_info:
                country = extract_country_from_rdap(region, rdap_info)
                print(f"RDAP Country: {country}")
                
                # Step 6: Compare the RDAP country with the data center's country
                if country == dc_country:
                    print(f"IP {ip_address} is correctly advertised in {dc_country}.")
                    correct_nodes += 1
                else:
                    print(f"Warning: IP {ip_address} is advertised in {country}, not in {dc_country} as expected.")
                    issues += 1
                    invalid_nodes.append(node_id)
        
        except Exception as e:
            print(f"Failed to process IP {ip_address}. Error: {e}")
            issues += 1
            invalid_nodes.append(node_id)

    # Summary
    print("\nSummary:")
    print(f"Nodes correctly advertised in {dc_country}: {correct_nodes}")
    print(f"Issues found: {issues}")
    if issues > 0:
        print("Invalid Node IDs:")
        for node_id in invalid_nodes:
            print(f" - {node_id}")

if __name__ == "__main__":
    # Example: You can replace 'cm1' with any other data center ID
    dc_id_input = input("Enter Data Center ID (e.g., cm1): ").strip()
    main(dc_id_input)

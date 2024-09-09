import os
import json
import yaml
import shutil

def convert_domain(sing_rule):
    mihomo_rule = {
        "payload": []
    }
    for rule in sing_rule["rules"]:
        domain_list = rule.get("domain")
        if domain_list:
            if isinstance(domain_list, str):
                domain_list = [domain_list]
            mihomo_rule["payload"] += domain_list
        domain_suffix_list = rule.get("domain_suffix") 
        if domain_suffix_list:
            if isinstance(domain_suffix_list, str):
                domain_suffix_list = [domain_suffix_list]
            for domain_suffix in domain_suffix_list:
                if domain_suffix[0] != "+":
                    if domain_suffix[0] == ".":
                        mihomo_rule["payload"].append(f"+{domain_suffix}")
                    else:
                        mihomo_rule["payload"].append(f"+.{domain_suffix}")
                else:
                    mihomo_rule["payload"].append(f"domain_suffix")
    return mihomo_rule


def convert_domain_regex(sing_rule):
    mihomo_rule = {
        "payload": []
    }
    for rule in sing_rule["rules"]:
        domain_regex_list = rule.get("domain_regex")
        if domain_regex_list:
            if isinstance(domain_regex_list, str):
                domain_regex_list = [domain_regex_list]
            for domain_regex in domain_regex_list:
                mihomo_rule["payload"].append(f"DOMAIN-REGEX,{domain_regex}")
    return mihomo_rule


def convert_ipcidr(sing_rule):
    mihomo_rule = {
        "payload": []
    }
    for rule in sing_rule["rules"]:
        ipcidr_list = rule.get("ip_cidr")
        if ipcidr_list:
            if isinstance(ipcidr_list, str):
                ipcidr_list = [ipcidr_list]
            mihomo_rule["payload"] += ipcidr_list
    return mihomo_rule

input_path = './'
geosite_dir = 'sing-geosite'
geoip_dir = 'sing-geoip'

output_path = './out'
domain_dir = 'domain'
classical_dir = 'classical'
ipcidr_dir = 'ipcidr'

def main():
    if os.path.exists(output_path):
        shutil.rmtree(output_path, ignore_errors=True) if os.path.isdir(output_path) else os.remove(output_path)  
    os.makedirs(f"{output_path}/{domain_dir}")
    os.makedirs(f"{output_path}/{classical_dir}")
    os.makedirs(f"{output_path}/{ipcidr_dir}")

    geosite_rules = os.listdir(f'{input_path}/{geosite_dir}')
    geosite_count = 0
    domain_count = 0
    classical_count = 0
    for geosite_rule in geosite_rules:
        if geosite_rule[-5:] != ".json":
            continue
        geosite_count += 1
        with open(f'{input_path}/{geosite_dir}/{geosite_rule}', 'r', encoding='utf-8') as f:
            sing_rule = json.load(f)
        if sing_rule["version"] not in [1, 2]:
            print(f'Unsupport sing-box rule-set version: {sing_rule["version"]} on {geosite_rule}')
            continue
        domain_rule_set = convert_domain(sing_rule)
        if len(domain_rule_set["payload"]) > 0:
            with open(f'{output_path}/{domain_dir}/{geosite_rule.replace(".json",".yaml")}', 'w', encoding='utf-8') as f:
                yaml.dump(domain_rule_set, f, Dumper=yaml.CDumper)
            domain_count += 1
        domain_regex_rule_set = convert_domain_regex(sing_rule)
        if len(domain_regex_rule_set["payload"]) > 0:
            with open(f'{output_path}/{classical_dir}/{geosite_rule.replace(".json","-regex.yaml")}', 'w', encoding='utf-8') as f:
                yaml.dump(domain_regex_rule_set, f, Dumper=yaml.CDumper)
            classical_count += 1
    print(f"Found: {geosite_count} geosite | Convert: {domain_count} domain, {classical_count} classical(domain-regex)")

    geoip_rules = os.listdir(f'{input_path}/{geoip_dir}')
    geoip_count = 0
    ipcidr_count = 0
    for geoip_rule in geoip_rules:
        if geoip_rule[-5:] != ".json":
            continue
        geoip_count += 1
        with open(f'{input_path}/{geoip_dir}/{geoip_rule}', 'r', encoding='utf-8') as f:
            sing_rule = json.load(f)
        if sing_rule["version"] not in [1, 2]:
            print(f'Unsupport sing-box rule-set version: {sing_rule["version"]} on {geoip_rule}')
            continue
        ipcidr_rule_set = convert_ipcidr(sing_rule)
        if len(ipcidr_rule_set["payload"]) > 0:
            with open(f'{output_path}/{ipcidr_dir}/{geoip_rule.replace(".json",".yaml")}', 'w', encoding='utf-8') as f:
                yaml.dump(ipcidr_rule_set, f, Dumper=yaml.CDumper)
            ipcidr_count += 1
    print(f"Found: {geoip_count} geoip | Convert: {ipcidr_count} ipcidr")

if __name__ == "__main__":
    main()

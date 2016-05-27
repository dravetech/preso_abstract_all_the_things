from ansible.module_utils.basic import *  #noqa


def main():
    """Main module"""
    module = AnsibleModule(
        argument_spec=dict(
            device_name=dict(type='str', required=True),
            fabric=dict(type='list', required=True),
            fabric_link_prefix=dict(type='str', required=True),
            bgp_neighbors=dict(type='dict', required=True),
        ),
    )
    device_name = module.params['device_name']
    fabric = module.params['fabric']
    fabric_link_prefix = module.params['fabric_link_prefix']
    bgp_neighbors = module.params['bgp_neighbors']

    result = []
    good = bad = 0
    healthy_fabric = True
    for index, link in enumerate(fabric):
        if device_name == link['left']:
            peer = "{}{}::1".format(fabric_link_prefix, index+1)
        elif device_name == link['right']:
            peer = "{}{}::".format(fabric_link_prefix, index+1)
        else:
            continue
        try:
            is_up = bgp_neighbors['global']['peers'][peer]['is_up']
            if not is_up:
                msg="{l[left]}:{l[left_port]} --- {l[right]}:{l[right_port]} is down".format(l=link)
                result.append(msg)
                healthy_fabric = False
                bad += 1
            else:
                good += 1
        except KeyError:
            bad += 1
            msg="{l[left]}:{l[left_port]} --- {l[right]}:{l[right_port]} is not configured".format(l=link)
            result.append(msg)
            healthy_fabric = False


    link_health = "Good links: {}, bad links: {}".format(good, bad)
    if healthy_fabric:
        module.exit_json(msg=link_health)
    else:
        result.insert(0, link_health)
        module.fail_json(msg='\n'.join(result), healthy_fabric=healthy_fabric)

if __name__ == '__main__':
    main()

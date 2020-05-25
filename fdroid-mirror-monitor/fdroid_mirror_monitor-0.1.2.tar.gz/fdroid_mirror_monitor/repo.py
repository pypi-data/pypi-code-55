#!/usr/bin/env python3

# external:
from fdroidserver import common, index


def _calculate_infos(data):
    size_outdated = 0
    size_current = 0
    num_current_packages = 0
    num_outdated_packages = 0
    infos = dict()

    # there are apps that have multiple packages per versionName (for different hardware platforms)
    # size_current calculates the sum of all package sizes with the current versionName
    for package_name in data['packages']:
        i = 0
        current_version = 0
        for packages in data['packages'][package_name]:

            # get current version from latest package:
            if i == 0:
                current_version = packages['versionName']
                size_current += packages['size']
                num_current_packages += 1
            else:
                older_version = packages['versionName']

                if older_version == current_version:
                    size_current += packages['size']
                    num_current_packages += 1
                else:
                    size_outdated += packages['size']
                    num_outdated_packages += 1

            i += 1

    infos['all_packages_size'] = size_current + size_outdated
    infos['current_packages_size'] = size_current

    infos['#all_packages'] = num_current_packages + num_outdated_packages
    infos['#current_packages'] = num_current_packages

    infos['#apps'] = len(data['apps'])
    return infos


# TODO: maybe extract info from public key
def infos_from_jar(file='index-v1.jar', fingerprint=None, minimal=False):
    '''
    supports only index-v1.jar

    :param fingerprint: optional: verify fingerprint
    :minimal: if set to True, don't calculate sizes and number of apps/packages
    :return: dict of with repo info
        address
        description
        fingerprint
        icon
        maxage
        mirrors
        name
        timestamp
        version

        #all_packages
        #apps
        #current_packages
        all_packages_size
        current_packages_size
    '''
    config = dict()
    config['jarsigner'] = 'jarsigner'
    common.config = config
    index.config = config
    with open(file, 'r') as fp:
        if fingerprint is None:
            data, public_key, received_fingerprint = index.get_index_from_jar(fp.name)
        else:
            data, public_key, received_fingerprint = index.get_index_from_jar(fp.name, fingerprint)
    infos = dict()
    infos['fingerprint'] = received_fingerprint
    for k in ('timestamp', 'version', 'maxage', 'name', 'icon', 'address', 'description', 'mirrors'):
        infos[k] = data['repo'][k]

    if minimal is False:
        infos.update(_calculate_infos(data))

    return infos


if __name__ == '__main__':
    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument('file',
                        help='path to file')
    parser.add_argument('-f', '--fingerprint',
                        help='verify the fingerprint')
    parser.add_argument('-m', '--minimal',
                        help='''don't calculate sizes and number of apps/packages''',
                        action='store_true')
    args = parser.parse_args()

    r = infos_from_jar(file=args.file, fingerprint=args.fingerprint, minimal=args.minimal)
    print(json.dumps(r))

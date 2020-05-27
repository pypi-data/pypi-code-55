import logging
import re

from .connection import DSMConnection
from .process import Process

LOG = logging.getLogger(__name__)


class Task():
    """
    Reimplementation of the shell scripts on https://git.uis.cam.ac.uk/i/uis/infra/dellsc.git
    """
    def __init__(self, host, port, user, password, verify):
        self.process = Process()
        self.dsm_connection = DSMConnection(host, port, user, password, verify)

    def __enter__(self):
        self.dsm_connection.open_connection()
        return self

    def __exit__(self, tipe, value, traceback):
        self.dsm_connection.close_connection()
        self.dsm_connection = None
        self.process = None

    def get_volume_info(self, wwn=None, mountpoint=None):
        """
        Returns details of volume with WWN `wwn` or mounted on `mountpoint`.

        :param wwn: volume's `wwn`.
        :param mountpoint: `mountpoint` where the volume is mounted.
        :returns: tuple (wwn, volid, volname, volFolderName, volFolderId, scName), `None`, otherwise.
        """
        if wwn is None and mountpoint is None:
            return None

        if mountpoint is not None:
            mpath = self.process.get_mpath_from_mountpoint(mountpoint)
            if mpath is None:
                return None

            wwn = self.process.get_wwn_from_mpath(mpath)
            if wwn is None:
                return None

        # get list of volumes
        self.dsm_connection.get_volumes()

        if self.dsm_connection.volumes.get(wwn) is not None:
            volid = self.dsm_connection.volumes[wwn].get('instanceId')
            volname = self.dsm_connection.volumes[wwn].get('name')
            volFolderName = self.dsm_connection.volumes[wwn].get('volumeFolderName')
            volFolderId = self.dsm_connection.volumes[wwn].get('volumeFolderId')
            volScName = self.dsm_connection.volumes[wwn].get('scName')
        else:
            LOG.error('Cannot get volume with WWN %s.', wwn)
            return None

        return (wwn, volid, volname, volFolderName, volFolderId, volScName)

    def get_vol_wwn_from_id(self, volid):
        """
        Returns volume wwn from volume ID.

        :param volid: volume ID.
        :return: volume WWN, `None` otherwise.
        """
        self.dsm_connection.get_volumes()
        for wwn, vol_info in self.dsm_connection.volumes.items():
            if self.dsm_connection.volumes[wwn]['instanceId'] == str(volid):
                return wwn

        LOG.error('Cannot get the volume WWN from the volume ID %s.', volid)

        return None

    def generate_clone_name(self, volume_name):
        """
        Generates a clone name from a volume name.

        :param volume_name: the volume name from which to generate a clone name.
        :returns: clone name, `None`, otherwise.
        """
        # remove clone name suffix from volume name
        original_name = re.sub(r'_\d+$', '', volume_name)

        # get list of volumes starting with 'orig_volname'
        self.dsm_connection.get_volumes()
        lst = []
        for vol in self.dsm_connection.volumes.values():
            if vol['name'].startswith(original_name) and not vol['inRecycleBin']:
                lst.append(vol['name'])

        if len(lst) == 0:
            LOG.error('Clone name cannot be generated as no volumes is found.')
            return None

        # get indexes in the volume list
        volname_with_index = re.compile(r'.*(_\d+)$')
        volindex_lst = [int(volname_.replace(f'{original_name}_', ''))
                        for volname_ in lst if volname_with_index.match(volname_)]
        volindex_lst.sort()
        if len(volindex_lst) == 0:
            clone_index = 1
        else:
            clone_index = volindex_lst[-1] + 1

        return f'{original_name}_{clone_index}'

    def get_local_server_id(self):
        """Returns local server ID, or `None` on error."""
        hostname = self.process.get_hostname()
        server_name = hostname.split('.')[0]

        server_id = self.dsm_connection.get_server_id(server_name)
        if server_id is None:
            LOG.error('Cannot get server ID of local server %s.', server_name)

        return server_id

    def replace_volume(self, src_mountpoint, dst_mountpoint, unmount_src_mp):
        """
        Clones the volume mounted on `src_mountpoint` and mount it on `dst_mountpoint`,
        the volume that was mounted on `dst_mountpoint` will be deleted.

        :param src_mountpoint: mountpoint of the volume to be cloned.
        :param dst_mountpoint: mountpoint of the clone volume.
        :param unmount_src_mp: If True, unmount the source mountpoint, otherwise, not.
        :return: `True` for success, `False` on error.
        """
        # check details of vols on source and destination mountpoints
        # volume details: (wwn, volid, volname, volFolderName, volFolderId, scName)
        src_vol_info = self.get_volume_info(mountpoint=src_mountpoint)
        if src_vol_info is None:
            return False

        dst_vol_info = self.get_volume_info(mountpoint=dst_mountpoint)
        if dst_vol_info is None:
            return False

        # unmount the volume to be cloned, call it "the source volume"
        if unmount_src_mp:
            if not self.process.umount(src_mountpoint):
                return False

        # unmount the destination volume
        if not self.process.umount(dst_mountpoint):
            return False

        # delete destination volume
        if not self.delete_volume(dst_vol_info[0]):
            return False

        # create a clone of source volume and mount it on dst_moutpoint
        clone_name = self.generate_clone_name(src_vol_info[2])
        if not self.clone_volume(src_vol_info[0], 'from_replace_volume', clone_name, dst_mountpoint):
            return False

        # mount source volume if needed
        if unmount_src_mp:
            if not self.process.mount(src_mountpoint):
                return False

        return True

    def unmap_dellsc_volume(self, wwn):
        """
        Unmaps a Dell SC volume with `WWN`. Unmounting the volume should be performed manually.

        :param wwn: `wwn` of the volume to unmap.
        :returns: `True` for success, `False` on error.
        """
        # make sure volume is not mounted
        if self.process.is_wwn_mounted(wwn) is not None:
            LOG.error('Volume with WWN %s is mounted on local server. Unmount it first.', wwn)
            return False

        # check if volume exists on Dell SCs
        vol_info = self.get_volume_info(wwn)
        if vol_info is None:
            return False

        # check if volume is visible to local server
        alias = self.process.get_mpath_from_wwn(wwn)
        if alias is None:
            return False

        # make sure volume is mapped to local server
        vol_mappings = self.dsm_connection.get_vol_mappings(vol_info[1])
        if vol_mappings is None:
            return False

        servers = [x['server']['instanceName'] for x in vol_mappings]
        if self.process.get_hostname().split('.')[0] not in servers:
            LOG.error('Volume with ID %s is not mapped to local server.', vol_info[1])
            return False

        # remove volume from fstab config file
        device_name = f'/dev/mapper/{alias}p1'
        if self.process.is_device_in_fstab(device_name):
            if not self.process.remove_entry_from_fstab(device_name):
                return False
            if not self.process.daemon_reload():
                return False
        else:
            LOG.warning('%s is not in /etc/fstab.', device_name)

        # remove (wwid, alias) entry from multipath.conf
        if not self.process.remove_multipath_entry(wwn, alias):
            return False

        # reload multipathd
        if not self.process.reload_multipathd():
            return False

        # get wwid from wwn
        wwid = self.process.get_wwid_from_wwn(wwn)
        if wwid is None:
            return False

        # delete raw devices of multipath device alias
        raw_devices = self.process.get_multipath_raw_devices(wwid)
        if raw_devices is None:
            LOG.warning('No raw devices (%s) for multipath device %s.', raw_devices, alias)
        else:
            result_delete_rawdevs = []

            for rawdev in raw_devices:
                result = self.process.delete_raw_devices(rawdev)
                result_delete_rawdevs.append(result)

            if False in result_delete_rawdevs:
                LOG.error('Failed to delete the raw devices %s of %s. Result: %s.',
                          raw_devices, alias, result_delete_rawdevs)
                return False

            LOG.info('The raw devices %s of %s have been deleted. Result: %s.',
                     raw_devices, alias, result_delete_rawdevs)

        # reload multipathd
        if not self.process.reload_multipathd():
            return False

        # unmap the volume from the local server
        return self.dsm_connection.unmap_volume(vol_info[1])

    def delete_volume(self, wwn, recycle=True):
        """
        Deletes a volume with `wwn`.

        :param wwn: `wwn` of the volume to delete.
        :returns: `True` for success, `False` on error.
        """
        # unmap the volume from the local server
        if not self.unmap_dellsc_volume(wwn):
            return False

        # get volid
        vol_info = self.get_volume_info(wwn)
        if vol_info is None:
            return False

        # delete the volume
        return self.dsm_connection.delete_volume(vol_info[1], recycle=recycle)

    def map_dellsc_volume(self, wwn, mountpoint=None):
        """
        Maps Dell SC volume with `WWN` to local server and mounts it on `mountpoint`.

        :param wwn: WWN of the volume to map to local server.
        :param mountpoint: optional field. Mountpoint to mount the volume on.
        :returns: `True` for success, `False` on error.
        """
        # check if volume exists and get its attributes
        vol_info = self.get_volume_info(wwn)
        if vol_info is None:
            return False

        # check if the volume is already mapped to any servers
        vol_mappings = self.dsm_connection.get_vol_mappings(vol_info[1])
        if vol_mappings is None:
            return False

        if len(vol_mappings) > 0:
            LOG.error('Volume %s is already mapped to: %s.',
                      wwn, [x['server']['instanceName'] for x in vol_mappings])
            return False

        # get ID of local server id and map the volume to it
        server_id = self.get_local_server_id()
        if server_id is None:
            return False

        if not self.dsm_connection.map_volume_to_server(vol_info[1], server_id):
            return False

        # rescan scsi bus
        if not self.process.rescan_scsibus():
            return False

        # add multipath alias of the volume
        if not self.process.add_multipath_alias(wwn):
            return False

        # reload multipath
        if not self.process.reload_multipathd():
            return False

        # if a mountpoint is specified, update fstab file and mount the volume
        if mountpoint is None:
            LOG.info('Mountpoint is not specified.')
            return True

        new_alias = self.process.get_mpath_from_wwn(wwn)
        if new_alias is not None:
            new_fsdevice = f'/dev/mapper/{new_alias}p1'
            if not self.process.add_entry_in_fstab(new_fsdevice, mountpoint):
                LOG.error('%s cannot be added to /etc/fstab', new_fsdevice)
                return False
            if not self.process.daemon_reload():
                return False
        else:
            LOG.error('Alias for the volume with WWN %s does not exist.', mountpoint)
            return False

        # mount target_mountpoint if it's not mounted
        # found it gets mounted after reload multipath, is it an expected behaviour?
        if not self.process.mountpoint_exists(mountpoint):
            if not self.process.mount(mountpoint):
                return False

        return True

    def clone_volume(self, volume_wwn, replay_label, clone_name, target_mountpoint):
        """
        Creates a snapshot of a volume, then creates a view volume from the snapshot,
        map the view volume to local server and mount it on `target_mountpoint`.

        :param volume_wwn: wwn of volume from which to create the snapshot and the view volume.
        :param replay_label: label of the snapshot to create the volume from.
        :param clone_name: name of clone volume.
        :param target_mounpoint: where to mount the view volume.
        :return: `True` for success, `False` on failure.
        """
        if not self.process.is_dir_empty(target_mountpoint):
            return False

        # get volume info: (wwn, volid, volname, volFolderName, volFolderId, scName)
        vol_info = self.get_volume_info(wwn=volume_wwn)
        if vol_info is None:
            return False

        # create snapshot from volume
        snapshot_id = self.dsm_connection.create_snapshot(vol_info[1], description=replay_label)
        if snapshot_id is None:
            return False

        # check if the source volume is a camsis volume
        replay_profile_id = None
        self.dsm_connection.get_snapshot_profiles()
        if self.dsm_connection.rply_profiles is None:
            return False

        if 'camsis' in vol_info[3].lower():
            # we're sure 'camsis' replay profile exists
            replay_profile_id = self.dsm_connection.rply_profiles['camsis']['instanceId']

        # create view volume
        view_volume_id = self.dsm_connection.create_view_volume(
            snapshot_id, replay_profile_id, clone_name, vol_info[4])

        # get view volume wwn
        view_volume_wwn = self.get_vol_wwn_from_id(view_volume_id)

        if view_volume_wwn is None:
            return False

        # map the volume to local server
        return self.map_dellsc_volume(view_volume_wwn, target_mountpoint)

    def create_snapshot(self, mountpoint, label, retention):
        """
        Creates a snapshot of the volume mounted on `mountpoint`.

        :param mountpoint: the mountpoint where the volume is mounted.
        :param label: snapshot label.
        :param retention: retention period of the snapshot to create, in days.
        :return: `True` for success, `False` on error.
        """
        # check if snapshot label is valid
        if not self.process.is_snapshot_label_valid(label):
            LOG.error('Snapshot label %s is not valid.', label)
            return False

        # check if the retention is between 1 and 99 days
        if not (int(retention) in range(1, 100)):
            LOG.error('Retention %s is not valid.', retention)
            return False

        # check if volume is on DSM
        vol_info = self.get_volume_info(mountpoint=mountpoint)
        if vol_info is None:
            LOG.error('No info on volume mounted on %s.', mountpoint)
            return False

        # get fsdevice. TODO: is this check really needed?
        fsdevice = self.process.get_fsdevice_from_mountpoint(mountpoint)
        if fsdevice is None:
            LOG.error('No fs device of volume mounted on %s.', mountpoint)
            return False

        # create the snapshot
        result = self.dsm_connection.create_snapshot(vol_info[1], label, int(retention)*1440)

        return False if result is None else True

    def delete_recycled_vols(self, recycled_vols_file):
        """
        Deletes the volumes listed in a file passed in argument.
        The volume must be in Recycle Bin to be deleted.

        :param recycled_vols_file: file containing the list of recycled volumes to be deleted.
        Each line in the file should contain the volume's WWN.
        The file should only contain lines in the following format:
        ('6000d31000e3940000000000000001c9', {'instanceId': '58260.165', \
            'inRecycleBin': True, 'volumeFolderPath': 'All Volumes/SB_VMWare_vols/', \
            'volumeFolderName': 'SB_VMWare_vols', 'volumeFolderId': '58260.11', \
            'status': 'Down', 'name': 'test_vol', 'scName': 'WCDC Storage Center'})
        :return: `True` if all the volumes that are in Recycle Bin are deleted, `False` otherwise.
        """
        if not self.dsm_connection.get_recycled_volumes():
            return False

        wwns = []
        with open(recycled_vols_file, 'r') as rvf:
            # extract the wwn and ignore the commented lines
            for linenum, line in enumerate(rvf):
                if not line.startswith('#'):
                    rs = re.search(r"\('[A-Za-z0-9]{32}'", line)
                    if rs:
                        wwns.append(rs.group(0).replace("'", '').replace("(", ''))
                    else:
                        LOG.warning("Cannot find a valid WWN in line number %s (%s...)", linenum, line[0:50])

        results = []
        for wwn in wwns:
            if self.dsm_connection.recycled_vols.get(wwn) is None:
                LOG.warning(f"Volume with WWN '{wwn}' will not be deleted as the WWN may not be valid"
                            " or the volume is not in Recycle Bin.")
            else:
                LOG.info('Volume %s will be DELETED from the Recyle Bin!', wwn)
                result_del_vol = self.dsm_connection.delete_volume(
                    self.dsm_connection.recycled_vols[wwn]['instanceId'], recycle=False)
                results.append(result_del_vol)

        return False if False in results else True

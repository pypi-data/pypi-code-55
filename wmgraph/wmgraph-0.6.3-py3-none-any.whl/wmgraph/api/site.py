class MgraphConnectoSiteMixin:
    def get_root_site(self):
        return self.get('/sites/root')

    def get_site(self, site_id):
        return self.get(f'/sites/{site_id}')

    def get_site_drive(self, site_id):
        return self.get(f'/sites/{site_id}/drive')

    def get_site_drives(self, site_id):
        res = self.get(f'/sites/{site_id}/drives')
        if 'value' in res:
            return res['value']
        return []

    def search_sites(self, site_name):
        res = self.get(f'/sites?search={site_name}')
        if 'value' in res:
            return res['value']
        return []

    def get_subsites(self, site_id):
        return self.get(f'/sites/{site_id}/sites')

    def walk_sites(self, site=None):
        if site is None:
            site = self.get_root_site()
            self.sites = {}
            self.sites[site['id']] = site
        subsites = self.get_subsites(site['id'])
        # jdump(subsites, caller=__file__)
        if 'value' in subsites:
            for subsite in subsites['value']:
                self.sites[subsite['id']] = subsite
                self.walk_sites(site=subsite)
        return self.sites

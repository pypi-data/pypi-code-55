class MgraphConnectorAuditlogsMixin:

    def list_directoryaudits(self, **kwargs):
        '''
        iterator over all audit log entries.
        '''
        return self.get_paged(f'/auditLogs/directoryAudits', **kwargs)

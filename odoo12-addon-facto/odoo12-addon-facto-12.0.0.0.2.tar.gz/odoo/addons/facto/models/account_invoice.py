# -*- coding: utf-8 -*-
# © 2020 Coopdevs - César López Ramírez  <cesar.lopez@coopdevs.org>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.onchange('partner_id', 'company_id')
    def _onchange_partner_id(self):
        res = super(AccountInvoice, self)._onchange_partner_id()
        if self.partner_id and self.type == 'out_invoice':
            pay_mode = self.payment_mode_id
            if pay_mode and pay_mode.bank_account_link == 'fixed':
                self.partner_bank_id = pay_mode.fixed_journal_id. \
                    bank_account_id
        return res


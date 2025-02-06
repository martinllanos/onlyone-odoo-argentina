##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class AccountAccount(models.Model):
    _inherit = "account.account"

    @api.model
    def set_non_monetary_tag(self, company):
        """Set <Non Monetary> tag to the corresponding accounts taking into account the account type"""
        non_monetary_tag = self.env.ref("l10n_ar_ux.no_monetaria_tag")
        account_types = [
            "asset_non_current",
            "asset_fixed",
            "income",
            "income_other",
            "expense",
            "expense_depreciation",
            "equity",
            "expense_direct_cost",
        ]
        if accounts := self.search(
            [("account_type", "in", account_types), *self.env["account.account"]._check_company_domain(company)]
        ).filtered(lambda x: x.company_fiscal_country_code == "AR"):
            accounts.write({"tag_ids": [(4, non_monetary_tag.id)]})
            _logger.info("Non Monetary tag is set on %s accounts ." % (company.name))

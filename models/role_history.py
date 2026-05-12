from odoo import fields, models, api

class ChamaRoleHistory(models.Model):
    _name = 'chamatech.role.history'
    _description = 'Chama Role History'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    member_id = fields.Many2one('chamatech.member', string="Member", ondelete='set null')
    role_id = fields.Many2one('chamatech.role', string="Role", ondelete='set null')
    date_assigned = fields.Date(string="Date Assigned", default=fields.Date.context_today)
    date_resigned = fields.Date(string="Date Resigned")


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('member_id'):
                # 1. Find the member's CURRENT active role (any role)
                # We want to close their previous role, wherever it was.
                active_history = self.search([
                    ('member_id', '=', vals['member_id']),
                    ('date_resigned', '=', False)
                ], limit=1)

                if active_history:
                    # 2. Stamp the resignation date on the OLD role
                    active_history.write({
                        'date_resigned': fields.Date.context_today(self)
                    })
        
        # 3. Create the NEW record (which has its own role_id from vals)
        return super(ChamaRoleHistory, self).create(vals_list)
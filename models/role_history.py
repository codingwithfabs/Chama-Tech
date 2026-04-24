from odoo import fields, models, api

class ChamaRoleHistory(models.Model):
    _name = 'chamatech.role.history'
    _description = 'Chama Role History'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    member_id = fields.Many2one('chamatech.member', string="Member")
    role_id = fields.Many2one('chamatech.role', string="Role")
    date_assigned = fields.Date(string="Date Assigned", default=fields.Date.context_today)
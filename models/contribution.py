from odoo import fields, api, models

class ChamaContribution(models.Model):
    _name = 'chamatech.contribution'
    _description = 'Member Contributions'
    _order = 'date desc'

    member_id = fields.Many2one('chamatech.member', string="Member", required=True, ondelete='cascade')
    date = fields.Date(string="Date", default=fields.Date.context_today, required=True)
    amount = fields.Float(string="Amount", required=True)
    notes = fields.Char(string="Notes")
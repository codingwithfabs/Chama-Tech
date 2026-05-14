from odoo import fields, api, models

class ChamaContribution(models.Model):
    _name = 'chamatech.contribution'
    _description = 'Member Contributions'

    member_id = fields.Many2one('chamatech.member', string="Member", required=True)
    amount = fields.Float(string="Amount", required=True)
    date = fields.Date(string="Date", default=fields.Date.context_today)
    
    # THIS IS THE MISSING FIELD:
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ], string="Status", default='draft', tracking=True)

    def action_confirm(self):
        for record in self:
            record.state = 'confirmed'
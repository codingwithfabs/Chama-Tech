from odoo import fields, models, api

class MyContribution(models.Model):
    _name = 'chamatech.mycontribution'
    _description = 'My Contributions List'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    member_id = fields.Many2one('res.users', string="Member", default=lambda self: self.env.user, required=True, tracking=True)
    date = fields.Datetime(string="Date of Contribution", required=True, tracking=True, default=fields.Date.today)
    method = fields.Selection(selection=[("mpesa", "Mpesa"),
                                         ("card", "Card"),
                                         ("cash", "Cash")], string="Method of payment", required=True, tracking=True)
    
    amount = fields.Monetary(string="Amount", required=True)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Currency")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    transaction_id = fields.Char(string="M-Pesa Code", required=True, tracking=True)
    state = fields.Selection([
            ('draft', 'Draft'),
            ('pending', 'Pending Validation'),
            ('validated', 'Validated'),
            ('refused', 'Refused')
        ], string="Status", default='draft', tracking=True)
    
    _sql_constraints = [('unique_transaction_id', 'unique (transaction_id)', 'This M-Pesa code has already been used!')]

    def action_submit(self):
        for record in self:
            record.state = 'pending'

    def action_validate(self):
        for record in self:
            record.state = 'validated'

    def action_refuse(self):
        for record in self:
            record.state = 'refused'
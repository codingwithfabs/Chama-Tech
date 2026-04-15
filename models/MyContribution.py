from odoo import fields, models, api

class MyContribution(models.Model):
    _name = 'chamatech.mycontribution'
    _description = 'My Contributions List'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    date = fields.Datetime(string="Date of Contribution", required=True, tracking=True, default=fields.Date.today)
    method = fields.Selection(selection=[("mpesa", "Mpesa"),
                                         ("card", "Card"),
                                         ("cash", "Cash")], string="Method of payment", required=True, tracking=True)
    
    amount = fields.Monetary(string="Amount", required=True, tracking=True)
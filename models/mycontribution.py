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


    @api.model_create_multi
    def create(self, vals_list):
        # 1. Standard Odoo creation logic to save the user's contribution first
        records = super(MyContribution, self).create(vals_list)
        
        for record in records:
            # 2. Find the corresponding chamatech.member record that matches this res.user
            chama_member = self.env['chamatech.member'].search([('user_id', '=', record.member_id.id)], limit=1)
            
            if chama_member:
                # 3. Automatically inject/populate the record into the All Contributions table
                self.env['chamatech.chamatech'].create({
                    'member_id': chama_member.id,
                    'my_contribution_id': record.id, # Links them together
                    'amount': record.amount,
                    'date': record.date,
                    'description': f"M-Pesa Payment via Code: {record.transaction_id}",
                })
                
        return records
from odoo import fields, models, api, _

class MyContribution(models.Model):
    _name = 'chamatech.mycontribution'
    _description = 'My Contributions List'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

    def _get_default_member(self):
        """Safely fetches the active member profile linked to the logged-in user."""
        member = self.env['chamatech.member'].search([('user_id', '=', self.env.user.id)], limit=1)
        return member.id if member else False

    # Core Relational Fields
    member_id = fields.Many2one(
        'chamatech.member', 
        string="Member", 
        required=True, 
        tracking=True, 
        ondelete='cascade', 
        default=_get_default_member
    )
    company_id = fields.Many2one(
        'res.company', 
        string="Company", 
        required=True, 
        default=lambda self: self.env.company
    )
    currency_id = fields.Many2one(
        'res.currency', 
        related='company_id.currency_id', 
        string="Currency", 
        store=True
    )

    # Transaction Fields
    date = fields.Datetime(
        string="Date of Contribution", 
        required=True, 
        tracking=True, 
        default=fields.Datetime.now
    )
    method = fields.Selection(
        selection=[("mpesa", "M-Pesa"), ("card", "Card"), ("cash", "Cash")], 
        string="Method of Payment", 
        required=True, 
        tracking=True,
        default="mpesa"
    )
    amount = fields.Monetary(
        string="Amount", 
        required=True, 
        currency_field='currency_id', 
        tracking=True
    )
    transaction_id = fields.Char(
        string="M-Pesa Code", 
        required=True, 
        tracking=True
    )
    
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('pending', 'Pending Validation'),
            ('validated', 'Validated'),
            ('refused', 'Refused')
        ], 
        string="Status", 
        default='draft', 
        tracking=True
    )

    # Reverted to clean list constraints definition to fix initialization arguments error
    _sql_constraints = [
        ('unique_transaction_id', 'unique(transaction_id)', 'This M-Pesa code has already been used!')
    ]

    # Workflow Actions
    def action_submit(self):
        for record in self:
            record.state = 'pending'

    def action_validate(self):
        """Validates the contribution and automatically syncs it to the master registry."""
        for record in self:
            record.state = 'validated'
            
            # Auto-sync to the master registry (chamatech.chamatech) upon validation
            if record.member_id:
                initial_status = "goal_reached" if record.amount >= record.member_id.target_amount else "in_progress"
                
                self.env['chamatech.chamatech'].create({
                    'member_id': record.member_id.id,
                    'my_contribution_id': record.id,
                    'amount': record.amount,
                    'date': record.date,
                    'status': initial_status,
                    'description': f"M-Pesa Payment via Code: {record.transaction_id}",
                })

    def action_refuse(self):
        for record in self:
            record.state = 'refused'

    validated_amount = fields.Monetary(
    string="Validated Amount", 
    compute="_compute_validated_amount"
    )

    @api.depends('amount', 'state')
    def _compute_validated_amount(self):
        for record in self:
            if record.state == 'validated':
                record.validated_amount = record.amount
            else:
                record.validated_amount = 0.0
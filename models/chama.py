from odoo import models, fields, api


class ChamaTech(models.Model):
    _name = 'chamatech.chamatech'
    _description = 'Chama Master Registry'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "date desc"  # Changed order to date descending for better ledger sorting

    member_id = fields.Many2one(
        'chamatech.member', 
        string="Member Name", 
        required=True, 
        tracking=True,
        ondelete='cascade',
        default=lambda self: self.env['chamatech.member'].search([('user_id', '=', self.env.user.id)], limit=1)
    )

    my_contribution_id = fields.Many2one(
        'chamatech.mycontribution', 
        string="Original Submission", 
        ondelete='cascade'
    )

    amount = fields.Integer(string="Amount", required=True, tracking=True)
    description = fields.Text(string="Description", required=True, tracking=True)
    
    # Kept store=True so the list decoration tags can read the status values instantly
    status = fields.Selection(
        selection=[("in_progress", "In Progress"), ("goal_reached", "Goal Reached")],
        string="Status", 
        tracking=True, 
        compute="_compute_status", 
        store=True
    )

    date = fields.Datetime(
        string="Date of Contribution", 
        required=True, 
        tracking=True, 
        default=fields.Datetime.now  # Changed to Datetime.now since field type is Datetime
    )
    
    # Track the parent member's aggregate calculations and goals
    @api.depends('member_id.total_contributions', 'member_id.target_amount')
    def _compute_status(self):
        for record in self:
            # Compares the member's total running balance against their target goal
            if record.member_id and record.member_id.total_contributions >= record.member_id.target_amount:
                record.status = "goal_reached"
            else:
                record.status = "in_progress"
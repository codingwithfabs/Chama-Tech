from odoo import models, fields, api


class ChamaTech(models.Model):
    _name = 'chamatech.chamatech'
    _description = 'chamatech'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "amount desc"

    member_id = fields.Many2one(
        'chamatech.member', 
        string="Member Name", 
        required=True, 
        tracking=True,
        ondelete='cascade',
        default=lambda self: self.env['chamatech.member'].search([('user_id', '=', self.env.user.id)], limit=1)
    )

    my_contribution_id = fields.Many2one('chamatech.mycontribution', string="Original Submission", ondelete='cascade')

    amount = fields.Integer(string="Amount", required=True, tracking=True)
    description = fields.Text(string="Decription", required=True, tracking=True)
    status = fields.Selection(
        selection=[("in_progress", "In Progress"), ("goal_reached", "Goal Reached")],
        string="Status", 
        required=True, 
        tracking=True, 
        compute="_compute_status", 
        store=True,
        default="in_progress" # Added default fallback to bypass creation constraints
    )
    

    date = fields.Datetime(string="Date of Contribution", required=True, tracking=True, default=fields.Date.today)
    
    @api.depends('amount', 'member_id.target_amount')
    def _compute_status(self):
        for record in self:
            # Added structural fallbacks to ensure record always gets a value assigned
            if record.member_id and record.amount >= record.member_id.target_amount:
                record.status = "goal_reached"
            else:
                record.status = "in_progress"
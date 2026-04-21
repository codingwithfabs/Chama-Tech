# from odoo import http
# from odoo.http import request
# from odoo.addons.portal.controllers.portal import CustomerPortal

# class ChamaPortal(CustomerPortal):

#     def _get_home_portal_counts(self):
#         counts = super()._get_home_portal_counts()
#         # This is the line that actually feeds the XML the number
#         counts['contribution_count'] = request.env['chamatech.mycontribution'].search_count([
#             ('member_id', '=', request.env.user.id)
#         ])
#         return counts

#     @http.route(['/my/contributions'], type='http', auth="user", website=True)
#     def portal_my_contributions(self):
#         values = self._prepare_portal_layout_values()
#         contributions = request.env['chamatech.mycontribution'].search([
#             ('member_id', '=', request.env.user.id)
#         ])
#         values.update({
#             'contributions': contributions,
#             'page_name': 'my_contributions',
#         })
#         return request.render("chama_tech.portal_my_contributions_list", values)
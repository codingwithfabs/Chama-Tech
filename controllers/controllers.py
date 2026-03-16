# from odoo import http


# class Chama-tech(http.Controller):
#     @http.route('/chama-tech/chama-tech', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/chama-tech/chama-tech/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('chama-tech.listing', {
#             'root': '/chama-tech/chama-tech',
#             'objects': http.request.env['chama-tech.chama-tech'].search([]),
#         })

#     @http.route('/chama-tech/chama-tech/objects/<model("chama-tech.chama-tech"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('chama-tech.object', {
#             'object': obj
#         })


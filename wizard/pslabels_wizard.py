# -*- coding: utf-8 -*-

from openerp import models, fields, api

class WizardLine(models.TransientModel):
    _name = "pslabels.wizard.line"
    _rec_name = "product_id"
    product_id = fields.Many2one("product.product", string="Variante", required=True)
    quantity = fields.Float("Cantidad", digits=0, required=True)
    wizard_id = fields.Many2one("pslabels.wizard", string="Wizard")

class Wizard(models.TransientModel):
    _name = "pslabels.wizard"

    def _default_product_template(self):
        return self.env['product.template'].browse(self._context.get('active_id'))

    product_template_id = fields.Many2one('product.template', string="Producto", required=True, default=_default_product_template)

    to_skip = fields.Integer(string="Saltar etiquetas:", default=0)

    product_quantities = fields.One2many('pslabels.wizard.line', 'wizard_id', 'Cantidades')

    @api.model
    def default_get(self, fields):
        product_template_id = self.env['product.template'].browse(self.env.context.get('active_id'))
        res = super(Wizard, self).default_get(fields)
        product_quantities = []
        for product in product_template_id.product_variant_ids:
            product_quantities.append((0, 0, {'product_id': product.id, 'quantity': product.incoming_qty, }))
            res.update({'product_quantities': product_quantities})
        return res


    @api.multi
    def print_labels(self):
        datas = {'ids': self.env.context.get('active_ids', [])}
        res = self.read(['product_template_id', 'to_skip', 'product_quantities'])
        res = res and res[0] or {}
        res['product_template_id'] = res['product_template_id'][0]
        res['texto'] = 'hola';
        datas['form'] = res
        return self.env['report'].get_action([], 'pslabels.report_pslabels_view2', data=datas)
    # def print_labels(self):
    #     value =  {
    #         'type': 'ir.actions.report.xml',
    #         'report_name':'pslabels.report_pslabels_view',
    #         'datas': {
    #             'model':'product.template',
    #             'id': self.product_template_id.id,
    #             # 'id': ids and ids[0] or False,
    #             # 'ids': ids and ids or [],
    #             'report_type': 'pdf'
    #         },
    #         'nodestroy': True
    #     }
    #     return value
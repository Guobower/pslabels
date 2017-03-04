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

    label_type = fields.Selection([('pslabels.report_pslabels_7024', '70x42.3mm'), ('pslabels.report_pslabels_10574', '105x74mm')], string="Tipo de etiqueta")

    pre_product_name = fields.Char(string="Prefijo nombre produco", help="Corresponde con el parámetro de sistema 'pslabels_pre_product_name'")

    to_skip = fields.Integer(string="Saltar etiquetas:", default=0)

    product_quantities = fields.One2many('pslabels.wizard.line', 'wizard_id', 'Cantidades')

    @api.model
    def default_get(self, fields):
        product_template_id = self.env['product.template'].browse(self.env.context.get('active_id'))
        res = super(Wizard, self).default_get(fields)
        product_quantities = []
        for product in product_template_id.product_variant_ids:
            product_quantities.append((0, 0, {'product_id': product.id, 'quantity': product.incoming_qty, }))

        conf = self.env['ir.config_parameter']
        pre_product_name = conf.get_param('pslabels_pre_product_name')
        res.update({'product_quantities': product_quantities, 'pre_product_name': pre_product_name, 'label_type': 'pslabels.report_pslabels_7024'})
        return res


    @api.multi
    def print_labels(self):
        product_qty_pairs = map(lambda p: {'product_id': p.product_id.id, 'qty': p.quantity}, self.product_quantities)
        datas = {'ids': self.env.context.get('active_ids', []),
                 'product_template_id': self.product_template_id[0].id,
                 'label_type': self.label_type,
                 'pre_product_name': self.pre_product_name,
                 'to_skip': self.to_skip,
                 'product_qty_pairs': product_qty_pairs}
        return self.env['report'].get_action([], self.label_type, data=datas)

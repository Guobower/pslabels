# -*- coding: utf-8 -*-

from openerp import models, fields, api

class PSLabelsReport1(models.AbstractModel):
    _name = "report.pslabels.report_pslabels_7024"

    labels_per_page = 18
    template_name = 'pslabels.report_pslabels_view_7024'

    def expand_product(self, wizard_product):
        expanded = self.env['product.product'].browse(wizard_product['product_id']);

        # talla_attr = next((a for a in expanded.attribute_value_ids if a.attribute_id.name == 'Talla'), None)
        # expanded.talla = talla_attr.name if talla_attr else '*'

        expanded.size = ''
        expanded.style = ''
        for a in expanded.attribute_value_ids:
            if a.attribute_id.name == 'Talla':
                expanded.exp_size = '- T' + a.name
            elif a.attribute_id.name == 'Color Etiqueta':
                expanded.exp_color = 'padding-top: 1mm; width: 5mm; height: 5mm; border-radius: 50%%; display: inline-block; background-color: %s;' % a.name[:7]
            else:
                expanded.exp_style = expanded.style + a.name + ' '

        return expanded

    @api.model
    def render_html(self, docids, data=None):
        data = data if data is not None else {}
        docids = data.get('ids')

        product_qty_lists = map(lambda p: [self.expand_product(p)] * p['qty'], data['product_qty_pairs'])
        products = ([{}] * data['to_skip']) + reduce(list.__add__, product_qty_lists)
        pages = (products[i:i + self.labels_per_page] for i in range(0, len(products), self.labels_per_page))
        pre_product_name = data['pre_product_name']

        docargs = {
            'doc_ids': docids,
            'doc_model': 'product.template',
            'docs': pages,
            'pre_product_name': pre_product_name
        }
        return self.env['report'].render(self.template_name, docargs)


class PSLabelsReport2(models.AbstractModel):
    _name = "report.pslabels.report_pslabels_10574"

    labels_per_page = 8
    template_name = 'pslabels.report_pslabels_view_10574'

    @api.model
    def render_html(self, docids, data=None):
        data = data if data is not None else {}
        docids = data.get('ids')

        product_qty_lists = map(lambda p: [self.env['product.product'].browse(p['product_id'])] * p['qty'], data['product_qty_pairs'])
        products = ([{}] * data['to_skip']) + reduce(list.__add__, product_qty_lists)
        pages = (products[i:i + self.labels_per_page] for i in xrange(0, len(products), self.labels_per_page))
        pre_product_name = data['pre_product_name']

        docargs = {
            'doc_ids': docids,
            'doc_model': 'product.template',
            'docs': pages,
            'pre_product_name': pre_product_name
        }
        return self.env['report'].render(self.template_name, docargs)

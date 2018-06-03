# -*- coding: utf-8 -*-

from openerp import models, fields, api

class PSLabelsReport1(models.AbstractModel):
    _name = "report.pslabels.report_pslabels_7024"

    labels_per_page = 18
    template_name = 'pslabels.report_pslabels_view_7024'

    def extend_product(self, wizard_product):
        extended = self.env['product.product'].browse(wizard_product['product_id']);

        extended.size = ''
        extended.style = ''
        for a in extended.attribute_value_ids:
            if a.attribute_id.name == 'Talla':
                extended.exp_size = a.name
            elif a.attribute_id.name == 'Color Etiqueta':
                extended.exp_color = 'font-weight: bold; font-size: x-large; width: 9mm; height: 9mm; border-radius: 50%%; display: inline-block; color: white; background-color: %s;' % a.name[:7]
            else:
                extended.exp_style = extended.style + a.name + ' '

        return extended

    @api.model
    def render_html(self, docids, data=None):
        data = data if data is not None else {}
        docids = data.get('ids')

        product_qty_lists = map(lambda p: [self.extend_product(p)] * p['qty'], data['product_qty_pairs'])

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

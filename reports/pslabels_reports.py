# -*- coding: utf-8 -*-

from openerp import models, fields, api

class PSLabelsReport(models.AbstractModel):
    _name = "report.pslabels.report_pslabels_view"

    labels_per_page = 18
    @api.model
    def render_html(self, docids, data=None):
        data = data if data is not None else {}
        docids = data.get('ids')
        product_qty_lists = map(lambda p: [self.env['product.product'].browse(p['product_id'])] * p['qty'], data['product_qty_pairs'])
        products = ([{}] * data['to_skip']) + reduce(list.__add__, product_qty_lists)
        pages = (products[i:i+self.labels_per_page] for i in xrange(0, len(products), self.labels_per_page))

        docargs = {
            'doc_ids': docids,
            'doc_model': 'product.template',
            'docs': pages,
        }
        return self.env['report'].render('pslabels.report_pslabels_view', docargs)

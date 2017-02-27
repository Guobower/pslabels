# pslabels
## Odoo 10 addon to print EAN13 labels

Adds a menu on product page which prints EAN13 labels for product variants.

For now it's fixed to 70mmx42.mm labels (21 labels on A4 paper, where the first 3 are skipped to avoid printer margin problems). It can be easily changed by editing the report files.

It's better to define a new paper format, A4 without margins, an to associate it to the report.

A system parameter named 'pslabels_pre_product_name' can be defined to specify a default prefix text to be printed just before the product name. This can be customized on a per print basis.


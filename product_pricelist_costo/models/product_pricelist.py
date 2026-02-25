from odoo import models
from odoo.tools.float_utils import float_round


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    @staticmethod
    def _extract_product_from_price_rule_line(line):
        """Handle different method signatures across Odoo versions.

        `_compute_price_rule` can receive either:
        - tuples like (product, qty, partner)
        - tuples where product is still the first value
        - bare product records
        """
        if isinstance(line, tuple):
            return line[0] if line else False
        return line

    def _compute_price_rule(self, products_qty_partner, *args, **kwargs):
        # In newer versions this argument can be an iterable of product records,
        # and in some call paths it can be a one-shot iterator. Reuse a concrete
        # list so we can inspect the values after calling `super()`.
        lines = list(products_qty_partner)
        prices = super()._compute_price_rule(lines, *args, **kwargs)

        rule_ids = []
        for price_data in prices.values():
            if len(price_data) >= 2 and price_data[1]:
                rule_ids.append(price_data[1])
        rules = self.env["product.pricelist.item"].browse(rule_ids)
        cost_rules = {rule.id: rule for rule in rules if rule.compute_price == "costo"}

        if not cost_rules:
            return prices

        for line in lines:
            product = self._extract_product_from_price_rule_line(line)
            if not product:
                continue
            product_data = prices.get(product.id)
            if not product_data:
                continue
            _price, rule_id = product_data
            cost_rule = cost_rules.get(rule_id)
            if cost_rule:
                prices[product.id] = (
                    float_round(cost_rule._compute_costo_price(), precision_digits=3),
                    rule_id,
                )

        return prices

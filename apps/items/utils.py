from .models import ProductImage
def calc_final_price(base_price, earning, vat):
    price_w_earnings = base_price + (base_price * earning/100)
    vat = base_price * vat
    final_price = price_w_earnings + vat
    return final_price

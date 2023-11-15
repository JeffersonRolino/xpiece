from decimal import Decimal

from django.conf import settings

from shop.models import Product


class Cart:
    def __init__(self, request):
        """
        Inicializando Carrinho de Compras
        O carrinho será armazenado nas sessões
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product):
        """
        Adiciona um produto no carrinho.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'product': str(product.name), 'price': str(product.price)}
        else:
            pass
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        """
        Remove Produto do carrinho baseado no ID
        """
        product_id = str(product.id)
        del self.cart[product_id]
        self.save()

    def clear(self):
        """
        Remove carrinho da sessão
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        """
        Retorna o valor total do carrinho
        """
        return sum(Decimal(item['price']) for item in self.cart.values())

    def __iter__(self):
        """
        Iterable padrão da classe.
        Itera sobre os items no carrinho e pega
        os produtos do banco de dados.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            yield item

    def __len__(self):
        return len(self.cart.values())

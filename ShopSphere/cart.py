class Cart:
   
   def __init__(self, request):
       """Initialize the cart with the session"""
       self.session = request.session
       cart = self.session.get("cart")
       if not cart:
           cart = self.session["cart"] = {}  # Create empty cart
       self.cart = cart

   def add(self, product, quantity=1):
       """Add a product to the cart or update its quantity"""
       product_id = str(product.id)
       if product_id in self.cart:
           self.cart[product_id]["quantity"] += quantity
       else:
           self.cart[product_id] = {
               "id": product_id,
               "name": product.name,
               "price": str(product.price),
               "quantity": quantity,
           }
       self.save()

   def remove(self, product):
       """Remove a product from the cart"""
       product_id = str(product.id)
       if product_id in self.cart:
           del self.cart[product_id]
           self.save()

   def save(self):
       """Save cart to session"""
       self.session.modified = True

   def clear(self):
       """Remove all items from the cart"""
       self.session["cart"] = {}
       self.session.modified = True

   def __iter__(self):
       """Iterate over items in the cart"""
       for item in self.cart.values():
           yield item

   def total_price(self):
       """Calculate total price"""
       return sum(float(item["price"]) * item["quantity"] for item in self.cart.values())
   
   def __len__(self):
       """Count total items in the cart"""
       return sum(item["quantity"] for item in self.cart.values())
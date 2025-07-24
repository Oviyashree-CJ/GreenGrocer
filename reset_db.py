from app import app
from models import db, Product

with app.app_context():
    # Drop all existing tables
    db.drop_all()
    print("✅ Tables dropped.")

    # Create all tables again
    db.create_all()
    print("✅ Tables created.")

    # Seed updated product list
    sample_products = [
            Product(name="Fresh Tomatoes", category="Vegetables", price=20, description="Fresh red tomatoes - 1 kg", image_url="tomato.jpeg"),
            Product(name="Organic Carrots", category="Vegetables", price=20, description="Organic  carrots - 1 kg bag", image_url="carrot.jpeg"),
            Product(name="Green Capsicum", category="Vegetables", price=20, description="Fresh green capsicum - 500g", image_url="green capsicum.jpeg"),
            Product(name="Cauliflower", category="Vegetables", price=50, description="Fresh cauliflower - 1 flower", image_url="cauliflower.jpeg"),
            Product(name="Beans", category="Vegetables", price=150, description="Fresh beans - 1Kg", image_url="beans.jpeg"),
            Product(name="Yellow Red Capsicum ", category="Vegetables", price=60, description="Fresh capsicum  packed with both color", image_url="capsicum.jpeg"),
            Product(name="Onion", category="Vegetables", price=40, description="Fresh onions - 1Kg", image_url="onion.jpeg"),
            Product(name="Curry Leaves", category="Vegetables", price=3, description="Fresh curry leaves", image_url="curry_leaves.jpeg"),
            Product(name="Coriander Leaves", category="Vegetables", price=5, description="Fresh coriander leaves", image_url="coriander_leaves.jpeg"),
            Product(name="Green onion", category="Vegetables", price=60, description="Fresh green onion - 1 kg pack", image_url="green onion.jpeg"),
            Product(name="Cucumber", category="Vegetables", price=60, description="Fresh cucumber packed with -5 ", image_url="cucumber.jpeg"),
            Product(name="Red chili", category="Vegetables", price=10, description="Fresh red chili 100g ", image_url="red chili.jpeg"),
            Product(name="Green chili", category="Vegetables", price=10, description="Fresh red chili 100g ", image_url="green chili.jpeg"),
            Product(name="Fresh Bananas", category="Fruits", price=100, description="Yellow bananas - 1 kg bunch(10 pieces)", image_url="banana.jpeg"),
            Product(name="Red Apples", category="Fruits", price=200, description="Crisp red apples - 1 kg bag", image_url="apple.jpeg"),
            Product(name="Fresh Oranges", category="Fruits", price=100, description="Juicy naval oranges - 1 kg bag", image_url="orange.jpeg"),
            Product(name="Fresh Guavas", category="Fruits", price=100, description="Juicy and fresh guavas - 1 kg bag", image_url="guava.jpeg"),
            Product(name="Strawberries", category="Fruits", price=240, description="Fresh strawberries - 500g container", image_url="strawberry.jpeg"),
            Product(name="BlueBerry", category="Fruits", price=540, description="Fresh Blueberry - 500g container", image_url="blue berry.jpeg"),
            Product(name="Raspberry", category="Fruits", price=600, description="Fresh Raspberry - 500g container", image_url="rasberry.jpeg"),
            Product(name="pear", category="Fruits", price=140, description="Fresh pear - 1kg", image_url="pear.jpeg"),
            Product(name="Pomegranate", category="Fruits", price=190, description="Fresh Pomegranate - 1kg", image_url="pome.jpeg"),
            Product(name="Pineapple", category="Fruits", price=40, description="Fresh Pineapples - 1Kg", image_url="pine.jpeg"),
            Product(name="Mango", category="Fruits", price=100, description="Fresh Mangoes - 1Kg", image_url="mango.jpeg"),
            Product(name="Arokya", category="Dairy", price=38, description="Full Cream milk - 500ml", image_url="milk aarokya.jpeg"),
            Product(name="Cheddar Cheese", category="Dairy", price=185, description="Sharp cheddar cheese - 250g block", image_url="cheese.jpeg"),
            Product(name="Paneer", category="Dairy", price=435, description="Fresh white paneer - 1 kg container", image_url="panner.jpeg"),
            Product(name="Butter", category="Dairy", price=220, description="Unsalted butter - 500g pack", image_url="butter.jpg"),
            Product(name="Greek yogurt ", category="Dairy", price=50, description="Greek yogurt- 500ml", image_url="greek_yogurt.jpeg"), 
            Product(name=" yogurt ", category="Dairy", price=40, description=" yogurt- 500ml", image_url="yogurt.jpeg"),    
            Product(name="Curd ", category="Dairy", price=10, description="curd- 100ml", image_url="curd.jpeg"),
            Product(name="Ghee ", category="Dairy", price=350, description="Ghee- 500ml", image_url="ghee.jpeg"),
            Product(name="Chocolate Ice cream ", category="Dairy", price=270, description="Chocolate Ice cream- 500ml", image_url="choco_ice.jpeg"), 
            Product(name="Strawberry Ice cream ", category="Dairy", price=190, description="Strawberry Ice cream- 500ml", image_url="strawberry_ice.jpeg"),
            Product(name="Vanilla Ice cream ", category="Dairy", price=170, description="Vanilla Ice cream- 500ml", image_url="vanilla_ice.jpeg"),
            Product(name="Butterscotch Ice cream ", category="Dairy", price=250, description="Butterscotch Ice cream- 500ml", image_url="butterscotch_ice.jpeg"),        
            Product(name="Orange Juice", category="Beverages", price=80, description="Fresh orange juice - 1 liter carton", image_url="orange_juice.jpeg"),
            Product(name="Sparkling Water", category="Beverages", price=50, description="Sparkling water - 2 liter bottle", image_url="spark_water.png"),
            Product(name="Green Tea", category="Beverages", price=350, description="Organic green tea bags - 250g box", image_url="green_tea.jpeg"),
            Product(name="Sprite", category="Beverages", price=30, description="Cool drink Sprite", image_url="spirit.jpeg"),
            Product(name="7up", category="Beverages", price=50, description="Cool drink 7up", image_url="7up.jpeg"),
            Product(name="Pepsi", category="Beverages", price=40, description="Cool drink pepsi", image_url="pepsi.jpeg"),
            Product(name="Chocolate milkshake", category="Beverages", price=28, description="Chocolate MilkShake", image_url="choco_milk.jpeg"),
            Product(name="Strawberry milkshake", category="Beverages", price=30, description="Strawberry MilkShake", image_url="strawberry_milk.jpeg"),
            Product(name="Cold coffee", category="Beverages", price=40, description="Cold Coffee with wonderful icing flavour", image_url="cold_coffee.jpeg"),
            Product(name="Cavin's Milkshake Combo", category="Beverages", price=90, description="Cool offer milkshake with 4 different flavors", image_url="combomilk.jpeg"),
            Product(name="Thumbsup", category="Beverages", price=50, description="Cool drink Thumbsup", image_url="thumbs_up.jpeg"),
            Product(name="Bovonto", category="Beverages", price=45, description="Cool drink Bovonto", image_url="bovonto.jpeg"),
            Product(name="Coffee Beans", category="Beverages", price=400, description="Premium coffee beans - 500g bag", image_url="coffee_bean.jpeg"),
            Product(name="potazos", category="Snacks", price=20, description="Original potato biscuit - 250g pack", image_url="potazo.jpg"),
            Product(name="Pringles", category="Snacks", price=120, description="Toasted pringles - 450g container", image_url="pringles red.jpg"),
            Product(name="Red Hot Lays", category="Snacks", price=20, description="Sizzlin Hot Potato Chips - 24g packet", image_url="hot red lays.jpg"),
            Product(name="Doritos", category="Snacks", price=20, description="Nacho cheese Tortilla chips - 24g packet", image_url="dorito.jpg"),
            Product(name="Green Lays", category="Snacks", price=20, description="chili and lemon mixed flavored Potato Chips - 24g packet", image_url="green lays.jpg"),
            Product(name="Little Hearts", category="Snacks", price=20, description="Britannia's classic biscuit - 24g packet", image_url="little heart.jpg"),
            Product(name="Marie Gold", category="Snacks", price=20, description="Britannia's Gold biscuit - 120g packet", image_url="marie gold bis4.jpg"),
            Product(name="Mixture Namkeen", category="Snacks", price=20, description="Groundnut and spices mixed snack - 40g packet", image_url="old snacks.jpg"),
            Product(name="Red Lays", category="Snacks", price=20, description="Tomato Tango Potato Chips - 24g packet", image_url="red lays.jpg"),
            Product(name="Treat", category="Snacks", price=20, description="Cream loaded sandwich biscuit - 100g packet", image_url="treat.jpg"),
            Product(name="Vita", category="Snacks", price=30, description="Nutrition biscuit - 100g packet", image_url="vita bis 5.jpg"),
            Product(name=" Honey Barbecue Lays", category="Snacks", price=20, description="honey flavored with barbecue Potato Chips - 24g packet", image_url="yellow lays.jpg"),
            Product(name="Black Pepper", category="Spices", price=220, description="Ground black pepper - 50g shaker", image_url="black_pep.jpeg"),
            Product(name="Sea Salt", category="Spices", price=130, description="Fine sea salt - 100g container", image_url="sea_salt.jpeg"),
            Product(name="Garlic Powder", category="Spices", price=100, description="Pure garlic powder - 75g shaker", image_url="gar_powder.jpeg"),
            Product(name="Italian Herbs", category="Spices", price=100, description="Italian herb blend - 30g container", image_url="it_herbs.jpeg"),
            Product(name="Garam masala", category="Spices", price=30, description="Garam masala - 100g pack", image_url="garam_masala.jpeg"),
            Product(name="Mutton masala", category="Spices", price=30, description="AACHI Mutton masala - 100g pack", image_url="mutton_masala.jpeg"),
            Product(name="Clove", category="Spices", price=10, description="Clove - 30g", image_url="clove.jpeg"),
            Product(name="Bay leaves", category="Spices", price=10, description="Bay leaves - 20g", image_url="bay_leaf.jpeg"),
            Product(name="Chicken masala", category="Spices", price=30, description="AACHI Chicken masala - 50g pack", image_url="chicken_masala.jpeg"),
            Product(name="Ceylon Cinnamon", category="Spices", price=150, description="Ceylon Cinnamon with rich flavour ", image_url="cinna.jpeg"),
            Product(name="Aachi combo offer powder", category="Spices", price=100, description="3 packs of aachi different flavoured powder - 100g pack", image_url="combopowder.jpeg"),
            Product(name="Hand Soap", category="Personal Care", price=80, description="Antibacterial hand soap - 350ml pump", image_url="hand_soap.jpeg"),
            Product(name="Shampoo", category="Personal Care", price=140, description="Daily shampoo - 500ml bottle", image_url="clinic.jpeg"),
            Product(name="Toothpaste", category="Personal Care", price=90, description="Fluoride toothpaste - 150g tube", image_url="col.png"),
            Product(name="Toothbrush", category="Personal Care", price=20, description=" Toothbrush with soft technology - 1 tooth brush", image_url="toothbrush.jpeg"),
            Product(name="Dish washer", category="Personal Care", price=90, description="Dish washer with combo offer of 4 different smell", image_url="dish_washer.jpeg"),
            Product(name="Detergent", category="Personal Care", price=100, description="Ariel Detergent  ", image_url="detergent.jpeg"),
            Product(name="Wipes", category="Personal Care", price=20, description="Soft and Moisture Wipes ", image_url="wipes.jpeg"),
            Product(name="Body Lotion", category="Personal Care", price=300, description="Moisturizing body lotion - 350ml bottle", image_url="body_lotion.jpeg"),
            Product(name="Broom Stick", category="Personal Care", price=150, description="Easy to handle and cleaning is extraordinary with comfort", image_url="broom.jpeg")
    ]




    db.session.bulk_save_objects(sample_products)
    db.session.commit()
    print("✅ Sample products seeded.")
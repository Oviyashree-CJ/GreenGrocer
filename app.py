import os
import logging

from flask import Flask
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv
from models import db, Product, Benefit
from flask_migrate import Migrate

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__, static_folder='static')
app.secret_key = os.environ.get("SESSION_SECRET")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)


with app.app_context():

    # Create tables
    db.create_all()

    # Seed sample products if none exist
    if Product.query.count() == 0:
        sample_products = [
            Product(name="Fresh Tomatoes", category="Vegetables", price=20, description="Fresh red tomatoes - 1 kg", image_url="tomato.jpeg"),
            Product(name="Organic Carrots", category="Vegetables", price=20, description="Organic  carrots - 1 kg bag", image_url="carrot.jpeg"),
            Product(name="Green Capsicum", category="Vegetables", price=20, description="Fresh green capsicum - 500g", image_url="capsicum.jpeg"),
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


        for product in sample_products:
           db.session.add(product)
        db.session.commit()
        logging.info("Sample products initialized")
    
    
    sample_benefits = [
        {
            "product_name": "Onion",
            "nutrition": "Fiber 11.7%, Manganese 16%, Biotin 26.6%, Vitamin B6 15.8%, Vitamin C 14.5%, Potassium 9.9%",
            "health_benefits": "Anti-inflammatory, anti-bacterial, improves blood sugar balance, supports bone and connective tissue, fights cancer, enhances brain and eye health."
        },
        {
            "product_name": "Fresh Tomatoes",
            "nutrition": "Vitamin C, Vitamin K, Vitamin B, High in fiber, 0.2g fat, Low in calories, Rich in antioxidants",
            "health_benefits": "Promotes weight loss, provides essential nutrients, supports heart and immune health."
        },
        {
            "product_name": "Organic Carrots",
            "nutrition": "Dietary Fiber 12%, Carbohydrates 3%, Calories 2%, Protein 1%, Vitamin A 276%, Vitamin K 12%, Folate 7%, Vitamin B6 5%, Manganese 8%, Potassium 7%, Copper 5%, Iron 5%",
            "health_benefits": "Improves eyesight, prevents heart diseases, reduces high blood pressure, maintains good digestive health, boosts immune system, regulates blood sugar levels, prevents macular degeneration, reduces risk of cancer and stroke."
        },
        {
            "product_name": "Green Capsicum",
            "nutrition": "Protein 1g, Carbohydrates 6g, Fiber 2.1g, Water 92%, Fat 0.3g, Sugar 4.2g",
            "health_benefits": "Improves blood circulation, treats skin infection, contains anti-bacterial agents, promotes hair health, removes signs of ageing skin, supports immune system, boosts eye health."
        },
        {
            "product_name": "Cauliflower",
            "nutrition": "Calories 25 KCAL, Protein 1.9g, Fiber 2g, Carbohydrates 4.9g",
            "health_benefits": "Rich in vitamins and minerals, supports heart health, supports digestion, promotes weight loss."
        },
        {
            "product_name": "Beans",
            "nutrition": "Vitamin C, Vitamin A, Vitamin K, Folate, Manganese, Fiber",
            "health_benefits": "Regulates blood sugar, has anti-inflammatory properties, promotes healthy skin, aids hydration, and provides dietary fiber."
        },
        {
            "product_name": "Green onion",
            "nutrition": "Calories 32, Fibre 2.6g, Copper 0.08mg, Iron 1.48g, Protein 1.8g, Calcium 72mg, Carbohydrates 7.3g, Magnesium 20mg, Fat 0.4g, Potassium 276mg",
            "health_benefits": "Boosts immune system, maintains heart health, relaxes muscle cramps, aids digestion, fortifies bones and joints, benefits eye and skin health, aids in weight loss."
        },
        {
            "product_name": "Cucumber",
            "nutrition": "Calories 15 KCAL, Carbohydrates 3.63g, Fat 0.11g, Protein 0.65g, Vitamin C 2.8mg, Vitamin K 16.4mg, Potassium 147mg, Magnesium 13mg, Calcium 16mg, Iron 0.28mg",
            "health_benefits": "Prevents acne, hydrates the skin, treats sunburn, rich in antioxidants, reduces dark circles, lightens skin, reduces swelling, tightens the skin."
        },
        {
            "product_name": "Green chili",
            "nutrition": "Vitamin A 19%, Vitamin C 239%, Vitamin B6 25%, Potassium 9%, Iron 5%",
            "health_benefits": "Boosts digestion, helps in weight loss, keeps heart healthy, protects against cancer."
        },
        {
            "product_name": "Red chili",
            "nutrition": "Vitamin A, Vitamin B, Vitamin C, Vitamin E, Antioxidants",
            "health_benefits": "Helps to absorb iron, manages blood pressure, relieves congestion, good source of vitamin C."
        },
        {
            "product_name": "Fresh Bananas",
            "nutrition": "Calories 110, Fat 0g, Protein 1g, Carbs 28g, Sugar 15g, Fibre 3g, Potassium 450mg",
            "health_benefits": "Improves digestion and kidney function, improves heart health, boosts energy, reduces inflammation, strengthens bones."
        },
        {
            "product_name": "Red Apples",
            "nutrition": "Calories 52, Water 86%, Protein 0.3g, Carbs 13.8g, Sugar 10.4g, Fiber 2.4g, Fat 0.2g, Sodium 1mg, Potassium 107mg, Vitamin C 7%",
            "health_benefits": "Provides bone protection, helps with asthma, prevents lung, breast, colon, and liver cancer, lowers cholesterol, aids in weight loss."
        },
        {
            "product_name": "Fresh Oranges",
            "nutrition": "Calories 60, Fibre 3g, Sugar 12g, Protein 1g, Vitamin A 14mg, Vitamin C 70mg, Potassium 237mg, Carbohydrates 15.4g",
            "health_benefits": "Boosts immunity, lowers cholesterol level, supports heart health, reduces risk of colon cancer, prevents skin damage and aging, helps control blood pressure."
        },
        {
            "product_name": "Fresh Guavas",
            "nutrition": "Vitamin C 396%, Pyridoxin 8.5%, Folates 12.5%, Vitamin A 21%, Iron 3%, Magnesium 5.5%, Copper 2.5%",
            "health_benefits": "Good for brain, improves vision, protects skin from damage, lowers blood sugar level, aids digestion."
        },
        {
            "product_name": "Strawberries",
            "nutrition": "Vitamin C 58.8mg, Vitamin E 0.3mg, Vitamin B3 0.4mg, Vitamin B4 5.7mg, Vitamin B5 0.125mg, Vitamin B6 0.47mg, Vitamin B9 24.9mg",
            "health_benefits": "Strengthens teeth, great for eyes, boosts immunity, promotes hair growth, improves brain health, reduces inflammation."
        },
        {
            "product_name": "BlueBerry",
            "nutrition": "Vitamin C, Vitamin K, Calories 57, Proteins 0.7g, Fibre 2.4g, Carbs 14.5g",
            "health_benefits": "High in antioxidants, helps in weight loss, alleviates inflammation, promotes heart health, helps fight cancer, boosts brain health, supports digestion."
        },
        {
            "product_name": "Raspberry",
            "nutrition": "Proteins 1.5g, Fat 0.08g, Calories 64, Carbs 14.7g, Fibre 8g",
            "health_benefits": "Boosts immune system, rich in antioxidants, helps to burn fat, has anti-aging properties, aids in cancer prevention."
        },
        {
            "product_name": "pear",
            "nutrition": "Calories 101, Fibre 5.5g, Carbs 27g, Fat 0.3g, Protein 0.6g",
            "health_benefits": "Boosts heart health, helps to manage body weight, lowers the risk of diabetes, has anti-cancer effects, promotes digestive health."
        },
        {
            "product_name": "Pomegranate",
            "nutrition": "Vitamin K 21%, Vitamin C 17%, Thiamin 4%, Folate 10%, Potassium 7%, Copper 8%",
            "health_benefits": "Repairs sun-damaged skin, reduces wrinkles, strengthens immune system, supports good digestion, reduces redness and swelling, protects from toxins."
        },
        {
            "product_name": "Pineapple",
            "nutrition": "Protein 0.9g, Fibre 2.4g, Calories 82, Carbs 22g, Fat 0.2g",
            "health_benefits": "Fights many diseases, rich in antioxidants, helps to break down food, maintains strong bones, prevents cough and colds, reduces hypertension."
        },
        {
            "product_name": "Mango",
            "nutrition": "Vitamin C 46%, Vitamin E 75%, Vitamin A 25.5%, Copper 12%, Calcium 1%",
            "health_benefits": "Regulates blood pressure, improves digestion, helps fight heat strokes, boosts the immune system, helps with diabetes, improves eye health, clears the skin, lowers cholesterol."
        }
    ]



    for benefit in sample_benefits:
        product = Product.query.filter_by(name=benefit["product_name"]).first()
        if product:
            existing = Benefit.query.filter_by(product_id=product.id).first()
            if not existing:  # Prevent duplicate insert
                new_benefit = Benefit(
                    product_id=product.id,
                    nutrition=benefit["nutrition"],
                    health_benefits=benefit["health_benefits"]
                )
                db.session.add(new_benefit)

    db.session.commit()
    logging.info("Sample benefits initialized")




# Import routes at the end to avoid circular imports
#  # noqa: F401, F403
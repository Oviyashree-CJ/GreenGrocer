from flask import render_template, request, redirect, url_for, flash, session, jsonify
from twilio.rest import Client
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import joinedload
from app import app, db
from models import User, Product, CartItem, Order, OrderItem, Benefit
from utils import validate_password
import os, logging
from dotenv import load_dotenv
from datetime import datetime
import pytz

# Load env variables
load_dotenv()

# Initialize Twilio client
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
client = Client(account_sid, auth_token)


@app.route('/')
def index():
    """Homepage with featured products and categories"""
    categories = ['Vegetables', 'Fruits', 'Dairy', 'Beverages', 'Snacks', 'Spices', 'Personal Care']
    featured_products = Product.query.limit(8).all()
    return render_template('index.html', categories=categories, featured_products=featured_products)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        new_password = request.form['new_password']
        
        user = User.query.filter_by(username=username, email=email).first()
        
        if user:
            user.password_hash = generate_password_hash(new_password)
            db.session.commit()
            flash('Password updated successfully. You can now log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Invalid username or email.', 'danger')
    
    return render_template('forgot_password.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')
        
        if not validate_password(password):
            flash('Password must be at least 4 characters with exactly 2 numbers and no special characters.', 'danger')
            return render_template('register.html')
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return render_template('register.html')
        
        # Create new user
        user = User(username=username, email=email, login="No")
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            user.login = "Yes"
            session['user_id'] = user.id
            session['username'] = user.username
            db.session.commit() 
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """User logout"""
    user_id = session.get('user_id')
    
    if user_id:
        user = User.query.get(user_id)
        if user:
            user.login = "No"
            db.session.commit()
    
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))



@app.route('/products')
@app.route('/products/<category>')
def products(category=None):
    """Products page with category filtering"""
    categories = ['Vegetables', 'Fruits', 'Dairy', 'Beverages', 'Snacks', 'Spices', 'Personal Care']
    
    if category:
        products = Product.query.options(joinedload(Product.benefits)).filter_by(category=category).all()
    else:
        products = Product.query.options(joinedload(Product.benefits)).all()
    
    return render_template('products.html', products=products, categories=categories, current_category=category)

@app.route('/get_benefits/<item_name>')
def get_benefits(item_name):
    product = Product.query.filter_by(name=item_name).first()
    if product and product.benefits:
        benefit_data = {
            "nutrition": product.benefits[0].nutrition,
            "health_benefits": product.benefits[0].health_benefits
        }
        return jsonify(benefit_data)
    return jsonify({"error": "No benefits found"}), 404

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    """Add product to cart"""
    if 'user_id' not in session:
        flash('Please log in to add items to cart.', 'warning')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    product = Product.query.get_or_404(product_id)
    
    # Check if item already in cart
    cart_item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
    
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(user_id=user_id, product_id=product_id, quantity=1)
        db.session.add(cart_item)
    
    db.session.commit()
    flash(f'{product.name} added to cart!', 'success')
    return redirect(request.referrer or url_for('products'))


@app.route('/cart')
def cart():
    """Shopping cart page"""
    if 'user_id' not in session:
        flash('Please log in to view your cart.', 'warning')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    return render_template('cart.html', cart_items=cart_items, total=total)


@app.route('/remove_from_cart/<int:cart_item_id>')
def remove_from_cart(cart_item_id):
    """Remove item from cart"""
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))
    
    cart_item = CartItem.query.get_or_404(cart_item_id)
    
    # Verify item belongs to current user
    if cart_item.user_id != session['user_id']:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('cart'))
    
    db.session.delete(cart_item)
    db.session.commit()
    flash('Item removed from cart.', 'info')
    return redirect(url_for('cart'))


@app.route('/update_cart/<int:cart_item_id>', methods=['POST'])
def update_cart(cart_item_id):
    """Update cart item quantity"""
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))
    
    cart_item = CartItem.query.get_or_404(cart_item_id)
    
    # Verify item belongs to current user
    if cart_item.user_id != session['user_id']:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('cart'))
    
    new_quantity = int(request.form['quantity'])
    if new_quantity > 0:
        cart_item.quantity = new_quantity
        db.session.commit()
        flash('Cart updated.', 'success')
    else:
        db.session.delete(cart_item)
        db.session.commit()
        flash('Item removed from cart.', 'info')
    
    return redirect(url_for('cart'))


@app.route('/payment', methods=['GET', 'POST'])
def payment():
    """Payment page"""
    if 'user_id' not in session or 'username' not in session:
        flash('Please log in to checkout.', 'warning')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    username = session['username'] 
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    
    if not cart_items:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('products'))
    
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    if request.method == 'POST':
        address = request.form['address']
        phone = request.form.get('phone')
        payment_method = request.form['payment_method']
        
        if not address:
            flash('Delivery address is required.', 'danger')
            return render_template('payment.html', cart_items=cart_items, total=total)
        
        # Process payment method
        if payment_method == "Online Payment":
            # Check if a specific payment app was selected
            payment_password = request.form.get('payment_password')
            if not payment_password:
                flash('Payment password is required for online payment.', 'danger')
                return render_template('payment.html', cart_items=cart_items, total=total)
            # In a real application, you would process the payment here
            payment_method = "Online Payment - UPI"
        
        # Create order
        order = Order(
            user_id=user_id,
            username=username,
            total_amount=total,
            payment_method=payment_method,
            delivery_address=address,
            order_status='Order Placed',
            created_at=datetime.now(pytz.timezone('Asia/Kolkata')),
        )
        db.session.add(order)
        db.session.flush()  # Get order ID
        
        # Create order items
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            db.session.add(order_item)
        
        # Clear cart
        CartItem.query.filter_by(user_id=user_id).delete()
        
        db.session.commit()

         # Send SMS confirmation to user
        user = User.query.get(user_id)
        if user and phone:  # ensure phone number is stored for user
            try:
                if payment_method == "Online Payment":
                    message = client.messages.create(
                    body=f"Hi Admin, {user.username}'s order has been placed successfully. Total: ₹{total} has been credited.",
                    from_=twilio_number,
                    to=os.getenv("ADMIN_PHONE_NUMBER")
                    )
                    logging.info(f"SMS sent: SID {message.sid}")
                else:
                    message = client.messages.create(
                    body=f"Hi Admin, {user.username}'s order has been placed successfully. Total: ₹{total}.",
                    from_=twilio_number,
                    to=os.getenv("ADMIN_PHONE_NUMBER")
                    )
                    logging.info(f"SMS sent: SID {message.sid}")
            except Exception as e:
                logging.error(f"SMS failed: {str(e)}")

        
        flash('Order placed successfully! Thank you for your purchase.', 'success')
        return redirect(url_for('order_history'))
    
    return render_template('payment.html', cart_items=cart_items, total=total)


@app.route('/order_history')
def order_history():
    """Order history page"""
    if 'user_id' not in session:
        flash('Please log in to view your orders.', 'warning')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    
    return render_template('order_history.html', orders=orders)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        username = session['username'] 
        user_phone = request.form.get('phone')
        user_message = request.form.get('message')

        try:
            # Send SMS to you (admin) from user contact form
            sms = client.messages.create(
                body=f"New Message from {username} ({user_phone}): {user_message}",
                from_=twilio_number,
                to=os.getenv("ADMIN_PHONE_NUMBER")  # your personal number (must be verified in Twilio)
            )
            flash('Thank you for contacting us. We’ll get back to you soon!', 'success')
            logging.info(f"Contact SMS sent: {sms.sid}")
        except Exception as e:
            flash('Failed to send message. Try again later.', 'danger')
            logging.error(f"Twilio Error: {str(e)}")

    return render_template('contact.html')



@app.route('/faq')
def faq():
    """FAQ page"""
    return render_template('faq.html')


@app.route('/terms')
def terms():
    """TERMS AND CONDITION"""
    last_updated = datetime.now().strftime("%B %d, %Y")  
    return render_template('terms.html', last_updated=last_updated)


@app.context_processor
def inject_user():
    """Make user info available in all templates"""
    return dict(
        current_user_id=session.get('user_id'),
        current_username=session.get('username')
    )

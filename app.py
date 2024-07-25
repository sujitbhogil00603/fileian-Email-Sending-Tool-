import logging
from flask import Flask, request, render_template, redirect, url_for, session
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'mail.adopt.email'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'support@adopt.email'
app.config['MAIL_PASSWORD'] = 'hDthqFv1'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('send_email'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    stored_password = users.get(email)
    if stored_password and check_password_hash(stored_password, password):
        session['user'] = email
        return redirect(url_for('send_email'))
    return 'Invalid credentials', 403

@app.route('/send-email', methods=['GET', 'POST'])
def send_email():
    if 'user' not in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        recipient_email = request.form['email']
        subject = 'Your Subject Here'
        context = {'image_url': 'http://example.com/image.jpg'}
        html_content = render_template('email_template.html', **context)

        msg = Message(subject,
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[recipient_email])
        msg.html = html_content
        
        try:
            mail.send(msg)
            return 'Email sent!'
        except Exception as e:
            logging.error(f'Error sending email: {e}')
            return 'Error sending email!', 500
    
    return render_template('email_form.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

from celery_worker import celery_app
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText
import smtplib 
from flask import render_template
from models import User, Booking, Trek 

SERVER_SMTP_HOST = 'localhost'
SERVER_SMTP_PORT = 1025 
SENDER_ADDRESS = 'admin@trektn.com'
SENDER_PASSWORD = ''

def send_email(to_address, subject, message, content="text", attachment=None):
    msg = MIMEMultipart()
    msg['To'] = to_address
    msg['From'] = SENDER_ADDRESS
    msg['Subject'] = subject
    
    if content == "html":
        msg.attach(MIMEText(message, 'html'))
    else:
        msg.attach(MIMEText(message, 'plain'))

    if attachment:
        with open(attachment, "rb") as a:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(a.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={attachment}")
        msg.attach(part)          

    s = smtplib.SMTP(host=SERVER_SMTP_HOST, port=SERVER_SMTP_PORT)
    
    
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    
    s.send_message(msg)
    s.quit()
    return True

@celery_app.task
def send_monthly_report():
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        return "No admin user found"
        
    bookings = Booking.query.all()
    booking_data = []
    
    for booking in bookings:
        user = User.query.get(booking.user_id)
        trek = Trek.query.get(booking.trek_id)
        
        if user and trek:
            booking_data.append({
                'username': user.username,
                'trek_name': trek.name,
                'location': trek.location,
                'status': booking.status,
                'booking_date': booking.booking_date,
                'price': trek.price
            })
            
    html = render_template('monthly_report.html', bookings=booking_data)
    send_email(admin.email, "Monthly Trek Bookings Report", html, content="html")
    
    return "Monthly report sent to admin."
    
@celery_app.task
def send_daily_reminder():  
    """Sends a reminder to users who have an active/confirmed booking."""
    active_bookings = Booking.query.filter_by(status='Confirmed').all() 
    
    for booking in active_bookings:
        user = User.query.get(booking.user_id)
        trek = Trek.query.get(booking.trek_id)
        
        if user and trek:
            email_body = (f"Dear {user.name},\n\n"
                          f"This is a reminder for your upcoming trek: {trek.name} in {trek.location}.\n"
                          f"Your booking status is currently {booking.status}. "
                          f"Please ensure you review the trek details and prepare accordingly!\n\n"
                          f"Happy Trekking!")
                          
            send_email(user.email, f"Daily Reminder: Upcoming Trek - {trek.name}", email_body) 
            
    return "Daily reminders sent to trekkers."
    
@celery_app.task
def export_bookings_report(user_id):
    user = User.query.get(user_id)
    if not user:
        return "User not found"
        
    bookings = Booking.query.filter_by(user_id=user_id).all()
    booking_data = []
    
    for booking in bookings:
        trek = Trek.query.get(booking.trek_id)
        if trek:
            booking_data.append({
                'trek_name': trek.name,
                'location': trek.location,
                'status': booking.status,
                'start_date': trek.start_date.strftime('%d-%m-%Y') if trek.start_date else 'N/A',
                'end_date': trek.end_date.strftime('%d-%m-%Y') if trek.end_date else 'N/A',
                'price': trek.price
            })
            
    total_cost = sum(item['price'] for item in booking_data)
    
    html = render_template(
        'export.html', 
        bookings=booking_data, 
        username=user.username, 
        total_bookings=len(booking_data), 
        total_cost=total_cost
    )    
    
    send_email(user.email, "Your Trek Bookings Export", html, content="html")
    return "Bookings report sent to user."
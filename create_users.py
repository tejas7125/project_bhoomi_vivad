from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    # पहले से मौजूद यूज़र्स हटाएँ
    db.session.query(User).delete()
    db.session.commit()

    # नए यूज़र जोड़ें
    admin = User(username="admin", password=generate_password_hash("admin123"), role="admin")
    thana_user = User(username="thana1", password=generate_password_hash("thana123"), role="thana")
    officer_user = User(username="officer1", password=generate_password_hash("officer123"), role="officer")

    db.session.add(admin)
    db.session.add(thana_user)
    db.session.add(officer_user)
    db.session.commit()

    print("✅ सभी यूज़र फिर से बनाए गए!")

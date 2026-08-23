from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("\n=======================================================")
    print(" Digital Citizen Service Portal - Server Starting ")
    print("=======================================================")
    print(" Local URL: http://127.0.0.1:5000")
    print(" Demo Admin: admin@gov.in | Admin@123")
    print(" Demo Citizen: citizen@gmail.com | Citizen@123")
    print("=======================================================\n")
    app.run(host='127.0.0.1', port=5000, debug=True)

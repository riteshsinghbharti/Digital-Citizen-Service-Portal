import os
import json
from datetime import datetime
from app import create_app, db
from app.models import User, Service, Application, Document, Grievance, Notification

app = create_app()

def seed_database():
    with app.app_context():
        # Create tables
        db.create_all()
        print("Database tables created successfully.")

        # Seed Admin User if not existing
        admin = User.query.filter_by(email='admin@gov.in').first()
        if not admin:
            admin = User(
                name='Nodal Administrative Officer',
                email='admin@gov.in',
                mobile='9876543210',
                role='admin',
                address='Government Secretariat Building',
                state='Maharashtra',
                district='Mumbai'
            )
            admin.set_password('Admin@123')
            db.session.add(admin)
            print("Admin user created: admin@gov.in / Admin@123")

        # Seed Sample Citizen User if not existing
        citizen = User.query.filter_by(email='citizen@gmail.com').first()
        if not citizen:
            citizen = User(
                name='Ramesh Kumar',
                email='citizen@gmail.com',
                mobile='9812345678',
                role='citizen',
                address='Flat 402, Sunshine Apartments, MG Road',
                state='Maharashtra',
                district='Pune'
            )
            citizen.set_password('Citizen@123')
            db.session.add(citizen)
            print("Citizen user created: citizen@gmail.com / Citizen@123")

        db.session.commit() # commit users to get IDs

        # Seed Services Catalog if empty
        if Service.query.count() == 0:
            services_data = [
                {
                    'name': 'Income Certificate',
                    'description': 'Official government revenue document certifying total annual family income from all sources.',
                    'required_documents': 'Aadhaar Card, Salary Slip / Form 16, Ration Card, Self-Declaration Affidavit',
                    'processing_time': '3 Working Days',
                    'category': 'Certificates',
                    'icon': 'fa-file-invoice-dollar'
                },
                {
                    'name': 'Domicile & Residence Certificate',
                    'description': 'Proof of continuous residence in the state for education, recruitment, and welfare benefits.',
                    'required_documents': 'Identity Proof, Electricity / Water Bill, School Leaving Certificate, Tax Receipt',
                    'processing_time': '5 Working Days',
                    'category': 'Certificates',
                    'icon': 'fa-house-chimney-user'
                },
                {
                    'name': 'Birth Certificate',
                    'description': 'Official vital registration record certifying person date and place of birth.',
                    'required_documents': 'Hospital Birth Slip, Parents Aadhaar Card, Marriage Certificate',
                    'processing_time': '7 Working Days',
                    'category': 'Certificates',
                    'icon': 'fa-baby'
                },
                {
                    'name': 'Caste & Category Certificate',
                    'description': 'Verification certificate for reserved category quotas, scholarships, and state schemes.',
                    'required_documents': 'School Register Extract, Blood Relative Caste Proof, Ancestral Residence Proof',
                    'processing_time': '10 Working Days',
                    'category': 'Certificates',
                    'icon': 'fa-id-card'
                },
                {
                    'name': 'Senior Citizen Pension Scheme',
                    'description': 'Monthly financial pension support for state citizens aged 60 years and above.',
                    'required_documents': 'Age Proof (Passport/Voter ID), Bank Passbook Details, Income Declaration',
                    'processing_time': '14 Working Days',
                    'category': 'Pensions',
                    'icon': 'fa-person-cane'
                },
                {
                    'name': 'Land Mutation & Title Extract',
                    'description': 'Revenue land record update and certified extract copy for property owners.',
                    'required_documents': 'Registered Sale Deed, Index-II Copy, Property Tax No-Dues Receipt',
                    'processing_time': '7 Working Days',
                    'category': 'Revenue',
                    'icon': 'fa-landmark'
                }
            ]

            for s_data in services_data:
                srv = Service(**s_data)
                db.session.add(srv)
            db.session.commit()
            print("Services catalog seeded.")

        # Seed Initial Applications if empty
        if Application.query.count() == 0:
            income_srv = Service.query.filter_by(name='Income Certificate').first()
            domicile_srv = Service.query.filter_by(name='Domicile & Residence Certificate').first()
            pension_srv = Service.query.filter_by(name='Senior Citizen Pension Scheme').first()

            p_info = {
                'full_name': 'Ramesh Kumar',
                'dob': '1990-05-15',
                'gender': 'Male',
                'mobile': '9812345678',
                'email': 'citizen@gmail.com'
            }
            a_info = {
                'street_address': 'Flat 402, Sunshine Apartments, MG Road',
                'city': 'Pune',
                'district': 'Pune',
                'state': 'Maharashtra',
                'pincode': '411001'
            }

            # 1. Approved Application
            app1 = Application(
                application_number='APP-2026-10001',
                user_id=citizen.id,
                service_id=income_srv.id,
                personal_info=json.dumps(p_info),
                address_info=json.dumps(a_info),
                purpose='College Fee Scholarship Application',
                additional_info='Annual family income under 2.5 Lakhs.',
                status='approved',
                current_remarks='All documents verified. Income Certificate issued successfully.'
            )

            # 2. Submitted Application
            app2 = Application(
                application_number='APP-2026-10002',
                user_id=citizen.id,
                service_id=domicile_srv.id,
                personal_info=json.dumps(p_info),
                address_info=json.dumps(a_info),
                purpose='State Public Service Commission Recruitment',
                additional_info='Resident since 2010.',
                status='submitted',
                current_remarks='Application dossier submitted online by applicant.'
            )

            # 3. Under Review Application
            app3 = Application(
                application_number='APP-2026-10003',
                user_id=citizen.id,
                service_id=pension_srv.id,
                personal_info=json.dumps(p_info),
                address_info=json.dumps(a_info),
                purpose='State Senior Pension Registration',
                additional_info='Applying on behalf of parent.',
                status='under_review',
                current_remarks='Dossier assigned to Field Verification Officer.'
            )

            db.session.add_all([app1, app2, app3])
            db.session.flush()

            # Seed Sample Document for App 1
            doc1 = Document(
                application_id=app1.id,
                document_type='Identity Proof',
                original_filename='aadhaar_card_scan.pdf',
                stored_filename='sample_aadhaar.pdf',
                file_path='uploads/documents/sample_aadhaar.pdf',
                file_type='pdf',
                file_size=245000
            )
            doc2 = Document(
                application_id=app1.id,
                document_type='Income Affidavit',
                original_filename='salary_declaration.pdf',
                stored_filename='sample_income.pdf',
                file_path='uploads/documents/sample_income.pdf',
                file_type='pdf',
                file_size=180000
            )
            db.session.add_all([doc1, doc2])

            # Seed Initial Notifications for Citizen
            n1 = Notification(
                user_id=citizen.id,
                title='Certificate Approved & Ready!',
                message='Your application APP-2026-10001 for Income Certificate has been approved! You can now download your digital certificate.',
                type='application',
                is_read=False
            )
            n2 = Notification(
                user_id=citizen.id,
                title='Application APP-2026-10002 Received',
                message='Your application for Domicile & Residence Certificate has been received by the department.',
                type='application',
                is_read=True
            )
            db.session.add_all([n1, n2])

            db.session.commit()
            print("Sample applications, documents, and notifications seeded.")

        # Seed Initial Grievance if empty
        if Grievance.query.count() == 0:
            grv = Grievance(
                grievance_number='GRV-2026-10001',
                user_id=citizen.id,
                citizen_name='Ramesh Kumar',
                citizen_email='citizen@gmail.com',
                citizen_mobile='9812345678',
                category='Delay in Service Delivery',
                subject='Delay in Domicile Verification for APP-2026-10002',
                description='I submitted my domicile certificate dossier last week. Kindly expedite the officer field verification stage.',
                status='in_progress',
                remarks='Assigned to Tehsildar office for immediate resolution.'
            )
            db.session.add(grv)
            db.session.commit()
            print("Sample grievance seeded.")

        print("\n--- DATABASE SEED COMPLETE ---")
        print("Admin Login:   admin@gov.in    | Password: Admin@123")
        print("Citizen Login: citizen@gmail.com | Password: Citizen@123")

if __name__ == '__main__':
    seed_database()

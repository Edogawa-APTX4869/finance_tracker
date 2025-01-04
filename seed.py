from django.contrib.auth.models import User
from expenses.models import Category
from incomes.models import Source

def seed_database():
    try:
        # Create Superuser if not exists
        username = "Admin"
        password = "Admin12345"
        email = "Admin@tracker.com"

        # Check if superuser exists, create if not
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            print(f"Superuser '{username}' created successfully.")
        else:
            print("Superuser already exists.")

        # Data for Categories
        category_data = [
            {"id": 1, "name": "Groceries", "description": ""},
            {"id": 2, "name": "Fuel/Petrol", "description": ""},
            {"id": 3, "name": "House rent", "description": ""},
            {"id": 4, "name": "Electricity bills", "description": ""},
            {"id": 5, "name": "Water bills", "description": ""},
            {"id": 6, "name": "Internet bills", "description": ""},
            {"id": 7, "name": "Mobile recharge/top-up", "description": ""},
            {"id": 8, "name": "Snacks", "description": ""},
            {"id": 9, "name": "Drinks (e.g., coffee, soda, etc.)", "description": ""},
            {"id": 10, "name": "Fast food", "description": ""},
            {"id": 11, "name": "Dining out", "description": ""},
            {"id": 12, "name": "Public transportation", "description": ""},
            {"id": 13, "name": "Ride-hailing services (e.g., Uber)", "description": ""},
            {"id": 14, "name": "Loan repayments", "description": ""},
            {"id": 15, "name": "Medicines", "description": ""},
            {"id": 16, "name": "Doctor visits", "description": ""},
            {"id": 17, "name": "Beauty products", "description": ""},
            {"id": 18, "name": "Haircuts", "description": ""},
            {"id": 19, "name": "Home cleaning supplies", "description": ""},
            {"id": 20, "name": "Vehicle maintenance", "description": ""},
            {"id": 21, "name": "Clothing", "description": ""},
            {"id": 22, "name": "Footwear", "description": ""},
            {"id": 23, "name": "Entertainment", "description": ""},
            {"id": 24, "name": "Subscriptions", "description": ""},
            {"id": 25, "name": "Gym membership", "description": ""},
            {"id": 26, "name": "Gifts", "description": ""},
            {"id": 27, "name": "Insurance premiums", "description": ""},
            {"id": 28, "name": "Education fees", "description": ""},
            {"id": 29, "name": "Sadaqah", "description": ""},
            {"id": 30, "name": "Zakat", "description": ""},
            {"id": 31, "name": "Charity", "description": ""},
            {"id": 32, "name": "Vapes", "description": ""},
            {"id": 33, "name": "E-cigarettes", "description": ""},
            {"id": 34, "name": "Personal grooming products", "description": ""},
            {"id": 35, "name": "Baby products", "description": ""},
            {"id": 36, "name": "School supplies", "description": ""},
            {"id": 37, "name": "Pet food and supplies", "description": ""},
            {"id": 38, "name": "Emergency funds", "description": ""},
            {"id": 39, "name": "Travel expenses", "description": ""},
            {"id": 40, "name": "Home repairs", "description": ""},
            {"id": 41, "name": "Furniture purchases", "description": ""},
            {"id": 42, "name": "Electronics and gadgets", "description": ""},
            {"id": 43, "name": "Fitness classes or equipment", "description": ""},
            {"id": 44, "name": "Hobby expenses (e.g., books, arts & crafts)", "description": ""},
            {"id": 45, "name": "Savings contributions", "description": ""},
            {"id": 46, "name": "Professional services", "description": ""},
            {"id": 47, "name": "Others", "description": ""}
        ]

        # Data for Sources (Income)
        income_data = [
            {"id": 1, "name": "Salary", "description": ""},
            {"id": 2, "name": "Business", "description": ""},
            {"id": 3, "name": "Investment", "description": ""},
            {"id": 4, "name": "Other", "description": ""}
        ]

        # Seed Categories
        for category in category_data:
            Category.objects.get_or_create(
                id=category['id'],
                defaults={
                    'name': category['name'],
                    'description': category['description']
                }
            )

        # Seed Sources (Income)
        for source in income_data:
            Source.objects.get_or_create(
                id=source['id'],
                defaults={
                    'name': source['name'],
                    'description': source['description']
                }
            )

        print("Database seeding completed successfully.")
    except Exception as e:
        print(f"An error occurred while seeding the database: {e}")

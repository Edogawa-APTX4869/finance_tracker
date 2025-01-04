# tracker/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from tracker.seed import seed_database

@receiver(post_migrate)
def seed_after_migration(sender, **kwargs):
    """
    This function will run after every migration.
    It will automatically call the seed_database function to populate the database.
    """
    print("Running database seeding after migration...")
    try:
        seed_database()  # Call the seed function
        print("Database seeded successfully.")
    except Exception as e:
        print(f"An error occurred while seeding the database: {e}")

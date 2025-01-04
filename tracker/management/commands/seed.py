# tracker/management/commands/seed.py
from django.core.management.base import BaseCommand
from tracker.seed import seed_database  # Adjust the import path to your seed function

class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding the database...")
        try:
            seed_database()  # This calls the function in your seed.py file
            self.stdout.write(self.style.SUCCESS('Database seeding completed successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))

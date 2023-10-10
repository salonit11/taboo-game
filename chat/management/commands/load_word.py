import csv

import pandas as pd
from django.core.management import BaseCommand

from ...models import Word


class Command(BaseCommand):
    help = "Load a word csv file into the database"

    def add_arguments(self, parser):
        parser.add_argument("--path", type=str)

    def handle(self, *args, **kwargs):
        # Remove any existing data
        print("Clean old product data")
        Word.objects.all().delete()
        path = kwargs["path"]
        # Read the product csv file as a dataframe
        product_df = pd.read_csv(path)
        # Iterate each row in the dataframe
        for index, row in product_df.iterrows():
            words = row["Words"]
            difficulty = row["Difficulty"]
            score = row["Score"]
            # Populate Product object for each row
            word = Word(
                words=words,
                difficulty=difficulty,
                score=score,
            )
            # Save product object
            word.save()
            print(f"Words: {words}, {score} saved...")


# python manage.py load_word --path csv file name

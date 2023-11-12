from django.core.management.base import BaseCommand, CommandError
import json
import os
from collection.models import Artist, Style, Period, Genre, Artwork
from django.db import IntegrityError
from decouple import config
from django.conf import settings
import csv



class Command(BaseCommand):
    help = "Load all Artists, Styles, Periods, Genres and Artworks from CSV files"
    

    def handle(self, *args, **options):
        BASE_DIR = settings.BASE_DIR
        WIKIART_DIR = os.path.join(BASE_DIR, 'wikiart_data/data')
        csv_files= os.listdir(WIKIART_DIR)


        try:
            artists = [f for f in csv_files if '-art.csv' not in f]
            for artist in artists:
                with open(os.path.join(WIKIART_DIR, artist), newline='') as f:
                    reader = csv.reader(f) 
                    for row in reader:
                        slug = row[0]
                        name = row[1]
                        born_date = row[2]
                        
                        artist_obj = Artist.objects.create(
                            slug=slug,
                            name=name,
                            born_date=born_date,
                        )
                artist_art = artist.replace('.csv', '-art.csv')

                print(f"Created artist: {name}")

                with open(os.path.join(WIKIART_DIR, artist_art), newline='') as f:
                    reader = csv.reader(f) 
                    for row in reader:
                        if row[4] != "":
                            style_obj, _ = Style.objects.get_or_create(name=row[4])
                        if row[5] != "":
                            period_obj, _ = Period.objects.get_or_create(name=row[5])
                        if row[6] != "":
                            genre_obj, _ = Genre.objects.get_or_create(name=row[6])

                        path=row[1]
                        title=row[2]
                        date=row[3]
                        image_url = row[7]

                        artwork_obj = Artwork.objects.create(
                            author=artist_obj,
                            path=path,
                            title=title,
                            date=date,
                            style=style_obj if row[4] != "" else None,
                            period=period_obj if row[5] != "" else None,
                            genre=genre_obj if row[6] != "" else None,
                            image_url=image_url,
                        )

                        print(f"Created artwork: {title}")

        except Exception as e:
            raise CommandError("Error: " + str(e))
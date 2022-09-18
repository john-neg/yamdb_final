from csv import DictReader

from django.core.management import BaseCommand

from api_yamdb.reviews.models import (Category, Comment, Genre, Review, Title,
                                      TitleGenre)
from api_yamdb.users.models import User


class Command(BaseCommand):
    help = "Загружает данные из папки static/data в базу данных"

    def handle(self, *args, **options):
        databases = {
            User: {
                "filename": "static/data/users.csv",
                "fields": {
                    "id": "id",
                    "username": "username",
                    "email": "email",
                    "role": "role",
                    "bio": "bio",
                    "first_name": "first_name",
                    "last_name": "last_name",
                },
            },
            Category: {
                "filename": "static/data/category.csv",
                "fields": {
                    "id": "id",
                    "name": "name",
                    "slug": "slug",
                },
            },
            Genre: {
                "filename": "static/data/genre.csv",
                "fields": {
                    "id": "id",
                    "name": "name",
                    "slug": "slug",
                },
            },
            Title: {
                "filename": "static/data/titles.csv",
                "fields": {
                    "id": "id",
                    "name": "name",
                    "year": "year",
                    "category_id": "category",
                },
            },
            TitleGenre: {
                "filename": "static/data/genre_title.csv",
                "fields": {
                    "id": "id",
                    "title_id": "title_id",
                    "genre_id": "genre_id",
                },
            },
            Review: {
                "filename": "static/data/review.csv",
                "fields": {
                    "id": "id",
                    "title_id": "title_id",
                    "text": "text",
                    "author_id": "author",
                    "score": "score",
                    "pub_date": "pub_date",
                },
            },
            Comment: {
                "filename": "static/data/comments.csv",
                "fields": {
                    "id": "id",
                    "review_id": "review_id",
                    "text": "text",
                    "author_id": "author",
                    "pub_date": "pub_date",
                },
            },
        }
        for obj in databases:
            if obj.objects.exists():
                print(
                    f"В таблице {obj.__name__} уже имеются данные.\n"
                    f"Для загрузки необходимо очистить таблицу"
                )
                continue
            print(f"Загружаю данные в {obj.__name__}")

            for row in DictReader(
                open(databases[obj].get("filename"), encoding="UTF-8")
            ):
                kwargs = {
                    key: row[val] for key, val in databases[obj][
                        "fields"
                    ].items()
                }
                record = obj(**kwargs)
                record.save()
        print("Данные успешно загружены")

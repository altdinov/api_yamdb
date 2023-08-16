import csv

from django.core.management.base import BaseCommand
from django.db import transaction

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("csv_file", nargs="+", type=str)

    @transaction.atomic
    def handle(self, *args, **options):
        for csv_file_name in options["csv_file"]:
            reader = csv.DictReader(
                open(csv_file_name, encoding="utf-8"),
                delimiter=",",
                quotechar='"'
            )

            for row in reader:
                if "category.csv" in csv_file_name:
                    Category.objects.create(
                        id=row["id"], name=row["name"], slug=row["slug"]
                    )
                if "genre.csv" in csv_file_name:
                    Genre.objects.create(
                        id=row["id"], name=row["name"], slug=row["slug"]
                    )
                if "titles.csv" in csv_file_name:
                    Title.objects.create(
                        id=row["id"],
                        name=row["name"],
                        year=row["year"],
                        category_id=row["category"],
                    )
                if "genre_title.csv" in csv_file_name:
                    GenreTitle.objects.create(
                        id=row["id"],
                        title_id=row["title_id"],
                        genre_id=row["genre_id"]
                    )
                if "users.csv" in csv_file_name:
                    User.objects.create(
                        id=row["id"],
                        username=row["username"],
                        email=row["email"],
                        role=row["role"],
                        bio=row["bio"],
                        first_name=row["first_name"],
                        last_name=row["last_name"],
                    )
                if "review.csv" in csv_file_name:
                    Review.objects.create(
                        id=row["id"],
                        title_id=row["title_id"],
                        text=row["text"],
                        author_id=row["author"],
                        score=row["score"],
                        pub_date=row["pub_date"]
                    )
                if "comments.csv" in csv_file_name:
                    Comment.objects.create(
                        id=row["id"],
                        review_id=row["review_id"],
                        text=row["text"],
                        author_id=row["author"],
                        pub_date=row["pub_date"],
                    )

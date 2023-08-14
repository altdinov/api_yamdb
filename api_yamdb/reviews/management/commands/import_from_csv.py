import csv

from django.core.management.base import BaseCommand

from reviews.models import Category, Genre, GenreTitle, Title, Review, Comment
from users.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("csv_file", nargs="+", type=str)

    def handle(self, *args, **options):
        for csv_file_name in options["csv_file"]:
            reader = csv.DictReader(
                open(csv_file_name), delimiter=",", quotechar='"'
            )

            if (
                "category.csv" in csv_file_name
                and Category.objects.all().first() is not None
            ):
                return "Objects Category already exist in DB. Import aborted"
            if (
                "genre.csv" in csv_file_name
                and Genre.objects.all().first() is not None
            ):
                return "Objects Genre already exist in DB. Import aborted"
            if (
                "titles.csv" in csv_file_name
                and Title.objects.all().first() is not None
            ):
                return "Objects Title already exist in DB. Import aborted"
            if (
                "genre_title.csv" in csv_file_name
                and GenreTitle.objects.all().first() is not None
            ):
                return "Objects GenreTitle already exist in DB. Import aborted"
            if (
                "users.csv" in csv_file_name
                and User.objects.all().first() is not None
            ):
                return "Objects Users already exist in DB. Import aborted"
            if (
                "review.csv" in csv_file_name
                and Review.objects.all().first() is not None
            ):
                return "Objects Reviews already exist in DB. Import aborted"
            if (
                "comments.csv" in csv_file_name
                and Comment.objects.all().first() is not None
            ):
                return "Objects Comments already exist in DB. Import aborted"

            print(csv_file_name)
            for row in reader:
                if "category.csv" in csv_file_name:
                    Category.objects.create(name=row["name"], slug=row["slug"])
                if "genre.csv" in csv_file_name:
                    Genre.objects.create(name=row["name"], slug=row["slug"])
                if "titles.csv" in csv_file_name:
                    Title.objects.create(
                        name=row["name"],
                        year=row["year"],
                        category_id=row["category"],
                    )
                if "genre_title.csv" in csv_file_name:
                    GenreTitle.objects.create(
                        title_id=row["title_id"], genre_id=row["genre_id"]
                    )
                if "users.csv" in csv_file_name:
                    User.objects.create(
                        username=row["username"],
                        email=row["email"],
                        role=row["role"],
                        bio=row["bio"],
                        first_name=row["first_name"],
                        last_name=row["last_name"],
                    )
                if "review.csv" in csv_file_name:
                    Review.objects.create(
                        title_id=row["title_id"],
                        text=row["text"],
                        author_id=row["author"],
                        score=row["score"],
                        pub_date=row["pub_date"]
                    )
                if "comments.csv" in csv_file_name:
                    Comment.objects.create(
                        review_id=row["review_id"],
                        text=row["text"],
                        author_id=row["author"],
                        pub_date=row["pub_date"],
                    )

            if "category.csv" in csv_file_name:
                self.stdout.write("Import category.csv complited")
            if "genre.csv" in csv_file_name:
                self.stdout.write("Import genry.csv complited")
            if "titles.csv" in csv_file_name and row.get("name"):
                self.stdout.write("Import title.csv complited")
            if "genre_title.csv" in csv_file_name:
                self.stdout.write("Import genre_title.csv complited")
            if "users.csv" in csv_file_name:
                self.stdout.write("Import users.csv complited")
            if "review.csv" in csv_file_name:
                self.stdout.write("Import review.csv complited")
            if "comments.csv" in csv_file_name:
                self.stdout.write("Import comments.csv complited")

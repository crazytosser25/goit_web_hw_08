import os
import json
from mongoengine import connect, Document
from mongoengine.fields import ReferenceField, ListField, StringField
from dotenv import load_dotenv
# pylint: disable=no-member

load_dotenv()
mongo_user = os.getenv('user')
mongodb_pass = os.getenv('pass')
db_name = os.getenv('db_name')
domain = os.getenv('domain')

connect(
    host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}"""
)

class Authors(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

class Quotes(Document):
    tags = ListField(StringField())
    author = ReferenceField(Authors, required=True)
    quote = StringField(required=True)

def load_authors():
    with open('authors.json', 'r', encoding='utf-8') as file:
        authors_data = json.load(file)
        for author_data in authors_data:
            author = Authors.objects(fullname=author_data['fullname']).first()
            if not author:
                author = Authors(
                    fullname=author_data['fullname'],
                    born_date=author_data.get('born_date'),
                    born_location=author_data.get('born_location'),
                    description=author_data.get('description')
                )
                author.save()
                print(f'Author {author.fullname} created.')
            else:
                print(f'Author {author.fullname} already exists.')

def load_quotes():
    with open('quotes.json', 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)
        for quote_data in quotes_data:
            author_name = quote_data['author']
            author = Authors.objects(fullname=author_name).first()
            if author:
                quote = Quotes(
                    quote=quote_data['quote'],
                    author=author,
                    tags=quote_data.get('tags', [])
                )
                quote.save()
                print(
                    f'Quote "{quote.quote}" by {quote.author.fullname} saved.'
                )
            else:
                print(
                    f'No author {author_name} for quote: {quote_data["quote"]}.'
                )

if __name__ == '__main__':
    load_authors()
    load_quotes()

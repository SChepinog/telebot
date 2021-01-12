from datetime import date

from base import Session, engine, Base
from pojos import Movie

Base.metadata.create_all(engine)

session = Session()


def create_movies():
    bourne_identity = Movie("The Bourne Identity", date(2002, 10, 11))
    furious_7 = Movie("Furious 7", date(2015, 4, 2))
    pain_and_gain = Movie("Pain & Gain", date(2013, 8, 23))

    session.add(bourne_identity)
    session.add(furious_7)
    session.add(pain_and_gain)

    session.commit()
    session.close()


# create_movies()

movies = session.query(Movie).all()

print('\n### All movies:')
for movie in movies:
    print(f'{movie.title} was released on {movie.release_date}')
print('')

movies = session.query(Movie) \
    .filter(Movie.release_date > date(2015, 1, 1)) \
    .all()

print('### Recent movies:')
for movie in movies:
    print(f'{movie.title} was released after 2015')
print('')

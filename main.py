# Name: Manav Gupta
# NetID: mgupta31 | UIN: 657115759
# School: University of Illinois at Chicago
# Project: CS 341 - Project 2
# Date: Spring 2023, 2nd February
#
# Program to analyze data from a MovieLens database

import sqlite3
import objecttier

#
# Command 1
#
# retrieves the movie id, title, and release year based on the name/wildcards _ and % inputted
# if no movie is found, return with 0 movies found, and if too many movies found, returns a message saying so.
def retrieve_movies(dbConn):
  print()
  name = input("Enter movie name (wildcards _ and % supported): ")

  movies = objecttier.get_movies(dbConn, name)
  print()

  if movies is None:
    print("# of movies found: 0")
    return

  print("# of movies found:", '{:}'.format(len(movies)))

  print()
  if len(movies) > 100: # too many movies
    print('There are too many movies to display, please narrow your search and try again...')
    return
  elif len(movies) > 0:
    for m in movies:
      print(m.Movie_ID, ":", m.Title, '({})'.format(m.Release_Year))

#
# Command 2
#
# retrieves all the details about a movie based on the inputted movie ID
# if an error is encountered/no movie with the given ID, then an error message is given and function returns
def retrieve_movie_details(dbConn):
  print()
  name = input("Enter movie id: ")

  movieDetails = objecttier.get_movie_details(dbConn, name)
  
  print()
  if movieDetails is None: # error
    print('No such movie...')
    return

  print(movieDetails.Movie_ID, ':', movieDetails.Title)
  print('  Release date:', movieDetails.Release_Date)
  print('  Runtime:', movieDetails.Runtime, '(mins)')
  print('  Orig language:', movieDetails.Original_Language)
  print('  Budget: ${:,}'.format(movieDetails.Budget), '(USD)')
  print('  Revenue: ${:,}'.format(movieDetails.Revenue), '(USD)')
  print('  Num reviews:', movieDetails.Num_Reviews)
  print('  Avg rating:', '{:0.2f}'.format(movieDetails.Avg_Rating), '(0..10)')
  print('  Genres:', end=" ")
  for g in movieDetails.Genres:
    print(g, end=", ")
  print()
  print('  Production companies:', end=" ")
  for pc in movieDetails.Production_Companies:
    print(pc, end=", ")
  print()
  print('  Tagline:', movieDetails.Tagline)
  
#
# Command 3
#
# retrieves the top N amount of movies with at least a minimum number of reviews. Gets N and min number of reviews as input. If either number is a negative, an error message is given and function returns.
def retrieve_top_N_movies(dbConn):
  print()
  N = int(input("N? "))
  if N < 1: # error
    print('Please enter a positive value for N...')
    return
  
  minReviews = int(input("min number of reviews? "))
  if minReviews < 1: # error
    print('Please enter a positive value for min number of reviews...')
    return

  topNMovies = objecttier.get_top_N_movies(dbConn, N, minReviews)

  if len(topNMovies) > 0:
    print()
    for t in topNMovies:
      print(t.Movie_ID, ':', t.Title, '({}),'.format(t.Release_Year), 'avg rating =', '{:0.2f}'.format(t.Avg_Rating), '({} reviews)'.format(t.Num_Reviews))
  

#
# Command 4
#
# adds a rating/review for a movie to the database. The rating and movie ID are input. If the rating is a negative number or above 10, an error message is given and the function returns. If movie id doesn't exist, error message and functino returns
def adding_review(dbConn):
  print()
  rating = int(input('Enter rating (0..10): '))
  if rating < 0 or rating > 10: # error
    print('Invalid rating...')
    return

  id = input('Enter movie id: ')

  reviewAdded = objecttier.add_review(dbConn, id, rating)

  print()
  if reviewAdded == 0: # error
    print('No such movie...')
    return
  
  print('Review successfully inserted')

#
# Command 5
#
# Sets a tagline for a movie. The tagline and movie ID are input. If the movie ID doesn't exist, an error message is given and function returns.
def setting_tagline(dbConn):
  print()
  tagline = input('tagline? ')

  id = input('movie id? ')

  taglineSet = objecttier.set_tagline(dbConn, id, tagline)

  print()
  if taglineSet == 0: # error
    print('No such movie...')
    return
  
  print('Tagline successfully set')
  dbConn.commit()

##################################################################  
#
# main
#
print('** Welcome to the MovieLens app **')

dbConn = sqlite3.connect('MovieLens.db')

print()

numMovies = objecttier.num_movies(dbConn)
numReviews = objecttier.num_reviews(dbConn)
if numMovies != -1 and numReviews != -1:
  print('General stats:')
  print("  # of movies:", '{:,}'.format(numMovies))
  print("  # of reviews:", '{:,}'.format(numReviews))
print()

cmd = input("Please enter a command (1-5, x to exit): ")

while cmd != "x":
  if cmd == "1":
    retrieve_movies(dbConn)
  elif cmd == "2":
    retrieve_movie_details(dbConn)
  elif cmd == "3":
    retrieve_top_N_movies(dbConn)
  elif cmd == "4":
    adding_review(dbConn)
  elif cmd == "5":
    setting_tagline(dbConn)
  else:
    print("**Error, unknown command, try again...")
  print()
  cmd = input("Please enter a command (1-5, x to exit): ")

dbConn.close()
#
# done
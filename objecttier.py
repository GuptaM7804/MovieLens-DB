# File: objecttier.py
#
# objecttier
#
# Builds Movie-related objects from data retrieved through 
# the data tier.
#
# Original author:
#   Prof. Joe Hummel
#   U. of Illinois, Chicago
#   CS 341, Spring 2022
#   Project #02
#
import datatier


##################################################################
#
# Movie:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#
class Movie:
  def __init__(self, ID, Title, Year):
    self._Movie_ID = ID
    self._Title = Title
    self._Release_Year = Year

  @property
  def Movie_ID(self):
    return self._Movie_ID
  @property
  def Title(self):
    return self._Title
  @property
  def Release_Year(self):
    return self._Release_Year


##################################################################
#
# MovieRating:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#   Num_Reviews: int
#   Avg_Rating: float
#
class MovieRating:
  def __init__(self, ID, Title, Year, num_reviews, avg_rating):
    self._Movie_ID = ID
    self._Title = Title
    self._Release_Year = Year
    self._Num_Reviews = num_reviews
    self._Avg_Rating = avg_rating

  @property
  def Movie_ID(self):
    return self._Movie_ID
  @property
  def Title(self):
    return self._Title
  @property
  def Release_Year(self):
    return self._Release_Year
  @property
  def Num_Reviews(self):
    return self._Num_Reviews
  @property
  def Avg_Rating(self):
    return self._Avg_Rating


##################################################################
#
# MovieDetails:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Date: string, date only (no time)
#   Runtime: int (minutes)
#   Original_Language: string
#   Budget: int (USD)
#   Revenue: int (USD)
#   Num_Reviews: int
#   Avg_Rating: float
#   Tagline: string
#   Genres: list of string
#   Production_Companies: list of string
#
class MovieDetails:
  def __init__(self, ID, Title, date, runtime, language, budget, revenue, num_reviews, avg_rating, tagline, genres, companies):
    self._Movie_ID = ID
    self._Title = Title
    self._Release_Date = date
    self._Runtime = runtime
    self._Original_Language = language
    self._Budget = budget
    self._Revenue = revenue
    self._Num_Reviews = num_reviews
    self._Avg_Rating = avg_rating
    self._Tagline = tagline
    self._Genres = genres
    self._Production_Companies = companies

  @property
  def Movie_ID(self):
    return self._Movie_ID
  @property
  def Title(self):
    return self._Title
  @property
  def Release_Date(self):
    return self._Release_Date
  @property
  def Runtime(self):
    return self._Runtime
  @property
  def Original_Language(self):
    return self._Original_Language
  @property
  def Budget(self):
    return self._Budget
  @property
  def Revenue(self):
    return self._Revenue
  @property
  def Num_Reviews(self):
    return self._Num_Reviews
  @property
  def Avg_Rating(self):
    return self._Avg_Rating
  @property
  def Tagline(self):
    return self._Tagline
  @property
  def Genres(self):
    return self._Genres
  @property
  def Production_Companies(self):
    return self._Production_Companies


##################################################################
# 
# num_movies:
#
# Returns: # of movies in the database; if an error returns -1
#
def num_movies(dbConn):
  sql = "Select count(*) from Movies"
  try:
    res = datatier.select_one_row(dbConn, sql, None)
    return res[0]
  except Exception:
    return -1
  


##################################################################
# 
# num_reviews:
#
# Returns: # of reviews in the database; if an error returns -1
#
def num_reviews(dbConn):
  sql = "Select count(*) from Ratings"
  try:
    res = datatier.select_one_row(dbConn, sql, None)
    return res[0]
  except Exception:
    return -1


##################################################################
#
# get_movies:
#
# gets and returns all movies whose name are "like"
# the pattern. Patterns are based on SQL, which allow
# the _ and % wildcards. Pass "%" to get all stations.
#
# Returns: list of movies in ascending order by name; 
#          an empty list means the query did not retrieve
#          any data (or an internal error occurred, in
#          which case an error msg is already output).
#
def get_movies(dbConn, pattern):
  sql = "Select Movies.Movie_ID, Title, strftime('%Y', Release_Date) from Movies where Title like ? Order by Movie_ID"
  res = datatier.select_n_rows(dbConn, sql, [pattern])
  if res is None:
    return None
  movies = []
  for r in res:
    temp = Movie(r[0], r[1], r[2])
    movies.append(temp)
  return movies


##################################################################
#
# get_movie_details:
#
# gets and returns details about the given movie; you pass
# the movie id, function returns a MovieDetails object. Returns
# None if no movie was found with this id.
#
# Returns: if the search was successful, a MovieDetails obj
#          is returned. If the search did not find a matching
#          movie, None is returned; note that None is also 
#          returned if an internal error occurred (in which
#          case an error msg is already output).
#
def get_movie_details(dbConn, movie_id):
  sql = "Select Movies.Movie_ID, Title, strftime('%Y-%m-%d', Release_Date), Runtime, Original_Language, Budget, Revenue, count(Rating), avg(Rating), Tagline from Movies left join Movie_Taglines on Movies.Movie_ID=Movie_Taglines.Movie_ID left join Ratings on Movies.Movie_ID=Ratings.Movie_ID where Movies.Movie_ID = ? group by Movies.Movie_ID"
  row = datatier.select_one_row(dbConn, sql, [movie_id])

  if len(row) == 0:
    return None

  sql2 = "Select Company_Name from Companies join Movie_Production_Companies on Companies.Company_ID=Movie_Production_Companies.Company_ID where Movie_Production_Companies.Movie_ID = ? order by Company_Name"
  companies = datatier.select_n_rows(dbConn, sql2, [movie_id])
  comp = []
  if companies is None:
    pass
  else:
    for c in companies:
      comp.append(c[0])
  
  
  sql3 = "Select Genre_Name from Genres join Movie_Genres on Genres.Genre_ID=Movie_Genres.Genre_ID where Movie_Genres.Movie_ID = ? order by Genre_Name"
  genres = datatier.select_n_rows(dbConn, sql3, [movie_id])
  genre = []
  if genres is None:
    pass
  else:
    for g in genres:
      genre.append(g[0])
  if row[7] == 0:
    avg = 0.00
  else:
    avg = row[8]
  if row[9] is None:
    tag = ""
  else:
    tag = row[9]
  movie_details = MovieDetails(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], avg, tag, genre, comp)
  return movie_details

##################################################################
#
# get_top_N_movies:
#
# gets and returns the top N movies based on their average 
# rating, where each movie has at least the specified # of
# reviews. Example: pass (10, 100) to get the top 10 movies
# with at least 100 reviews.
#
# Returns: returns a list of 0 or more MovieRating objects;
#          the list could be empty if the min # of reviews
#          is too high. An empty list is also returned if
#          an internal error occurs (in which case an error 
#          msg is already output).
#
def get_top_N_movies(dbConn, N, min_num_reviews):
  sql = "Select Movies.Movie_ID, Title, strftime('%Y', Release_Date), count(Rating), avg(Rating) from Movies join Ratings on Movies.Movie_ID=Ratings.Movie_ID group by Movies.Movie_ID having count(Rating) >= ? order by avg(Rating) desc limit ?"
  rows = datatier.select_n_rows(dbConn, sql, [min_num_reviews, N])
  if rows is None:
    return None
  ans = []
  for r in rows:
    movie_rating = MovieRating(r[0], r[1], r[2], r[3], r[4])
    ans.append(movie_rating)
  return ans


##################################################################
#
# add_review:
#
# Inserts the given review --- a rating value 0..10 --- into
# the database for the given movie. It is considered an error
# if the movie does not exist (see below), and the review is
# not inserted.
#
# Returns: 1 if the review was successfully added, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def add_review(dbConn, movie_id, rating):
  sql = "Select count(*) from Movies where Movie_ID = ?"
  check = datatier.select_one_row(dbConn, sql, [movie_id])
  if check[0] == 0:
    return 0
  sql = "INSERT INTO Ratings (Movie_ID, Rating) VALUES (?, ?)"
  cnt = datatier.perform_action(dbConn, sql, [movie_id, rating])
  if cnt == -1:
    return 0
  return cnt


##################################################################
#
# set_tagline:
#
# Sets the tagline --- summary --- for the given movie. If
# the movie already has a tagline, it will be replaced by
# this new value. Passing a tagline of "" effectively 
# deletes the existing tagline. It is considered an error
# if the movie does not exist (see below), and the tagline
# is not set.
#
# Returns: 1 if the tagline was successfully set, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def set_tagline(dbConn, movie_id, tagline):
  sql = "Select count(Movies.Movie_ID), count(Tagline) from Movies left join Movie_Taglines on Movies.Movie_ID=Movie_Taglines.Movie_ID where Movies.Movie_ID = ?"
  check = datatier.select_one_row(dbConn, sql, [movie_id])
  if check[0] == 0:
    return 0
  if check[1] == 0:
      sql = "INSERT INTO Movie_Taglines (Movie_ID, Tagline) VALUES (?, ?)"
      cnt = datatier.perform_action(dbConn, sql, [movie_id, tagline])
  else:
    sql = "UPDATE Movie_Taglines set Tagline = ? where Movie_ID = ?"
    cnt = datatier.perform_action(dbConn, sql, [tagline, movie_id])

  if cnt == -1:
    return 0
  return cnt
  

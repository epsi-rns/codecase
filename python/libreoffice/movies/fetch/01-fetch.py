import tomli, requests, csv, time
from typing import List, Dict, Any

class FetchOMDB:
  def __init__(self) -> None:
    # config, all parameter arguments from tomli
    self.set_config()

    # Example: Fetch movies for the 1980s
    self.output_folder = 'by-year'
    self.start_year = 1980
    self.end_year   = 2019

  def set_config(self) -> None:
    # read toml configuration
    config_path: str = 'secret.toml'
    file_obj: TextIO = open(config_path, 'rb')
    config_root = tomli.load(file_obj)
    file_obj.close()

    # Get my secret OMdb API KEY
    self.API_KEY = config_root.get('API_KEY', '')

  # Function to fetch movies by year
  def fetch_movies_by_year(
        self, year: int, search_term: str = "movie"
      ) -> List[Dict[str, Any]]:

    url = f"http://www.omdbapi.com/" + \
          f"?apikey={self.API_KEY}&s={search_term}" + \
          f"&y={year}&type=movie"
    response = requests.get(url)

    if response.status_code == 200:
      data = response.json()

      if data.get("Response") == "True":
        # Return a list of movies
        return data.get("Search", [])

    return []

  # Function to fetch detailed movie data
  def fetch_movie_details(
        self, imdb_id: str) -> Dict[str, Any]:

    url = f"http://www.omdbapi.com/" + \
          f"?apikey={self.API_KEY}&i={imdb_id}"
    response = requests.get(url)

    if response.status_code == 200:
      data = response.json()
      if data.get("Response") == "True":
        return {
          "Year"     : data.get("Year",     "N/A"),
          "Title"    : data.get("Title",    "N/A"),
          "Genre"    : data.get("Genre",    "N/A"),
          "Plot"     : data.get("Plot",     "N/A"),
          "Actors"   : data.get("Actors",   "N/A"),
          "Director" : data.get("Director", "N/A"),
          "Rated"    : data.get("Rated",    "N/A"),
          "Runtime"  : data.get("Runtime",  "N/A"),
          "Metascore": data.get("Metascore","N/A"),
        }
    return None

  # Save movies from a year into a CSV file
  def save_movies_by_year_to_csv(
        self, year: int, output_file: str, 
        search_term: str = "movie") -> None:

    fieldnames = [
      "Year", "Title", "Genre",
      "Plot", "Director", "Actors",
      "Rated", "Runtime", "Metascore"
    ]

    with open(output_file, \
           mode="w", newline="", encoding="utf-8"
         ) as csv_file:

      writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
      writer.writeheader()

      # Fetch a list of movies from the given year
      movies = self.fetch_movies_by_year(year, search_term)
      if not movies:
        print(f"No movies found for {year}")
        return

      for movie in movies:
        imdb_id = movie.get("imdbID")
        if imdb_id:
          details = self.fetch_movie_details(imdb_id)
          if details:
            writer.writerow(details)
            print(f"Added: {details['Title']} ({details['Year']})")
          else:
            print(f"Details not found for IMDb ID: {imdb_id}")
        
        # Avoid rate-limiting
        time.sleep(1)

  # Generate multiple sheets for decades
  def run(self) -> None:
    for year in range(self.start_year, self.end_year + 1):
      output_file = f"{self.output_folder}/movies_{year}.csv"
      print(f"Fetching movies for {year}...")
      self.save_movies_by_year_to_csv(year, output_file)

    print("Movies fetched and saved.")

# Run the script
def main() -> None:
  fetch_omdb = FetchOMDB()
  fetch_omdb.run()

# Program entry point
if __name__ == "__main__":
  main()

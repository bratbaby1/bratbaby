import hashlib
from os import listdir
import os
from os.path import join, isfile
import json
import uuid
from flask import current_app
from model.artist_model import ArtistModel
from model.movie_model import MovieModel

__author__ = 'Ashkan'

artist_dict = {}
film_dict = {}


FILMS_FOLDER_PATH = os.path.join(os.path.dirname(__file__), '../films/')


class ArtistData(object):
    """
    This class handles data layer methods for accessing artist and films
    it also does initializes the data by reading the json files and creates needed artist and film dictionaries
    """

    def init_data(self):
        """
        This method iterates through list of json files in films folder and reads each of them
        to populate artist and film dictionaries
        """
        for f in listdir(FILMS_FOLDER_PATH):
            file_full_path = join(FILMS_FOLDER_PATH, f)
            if isfile(file_full_path):
                self.__read_file(file_full_path)

    def __read_file(self, json_file):
        """
        Given a json file this method reads the json file and populates the artist and film dictionaries
        artist dict has artist name as the key and it's value is artist model containing artist info and their films
        films dict has unique id generated by me as key and value is film model containing the info of the film and
        it's casts
        @param json_file: content of the json file containing film info
        """
        with open(json_file) as json_file:
            json_data = json.load(json_file)
            if 'film' in json_data:
                # generate a guid since we can't use names,
                # names cause issues when we have same name few times
                # ex. Last Holiday we have it two times and we can't use them as key
                film_uuid = uuid.uuid1()

                # create new movie model by json data
                movie_model = MovieModel(film_uuid, json_data)
                film_dict[film_uuid] = movie_model

                # now parse the cast data of the film to generate artist dict
                if 'cast' in json_data and len(json_data['cast']) > 0:
                    for cast in json_data['cast']:
                        # create a new artist model from the cast info
                        # we assign a new id for this artist to avoid issues with getting artist by name
                        cast_name = cast['name']
                        cast_uuid = self.get_cast_id_for_name(cast_name)
                        artist_model = ArtistModel(cast_uuid, cast)

                        if artist_model.id not in artist_dict:
                            # first time seeing this artist,
                            # we haven't had this artist in the dict yet
                            # add them to the dict
                            artist_model.films.append(film_uuid)
                            artist_dict[artist_model.id] = artist_model
                        else:
                            # we already had this artist before
                            # no need to update the info, just add the film
                            artist_dict[artist_model.id].films.append(film_uuid)
                else:
                    current_app.logger.info(u"Movie {0} had no cast".format(movie_model.info['name']))
            else:
                current_app.logger.info(u"Missing film in json: {0}".format(json_data))

    def artist_exist(self, artist_id):
        """
        This method given an artist name makes sure artist exist in our artist dict or not
        @param artist_id: unique id of the artist we are looking for
        @return: boolean showing if artist exist in our system or not
        """
        return artist_id in artist_dict

    def get_all_films_for_artist(self, artist_id):
        """
        This python generator reads list of films of an artist
        @param artist_id: id of the artist we are looking for their films
        @return: next film model
        """
        for film in artist_dict[artist_id].films:
            yield film

    def get_movie_by_id(self, movie_id):
        """
        This method returns a movie model by getting it from film dict
        if we don't know this id it will return None
        @param movie_id: unique id of the film we are looking for
        @return: MovieModel of the film and None if we don't find the film
        """
        if movie_id in film_dict:
            return film_dict[movie_id]
        else:
            return None

    def get_artist_by_name(self, artist_name):
        """
        Passed an artist name this method returns the artist model
        @param artist_name: string name of the artist we are looking for
        @return: ArtistModel if exist and None if we don't have this artist
        """
        artist_id = self.get_cast_id_for_name(artist_name)
        return self.get_artist_by_id(artist_id)

    def get_artist_by_id(self, artist_id):
        """
        Passed an artist name this method returns the artist model
        @param artist_name: string name of the artist we are looking for
        @return: ArtistModel if exist and None if we don't have this artist
        """
        if artist_id in artist_dict:
            return artist_dict[artist_id]
        else:
            return None

    def search_artists_by_name(self, search_query):
        """
        This method searches for artists with search query in their name and returns the list
        @param search_query: string of the search we want to make
        @return: list of ArtistModels matching this search
        """
        return list(artist_model for artist_name, artist_model in artist_dict.iteritems()
                    if search_query.lower() in artist_model.info['name'].lower())

    def get_cast_id_for_name(self, cast_name):
        return hashlib.sha1(cast_name.lower().encode('utf-8')).hexdigest()


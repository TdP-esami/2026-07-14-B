from database.DB_connect import DBConnect
from model.movie import Movie


class DAO:
    @staticmethod
    def getAllGenres():
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct g.genre
                from genre g
                where g.genre is not null
                order by g.genre
                """
        cursor.execute(query)

        for row in cursor:
            results.append(row["genre"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getMoviesByGenre(genre):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT DISTINCT m.id, m.title, m.year, r.avg_rating
                FROM movie m
                JOIN genre g ON m.id = g.movie_id
                JOIN role_mapping rm ON rm.movie_id = m.id 
                AND (rm.category = "actor" or rm.category = "actress")
                LEFT JOIN ratings r ON r.movie_id = m.id
                WHERE g.genre = %s
                ORDER BY m.title
                """
        cursor.execute(query, (genre,))

        for row in cursor:
            avg_rating = row["avg_rating"] if row["avg_rating"] is not None else 0.0
            results.append(Movie(row["id"], row["title"], row["year"], avg_rating))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getActorsForMovie(movie):
        """Popola movie.Actors con l'insieme degli id degli attori del film. Non mi serviranno i dettagli degli attori,
        solo quanti sono, per cui non leggo anche da names."""
        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)
        query = """
                select rm.name_id
                from role_mapping rm
                where rm.movie_id = %s
                and (rm.category = "actor" or rm.category = "actress")
                """
        cursor.execute(query, (movie.MovieId,))

        movie.Actors = set(row["name_id"] for row in cursor)

        cursor.close()
        conn.close()

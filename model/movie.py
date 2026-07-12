from dataclasses import dataclass, field


@dataclass
class Movie:
    MovieId: int
    Title: str
    Year: int
    AvgRating: float = 0.0
    Actors: set = field(default_factory=set)

    def __hash__(self):
        return hash(self.MovieId)

    def __eq__(self, other):
        if not isinstance(other, Movie):
            return False
        return self.MovieId == other.MovieId

    def __str__(self):
        return f"{self.Title} ({self.Year})"

    def get_num_actors(self):
        return len(self.Actors)

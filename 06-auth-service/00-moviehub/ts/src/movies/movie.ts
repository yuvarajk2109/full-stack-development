interface Movie {
    id: number;
    title: string;
    genre: string;
    rating: number;
    description?: string;
}

function getMovieTitle(movie: Movie): string {
    return movie.title;
}

const movie: Movie = {
    id: 1,
    title: "Interstellar",
    genre: "Sci-Fi",
    rating: 9
};

console.log("Movie Title: " + getMovieTitle(movie));


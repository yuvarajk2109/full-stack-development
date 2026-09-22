const movies = [
    {
        id: 1,
        title: "Interstellar",
        genre: "Sci-Fi",
        rating: 9
    },
    {
        id: 2,
        title: "Inception",
        genre: "Sci-Fi",
        rating: 8.8
    },
    {
        id: 3,
        title: "Titanic",
        genre: "Romance",
        rating: 8
    }
];

console.log("All Movies");
console.log(movies);

const popularMovies = movies.filter(
    movie => movie.rating >= 8.5
);
console.log ("\nPopular Movies");
console.log(popularMovies);
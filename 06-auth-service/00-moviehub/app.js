import { movies } from "./movie-data.js";
const popularMovies = movies.filter(
    movie => movie.rating >= 8.5
);

console.log(popularMovies);
import { getMovies, getPopularMovies } from "./movie-service.js";
const movies = await getMovies();
console.log(movies);
import { movies } from "./movie-data.js";

export function getMovies() {
    return new Promise(resolve => {
        setTimeout(() => {
            resolve(movies);
        }, 1000);
    });
}

export function getPopularMovies() {
    return new Promise(resolve => {
        setTimeout(() => {
            resolve(movies.filter(
                movie => movie.rating >= 8.5
            ));
        }, 1000);
    });
}
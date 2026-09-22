import { Injectable } from "@nestjs/common";

@Injectable()
export class MoviesService {
    getMovies() {
         return [
            {
                id: 1,
                title: "Interstellar"
            }
        ];
    }
}
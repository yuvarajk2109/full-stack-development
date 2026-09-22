import {
    IsNotEmpty,
    IsNumber,
    Min,
    Max
} from "class-validator";

export class CreateMovieDto {
    @IsNotEmpty()
    title!: string;

    @IsNotEmpty()
    genre!: string;
    
    @IsNumber()
    @Min(0)
    @Max(10)
    rating!: number;
}
// TODO 1: import the decorators you need from class-validator, then add
// them so this DTO enforces:
//   - username: a string, not empty, at least 3 characters
//   - password: a string, at least 8 characters
//   - email: a string, and a VALID EMAIL ADDRESS (there's a decorator for
//     this specifically - check class-validator's exports)

import { IsEmail, IsNotEmpty, IsString, Min, MinLength } from "class-validator";

export class RegisterDto {
  @IsString()
  @IsNotEmpty()
  @MinLength(3)
  username!: string;

  @IsString()
  @MinLength(8)
  password!: string;

  @IsEmail()
  email!: string;
}

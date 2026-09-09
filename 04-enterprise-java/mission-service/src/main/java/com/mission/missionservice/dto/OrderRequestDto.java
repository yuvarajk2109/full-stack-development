package com.mission.missionservice.dto;

import com.mission.missionservice.enums.InstrumentType;
import com.mission.missionservice.enums.Side;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;

// Kata A: add Bean Validation annotations to every field, matching
// Module 5's OpenAPI OrderRequest schema:
//   - ticker: required, non-blank
//   - instrumentType: required
//   - quantity: required, must be positive
//   - price: required, must be positive
//   - side: required
// See OrderRequestDtoTest.java for the exact behaviour expected - it uses
// jakarta.validation directly, no Spring context needed.
public record OrderRequestDto(
        @NotBlank(message = "ticker must be present and non-blank") String ticker,
        @NotNull(message = "instrumentType is required") InstrumentType instrumentType,
        @Positive(message = "quantity must be greater than zero") double quantity,
        @Positive(message = "price must be greater than zero") double price,
        @NotNull(message = "side is required") Side side
) {
}

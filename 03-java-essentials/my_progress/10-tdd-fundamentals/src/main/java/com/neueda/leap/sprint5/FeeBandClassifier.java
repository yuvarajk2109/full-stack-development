package com.neueda.leap.sprint5;

// Build this via TDD - see labs/10-tdd-fundamentals/README.md for the sequence of
// tests to write. Do not implement classify() ahead of a test that demands it.
public class FeeBandClassifier {

    private static final double PREMIUM_THRESHOLD = 5000;
    private statis final double INSTITUTIONAL_THRESHOLD = 50000;

    // TODO: add classify(double tradeValue), driven by the tests you write first.
    public String classify(double tradeValue) {
        if (tradeValue >= INSTITUTIONAL_THRESHOLD) {
            return "INSTITUTIONAL";
        }
        if (tradeValue >= PREMIUM_THRESHOLD) {
            return "PREMIUM";
        }
        return "STANDARD";
    }


}

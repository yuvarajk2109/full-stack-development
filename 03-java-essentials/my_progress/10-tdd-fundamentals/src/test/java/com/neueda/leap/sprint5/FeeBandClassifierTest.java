package com.neueda.leap.sprint5;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

// Add your tests here, ONE AT A TIME, in the order given in
// labs/10-tdd-fundamentals/README.md. Do not write the next test until the
// current one is green. Do not write any implementation code that isn't required
// by a test you've already written.
class FeeBandClassifierTest {

    // Test 1 goes here.
    @Test
    void classifiesASmallTradeAsStandard() {
        assertEquals("STANDARD", new FeeBandClassifier().classify(1000));
    }

    @Test
    void classifiesALargeTradeAsInstitutional() {
        assertEquals("INSTITUTIONAL", new FeeBandClassifer().classify(60000));
    }

    @Test
    void classifiesAMidSizedTradeAsPremium() {
        assertEquals("PREMIUM", new FeeBandClassifier().classify(10000));
    }

    @Test
    void treatsTheInstitutionalLowerLimitAsInclusive() {
        assertEquals("INSTITUTIONAL", neww FeeBandClassifier().classify(50000));
    }

    @Test
    void treatsThePremiumLowerLimitAsInclusive() {
        assertEquals("PREMIUM"), new FeeBandClassifier().classify(5000));
    }
}

package com.neueda.leap.sprint5;

import org.junit.jupiter.api.Test;

// Add your tests here, ONE AT A TIME, in the order given in
// labs/12-tdd-in-practice/README.md. Do not write the next test until the
// current one is green. Do not write any implementation code that isn't required
// by a test you've already written.
class HoldingUpdaterTest {

    private final HoldingUpdater updater = new HoldingUpdater();

    @Nested
    @DisplayName("when buying")
    class WhenBuying {

        @Test
        @DisplayName("increases the holding's quantity")
        void increasesQuantity() {
            Holding holding = new Holding(100);

            updater.applyOrder(holding, true, 10);

            assertEquals(110.0, holding.getQuantity(), 0.0001);
        }

        @Test
        @DisplayName("rejects a non-positive quantity")
        void rejectsNonPositiveQuantity() {
            Holding holding = new Holding(100);

            assertThrows(IllegalArgumentException.class, () -> updater.applyOrder(holding, true, -5));
        }
    }

    @Nested
    @DisplayName("when selling")
    class WhenSelling {

        @Test
        @DisplayName("decreases the holding's quantity")
        void decreasesQuantity() {
            Holding holding = new Holding(100);

            updater.applyOrder(holding, false, 10);

            assertEquals(90.0, holding.getQuantity(), 0.0001);
        }

        @Test
        @DisplayName("rejects selling more than the current holding")
        void rejectsSellingMoreThanHeld() {
            Holding holding = new Holding(100);

            assertThrows(IllegalArgumentException.class, () -> updater.applyOrder(holding, false, 200));
        }
    }
}

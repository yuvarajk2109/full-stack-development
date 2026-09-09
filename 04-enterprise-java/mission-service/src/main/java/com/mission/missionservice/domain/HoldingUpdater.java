package com.mission.missionservice.domain;

public class HoldingUpdater {

    public void applyOrder(Holding holding, boolean isBuy, double quantity) {
        if (quantity <= 0) {
            throw new IllegalArgumentException("quantity must be positive");
        }
        if (isBuy) {
            holding.adjust(quantity);
        } else {
            holding.adjust(-quantity);
        }
    }
}

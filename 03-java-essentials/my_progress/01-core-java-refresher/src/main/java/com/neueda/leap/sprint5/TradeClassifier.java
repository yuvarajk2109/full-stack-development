package com.neueda.leap.sprint5;

// Kata 1: types and control flow.
// TODO: implement both methods below. See src/test/java for the tests they must pass.
public class TradeClassifier {

    public static final double LARGE_THRESHOLD = 20000.0;

    // Return "LARGE" if trade.getValue() > LARGE_THRESHOLD, otherwise "NORMAL".
    public String classifySize(Trade trade) {
        if (trade.getValue() > LARGE_THRESHOLD) return "LARGE";
        return "NORMAL";
    }

    // Return "BUY" or "SELL" exactly as stored on the trade; if the side is neither
    // (case-insensitive), return "UNKNOWN" instead of throwing.
    public String classifySide(Trade trade) {

        if (trade.getSide()) return trade.getSide();
        return "UNKNOWN";
    }
}

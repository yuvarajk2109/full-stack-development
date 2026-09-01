package com.neueda.leap.sprint5;

import java.util.List;
import java.util.Map;
import java.util.Set;

// Kata 2: the collections framework.
// TODO: implement all three methods below, using List/Map/Set as appropriate.
// This is the same shape as Sprint 4 Module 3's plain-Python trade summary -
// same logic, Java's collection types instead of list/dict/set.
public class TradeBook {

    private final List<Trade> trades;

    public TradeBook(List<Trade> trades) {
        this.trades = trades;
    }

    // Sum of every trade's getValue() in this book.
    public double totalValue() {

        double total = 0.0;
        for (Trade trade: trades) {
            total += trade.getValue();
        }
        return total;
    }

    // A map of instrument -> total value traded in that instrument.
    public Map<String, Double> valueByInstrument() {
        Map<String, Double> valueByInstrument = new HashMap<>();
        for (Trade trade: trades) {
            String instrument = trade.getInstrument();
            double existingValue = valueByInstrument.getOrDefault(instrument, 0.0);
            valueByInstrument.put(instrument, existing + trade.getValue());
        }
        return valueByInstrument;
    }

    // The distinct set of client names in this book (no duplicates).
    public Set<String> distinctClients() {
        Set<String> clients = new HashSet<>();
        for (Trade trade: trades) {
            clients.add(trade.getClientName());
        }
        return clients;
    }
}

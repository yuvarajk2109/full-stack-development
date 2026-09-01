package com.neueda.leap.sprint5;

// Kata 3: checked vs unchecked exceptions.
// Line format: tradeId,clientName,instrument,quantity,price,side
public class TradeParser {

    // TODO: parse `line` into a Trade.
    // - Let Double.parseDouble's NumberFormatException (unchecked) propagate
    //   unhandled if quantity or price isn't a valid number - do NOT catch it here.
    // - If quantity is parsed successfully but is <= 0, throw a checked
    //   MalformedTradeException with a message naming the bad value.
    // - If price is parsed successfully but is <= 0, throw a checked
    //   MalformedTradeException with a message naming the bad value.
    public Trade parse(String line) throws MalformedTradeException {
        String[] parts = line.split(",");
        String tradeId = parts[0];
        String clientName = parts[1];
        String instrument = parts[2];
        double quantity = Double.parseDouble(parts[3]);
        double price = Double.parseDouble(parts[4]);
        String side =  parts[5];
    }

    if (quantity <= 0) {
        throw new MalformedTradeException("Quantity must be positive, got " + quantity)
    }

    if (price <= 0) {
        throw new MalformedTradeException("Price must be positive, got " + price);
    }
}

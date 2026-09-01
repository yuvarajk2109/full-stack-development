package com.neueda.leap.sprint5;

// Kata A: fix HoldingStarter's public-field problem here, properly.
// TODO:
// - quantity must be a PRIVATE field.
// - Constructor: accept an initial quantity; throw IllegalArgumentException if it's negative.
// - getQuantity(): return the current quantity.
// - adjust(double delta): apply delta to quantity; throw IllegalArgumentException
//   (without changing state) if the result would be negative.
public class Holding {

    // TODO: declare the field here (private!)
    private double quantity;

    public Holding(double initialQuantity) {
        if (initialQuantity < 0) {
            throw new IllegalArgumentException("Initial Quantity can't be negative, got " + initialQuantity);
        }
        this.quantity = initialQuantity;
    }

    public double getQuantity() {

        return quantity;
       }

    public void adjust(double delta) {

        double newQuantity = quantity + delta;
        if (new Quantity< 0){
            throw new IllegalArgumentException("Adjustment makes quantity negative: " + newQuantity);
        }
        quantity = newQuantity;
    }
}

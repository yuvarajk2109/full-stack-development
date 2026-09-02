public class Order {

    private String customer;
    private String pizza;
    private int price;
    private int quantity;
    private String status;

    public Order(String customer, String pizza, int price, int quantity, String status) {
        this.customer = customer;
        this.pizza = pizza;
        this.price = price;
        this.quantity = quantity;
        this.status = status;
    }

    public String getCustomer() {
        return customer;
    }

    public String getPizza() {
        return pizza;
    }

    public int getPrice() {
        return price;
    }

    public int getQuantity() {
        return quantity;
    }

    public String getStatus() {
        return status;
    }

    @Override
    public String toString() {
        return customer + " - " + pizza +
                " - ₹" + price +
                " - Quantity: " + quantity +
                " - " + status;
    }
}
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class PizzaAnalyser {

    public static void main(String[] args) {

        List<Order> orders = List.of(
            new Order("Arun", "Margherita", 250, 2, "Delivered"),
            new Order("Priya", "Farmhouse", 450, 1, "Delivered"),
            new Order("Rahul", "Burger", 200, 3, "Cancelled"),
            new Order("Sneha", "Paneer", 400, 2, "Delivered"),
            new Order("Vijay", "Margherita", 250, 1, "Pending"),
            new Order("Anu", "Farmhouse", 450, 3, "Delivered"),
            new Order("Kiran", "Cheese", 350, 2, "Cancelled"),
            new Order("Ravi", "Paneer", 400, 1, "Delivered"),
            new Order("Meena", "Cheese", 350, 4, "Delivered"),
            new Order("Ajay", "Margherita", 250, 2, "Pending")
        );

        System.out.println("\nMISSION 1 ");
        System.out.println("Display all delivered orders:");
        orders.stream()
                .filter(order -> order.getStatus().equals("Delivered"))
                .forEach(System.out::println);

        System.out.println("\nMISSION 2 ");
        System.out.println("Total money earned from delivered orders:");
        int totalMoney = orders.stream()
                .filter(order -> order.getStatus().equals("Delivered"))
                .mapToInt(order -> order.getPrice() * order.getQuantity())
                .sum();
        System.out.println("Total Money Earned: ₹" + totalMoney);

        System.out.println("\nMISSION 3 ");
        System.out.println("Find the most expensive order:");
        Order expensiveOrder = orders.stream()
                .max(Comparator.comparingInt(Order::getPrice))
                .orElseThrow();
        System.out.println(expensiveOrder);

        System.out.println("\nMISSION 4 ");
        System.out.println("Customers whose order quantity is 3 or more:");
        orders.stream()
                .filter(order -> order.getQuantity() >= 3)
                .map(Order::getCustomer)
                .forEach(System.out::println);

        System.out.println("\nMISSION 5 ");
        System.out.println("Different pizza names without duplicates:");
        orders.stream()
                .map(Order::getPizza)
                .distinct()
                .forEach(System.out::println);

        System.out.println("\nMISSION 6 ");
        System.out.println("Orders sorted from cheapest to most expensive:");
        orders.stream()
                .sorted(Comparator.comparingInt(Order::getPrice))
                .forEach(System.out::println);

        System.out.println("\nMISSION 7 ");
        System.out.println("Count of orders by status:");
        long delivered = orders.stream()
                .filter(order -> order.getStatus().equals("Delivered"))
                .count();
        long pending = orders.stream()
                .filter(order -> order.getStatus().equals("Pending"))
                .count();
        long cancelled = orders.stream()
                .filter(order -> order.getStatus().equals("Cancelled"))
                .count();
        System.out.println("Delivered: " + delivered);
        System.out.println("Pending: " + pending);
        System.out.println("Cancelled: " + cancelled);

        System.out.println("\nMISSION 8 ");
        System.out.println("Customer who spent the most money on a single order:");
        Order vipOrder = orders.stream()
                .max(Comparator.comparingInt(
                        order -> order.getPrice() * order.getQuantity()
                ))
                .orElseThrow();
        System.out.println("Customer: " + vipOrder.getCustomer());
        System.out.println("Pizza: " + vipOrder.getPizza());
        System.out.println("Amount Spent: ₹"
                + (vipOrder.getPrice() * vipOrder.getQuantity()));

        System.out.println("\nFINAL CHALLENGE ");
        System.out.println("Best Customer - Customer who spent the most money overall:");
        Map<String, Integer> customerSpending = orders.stream()
                .collect(Collectors.groupingBy(
                        Order::getCustomer,
                        Collectors.summingInt(
                                order -> order.getPrice() * order.getQuantity()
                        )
                ));
        Map.Entry<String, Integer> bestCustomer =
                customerSpending.entrySet()
                        .stream()
                        .max(Map.Entry.comparingByValue())
                        .orElseThrow();

        System.out.println("Free pizza goes to " + bestCustomer.getKey());
        System.out.println(("Total money spent by " + bestCustomer.getKey() + " = " + bestCustomer.getValue()));


    }
}
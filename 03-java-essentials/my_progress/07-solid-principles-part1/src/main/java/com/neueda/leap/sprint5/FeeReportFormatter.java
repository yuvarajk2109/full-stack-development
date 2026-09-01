package com.neueda.leap.sprint5;

import java.util.List;

// Kata A.2 (SRP): one job only - turn orders plus a pre-calculated total into a
// report string. Format exactly:
//   Settlement Report
//   <clientId>: $<fee>
//   ... one line per order ...
//   Total fees: $<total>
// (no trailing newline after the total line)
public class FeeReportFormatter {

    public String format(List<Order> orders, double total) {
        StringBuilder report = new StringBuilder("Settlement Report\n");
        for (Order order : orders) {
            report.append(order.getClientId())
                    .append(": $")
                    .append(order.calculateFee())
                    .append("\n");
        }
        report.append("Total fees: $").append(total);
        return report.toString();
    }
}

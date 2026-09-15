| #  | Scenario                                                                           | Category |
|----|------------------------------------------------------------------------------------|----------|
| 1  | A customer clicks "Transfer Money" and asks the banking system to transfer ₹5,000. | **R**    |
| 2  | The banking system publishes "MoneyTransferred" after the transfer succeeds.       | **E**    |
| 3  | A customer asks the system to show their account balance.                          | **R**    |
| 4  | The system publishes "PaymentCompleted" after a payment is successfully processed. | **E**    |
| 5  | An application sends a request to create a new customer account.                   | **R**    |
| 6  | A "CustomerCreated" message is published after the account is created.             | **E**    |
| 7  | A user clicks "Cancel Order."                                                      | **R**    |
| 8  | The system publishes "OrderCancelled" after the cancellation is completed.         | **E**    |
| 9  | A customer asks for a refund for an order.                                         | **R**    |
| 10 | The payment system publishes "RefundProcessed."                                    | **E**    |
| 11 | A user asks a hotel system to book a room.                                         | **R**    |
| 12 | The hotel system publishes "RoomBooked" after the booking succeeds.                | **E**    |
| 13 | A service sends a message saying "OrderPlaced."                                    | **E**    |
| 14 | A customer sends a request to place an order for a laptop.                         | **R**    |
| 31 | "Please create a new loan application for this customer."                          | **R**    |
| 32 | "A new loan application has been created for customer 4582."                       | **E**    |
| 33 | "Please check whether this payment can be authorised."                             | **R**    |
| 34 | "Payment 7821 has been authorised."                                                | **E**    |
| 35 | "Send the customer's latest transactions."                                         | **R**    |
| 36 | "Customer 4582's transaction history was updated."                                 | **E**    |
| 37 | "Please reserve 2 seats on Flight 302."                                            | **R**    |
| 38 | "Two seats have been reserved on Flight 302."                                      | **E**    |
| 39 | "Tell me whether the order exists."                                                | **R**    |
| 40 | "Order 7821 was delivered."                                                        | **E**    |
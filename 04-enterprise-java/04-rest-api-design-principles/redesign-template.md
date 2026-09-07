# API Critique & Redesign — Order Management Service

## Part 1: What's Wrong (Critique)

For each issue you find in `bad-api-spec.md`, name the specific endpoint(s), the specific
problem, and which REST principle it violates. Aim for at least 6 distinct issues — there are
more than 6 in the spec.

| Endpoint(s)                                   | Problem                                                                                              | Principle violated                             |
|-----------------------------------------------|------------------------------------------------------------------------------------------------------|------------------------------------------------|
| GET /getAllOrders                             | The method is already GET, so getAllOrders is redundant                                              | Resource, NOT Action                           |
| GET /getOrder?id=123                          | Could have been combined with getAllOrders, but is separate with a different, extra name to remember | Resource, NOT Action                           |
| POST /createOrder                             | Again, we have a verb.                                                                               | Resource, NOT Action                           |
| DELETE /deleteOrder/123                       | Verb bruv.                                                                                           | Resource, NOT Action                           |
| GET /updateOrderStatus?id=123&status=REJECTED | Method should be PUT, and we again have a verb in the endpoint.                                      | Incorrect request method; Resource, NOT Action |
| POST /order                                   | Developer knows this is an older endpoint, but another developer or maybe a tester doesn't           | Versioning                                     |
| GET /orders/123/getFee                        | Again, verb usage is there                                                                           | Resource, NOT Action                           |

## Part 2: The Redesign

Rewrite the API properly. One row per operation.

| Method | URL                 | Status codes it can return | Idempotent? |
|--------|---------------------|----------------------------|-------------|
| GET    | /v1/orders          | 200, 403                   | NO          |
| GET    | /v1/orders/{id}     | 200, 403, 404              | NO          |
| POST   | /v2/orders          | 201, 403, 404              | YES         |
| DELETE | /v1/orders/{id}     | 204, 404                   | NO          |
| PUT    | /v1/orders/{id}     | 204, 404                   | NO          |
| POST   | /v1/orders          | 200, 403, 404              | YES         |
| GET    | /v1/orders/{id}/fee | 200, 403, 404              | NO          |

## Part 3: Versioning

Given the spec's claim that "there has never been a breaking change, so versioning has never
come up" — do you agree that's a good reason to have no versioning strategy at all? What would
you recommend, and why?

`No, that isn't a good enough reason. In fact, this spec actually requires versioning as there are two endpoints, both of which create an order, one of which is an older endpoint kept for backward compatibility - this is exactly what versioning is all about!` 

`Now that we have redesigned the endpoints with proper 'Resource, NOT Action' principle in mind, we add versions as well - the latest API has a higher version, and the older API with the lower version is still available to rollback to if needed.`

## Part 4: The Hardest Call

Which single issue in the original spec do you think would cause the most real damage in
production if left unfixed? Justify your answer in 2-3 sentences.

### Versioning

`Even the poorly named endpoints can be fine - errors related to them, like calling the wrong endpoint, can be easily tracked and fixed.`

`However, consider the two different order endpoints for order creation. Some developers may utilise the new endpoint and some may utilise the old endpoint, simply because it is not probably versioned and properly documented which one is the latest one.`

`And this could lead to a lot of serious issues. What if the old endpoint didn't have proper idempotency handling for orders while the new one did? This completely breaks the system when the old is used instead of the new one.`

### Status Codes

`Another notable thing is, in the original spec, there are no proper status codes that are returned. Every endpoint variation gets a 200, with the actual body of the returned message showing whether something is wrong or right`

`This can lead to testers not being able to track errors properly. This can lead to developers blindly believing their endpoint works even when it doesn't, and this further affects the corresponding frontend wherein it has to handle errors not based on status code but based on the body of the response, which is completely undesirable.`


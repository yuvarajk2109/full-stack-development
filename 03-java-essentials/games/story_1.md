# Library

## Part 1: Follow the Story

### 1. Who should initiate the borrowing process?

The client/library member is the trigger, but it is the librarian who actually initiates the process. 

For example, the librarian can reject a particular member from actually initiating a borrow, maybe because they have outstanding dues/they have exceeded the borrow limit.

### 2. What should happen immediately after the member requests to borrow a book?

The librarian checks for the availability of the book and validates the member.

### 3. Does the order of messages in the diagram make sense?

No, it doesn't make sense.

### 4. Is there any action happening too early?

The member validation isn't taking place - this means basically anyone can just come in and borrow and loan a book. The lack of initial validation creates a cascading effect that puts the entire system into chaos.

### 5. What information does the library need before creating a loan?

- Does the member have outstanding dues?
- Has the member crossed the loan limit?
- Does the member even exist?
- Does the book exist?
- Is the required quantity of the book available?

## Part 2: Who is Responsible?

Look carefully at who is communicating with whom.

### 1. Should the member communicate directly with the book?

The member should be validated initially with the library, only after that can they communicatr with the book.

### 2. Who should be responsible for checking whether a book is available?

The library

### 3. Should the book be asking the library to check it availability?

No

### 4. 

## Part 3: Follow the Information

### 1. When the library checks availability, where does the availability information come from?

### 2. What should the 

### 3. Does the current diagram show the result being returned?

## Part 4: Investigate the ALT

### 1.

No, it should come after check availability.

### 2.

It is created in the diagram, which is incorrect.

### 3.

## Part 5:

### 1.

Nothing happens, we need to introduce a validity check.

### 2. 

The loan is still created, which is incorrect. If the book doesn't exist - this check has to be made first.

### 3. 

The validation has to be performed even before the member initiates a borrow - so the borrow gets rejected in the first place before even going through to a loan.

### 4. What happens if a book is already borrowed?

Before proper book and customer validation, if the book is borrowed, it creates a huge inconsistency.

### 5. 

Pretty much everyone.

## Part 6: The Big Question

### 

Order of Messages changed!
Who communicates with whom accordingly modified.
Participant add/remove - NO.



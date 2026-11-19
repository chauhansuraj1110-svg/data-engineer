# 🏋️ Phase 2 Exercises

Test your SQL skills with these challenges.

---

## Exercise 1: Database Design
Design and create tables for a **Library System** with:
- `books` (book_id, title, author, genre, published_year, isbn)
- `members` (member_id, name, email, membership_date)
- `loans` (loan_id, book_id, member_id, loan_date, return_date, status)

Add appropriate constraints (NOT NULL, UNIQUE, FOREIGN KEY, CHECK).

---

## Exercise 2: Query Challenge
Using the e-commerce tables from the lessons, write queries to answer:

1. Which product has never been ordered?
2. What is the average time between a customer's first and second order?
3. Which city generates the most revenue per customer?
4. List products that contribute more than 25% of their category's revenue.
5. Find the top 3 customers by order frequency (not by total spend).

---

## Exercise 3: Window Function Practice
Write queries using window functions to:

1. For each order, show what percentage it is of that customer's total spending
2. Rank customers by their most recent order date (who ordered most recently?)
3. Calculate a 3-order moving average of order amounts
4. Find the time gap (in days) between consecutive orders for each customer

---

## ✅ Self-Check
Before moving to Phase 3, make sure you can:
- [ ] Create tables with proper data types and constraints
- [ ] Write SELECT queries with WHERE, ORDER BY, LIMIT
- [ ] Use INNER JOIN and LEFT JOIN confidently
- [ ] Write GROUP BY queries with HAVING
- [ ] Use at least 3 window functions (ROW_NUMBER, RANK, SUM OVER, LAG)

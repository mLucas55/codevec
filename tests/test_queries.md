# Test Queries for Semantic Search System

## Query Performance Test Cases

### Authentication & Security

1. **Query:** "check if password is strong enough"
   - **Expected:** `validate_password_strength` in utils/validation.py
   - **Tests:** Password validation, security requirements

2. **Query:** "generate JWT token for user"
   - **Expected:** `create_jwt_token` in auth/user_auth.py
   - **Tests:** Token generation, authentication

3. **Query:** "verify user login credentials"
   - **Expected:** `verify_password` in auth/user_auth.py
   - **Tests:** Synonym matching (verify/check)

4. **Query:** "prevent brute force login attacks"
   - **Expected:** `check_login_attempts` in auth/user_auth.py
   - **Tests:** Understanding intent, security concepts

### Validation & Data Quality

5. **Query:** "validate email address format"
   - **Expected:** `validate_email` in utils/validation.py
   - **Tests:** Direct matching, common task

6. **Query:** "check credit card number is valid"
   - **Expected:** `validate_credit_card` in utils/validation.py
   - **Tests:** Domain knowledge (Luhn algorithm)

7. **Query:** "sanitize user input to prevent SQL injection"
   - **Expected:** `sanitize_input` in utils/validation.py
   - **Tests:** Security understanding

8. **Query:** "verify phone number format"
   - **Expected:** `validate_phone_number` in utils/validation.py
   - **Tests:** Synonym (verify/validate)

### String Manipulation

9. **Query:** "convert text to URL friendly format"
   - **Expected:** `slugify` in utils/string_helpers.py
   - **Tests:** Understanding task description vs function name

10. **Query:** "hide credit card numbers"
    - **Expected:** `mask_sensitive_data` in utils/string_helpers.py
    - **Tests:** Synonym (hide/mask), security context

11. **Query:** "format money with dollar sign"
    - **Expected:** `format_currency` in utils/string_helpers.py
    - **Tests:** Common terminology (money/currency)

12. **Query:** "convert camelCase to snake_case"
    - **Expected:** `convert_to_snake_case` in utils/string_helpers.py
    - **Tests:** Technical terminology

### Database Operations

13. **Query:** "insert new record into database table"
    - **Expected:** `insert_record` in data/database.py
    - **Tests:** CRUD operation understanding

14. **Query:** "find record by ID"
    - **Expected:** `find_by_id` in data/database.py
    - **Tests:** Basic search operation

15. **Query:** "update existing database record"
    - **Expected:** `update_record` in data/database.py
    - **Tests:** CRUD operations

16. **Query:** "bulk insert multiple rows"
    - **Expected:** `batch_insert` in data/database.py
    - **Tests:** Synonym (bulk/batch)

### API & HTTP

17. **Query:** "make GET request to API endpoint"
    - **Expected:** `get` in api/http_client.py
    - **Tests:** HTTP method understanding

18. **Query:** "send POST request with JSON data"
    - **Expected:** `post` in api/http_client.py
    - **Tests:** HTTP operations

19. **Query:** "upload file to server"
    - **Expected:** `upload_file` in api/http_client.py
    - **Tests:** Specific task identification

20. **Query:** "retry failed API calls"
    - **Expected:** `retry_request` in api/http_client.py
    - **Tests:** Error handling patterns

### Payment Processing

21. **Query:** "process credit card payment"
    - **Expected:** `charge_credit_card` in services/payment_processor.py
    - **Tests:** Payment domain knowledge

22. **Query:** "calculate payment processing fees"
    - **Expected:** `calculate_processing_fee` in services/payment_processor.py
    - **Tests:** Financial calculations

23. **Query:** "issue refund to customer"
    - **Expected:** `refund_payment` in services/payment_processor.py
    - **Tests:** Payment operations

24. **Query:** "set up recurring billing"
    - **Expected:** `create_subscription` in services/payment_processor.py
    - **Tests:** Synonym (recurring/subscription)

### User Management

25. **Query:** "check user has admin permission"
    - **Expected:** `has_permission` in models/user.py
    - **Tests:** Authorization concepts

26. **Query:** "deactivate user account"
    - **Expected:** `deactivate_account` in models/user.py
    - **Tests:** Account management

27. **Query:** "get all active users"
    - **Expected:** `get_active_users` in models/user.py
    - **Tests:** Filtering operations

28. **Query:** "search users by email"
    - **Expected:** `search_users_by_email` in models/user.py
    - **Tests:** Search functionality

### Algorithms & Math

29. **Query:** "sort array using quicksort"
    - **Expected:** `quick_sort` in algorithms/sorting.py
    - **Tests:** Algorithm knowledge

30. **Query:** "binary search in sorted list"
    - **Expected:** `binary_search` in algorithms/sorting.py
    - **Tests:** Algorithm understanding

31. **Query:** "calculate compound interest"
    - **Expected:** `compound_interest` in math/calculations.py
    - **Tests:** Financial mathematics

32. **Query:** "check if number is prime"
    - **Expected:** `is_prime` in math/calculations.py
    - **Tests:** Mathematical concepts

33. **Query:** "calculate mean median mode"
    - **Expected:** `calculate_statistics` in math/calculations.py
    - **Tests:** Statistical operations

34. **Query:** "generate fibonacci sequence"
    - **Expected:** `fibonacci` in math/calculations.py
    - **Tests:** Well-known algorithms

## Evaluation Metrics

- **Recall@1:** Expected function is the top result
- **Recall@3:** Expected function is in top 3 results  
- **Recall@5:** Expected function is in top 5 results

## Usage

Run searches:
```bash
python search.py "check if password is strong enough"
python search.py "validate email address format"
python search.py "process credit card payment"
```

Check if the expected function appears in the results and at what rank.

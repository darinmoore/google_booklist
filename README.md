# Google Books Reading List

## Summary

Command line application using Google Books API to search for books and create a reading list.

Application allows the user to:

* Make a query for a book and displays the top 5 results
* Save one of the five displayed to a reading list
* View a reading list with all the books that have been previously saved

## Dependencies

The main program is dependent on *requests* and the tests are dependent on *pytest* library.

```
pip install pytest
pip install requests
```

## To Run

Program (requires python3.7):

```
python google_booklist.py
```

Tests:

```
pytest tests.py
```


## My Process

1. Research Google Books API / Refresher on JSON object layout.
2. Break down problem into subproblems and outline with possible functions for each subproblem.
3. For each of the subproblems I would prototype in the REPL, create unit tests, and then write the function.
4. Created a diagram of basic flow of the program, relating the different functions together.
5. Wrote and tested the code that interacted with the user.
6. Received and reviewed feedback.
7. Prioritized what to revise and implemented revisions.

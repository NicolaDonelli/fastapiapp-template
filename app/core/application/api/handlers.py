"""
Module containing base exception handlers.

Generic or common exceptions should be handled here, unless on of the following condition holds
(in that case a custom exception should be handled separately)
Cases for domain specific
* Adding new fields into the error description which aren't only tied to id and message requiring
the developer to extend the base error
* Handling the HTTP response differently, for any reason
"""

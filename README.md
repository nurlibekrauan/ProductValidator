# ProductValidator
ProductValidator is a Python project that includes classes for validating product attributes (name, price, quantity) and logging all changes to the object. This code demonstrates the use of object-oriented programming, decorators, and managing object state using descriptors.
# ProductValidator

This project contains a Python class for validating product attributes like name, price, and quantity. It also includes logging functionality to track changes made to the object.

## Features:
- Validates name, price, and quantity.
- Logs all changes to a log file.
- Demonstrates object-oriented programming and decorators in Python.

## Usage:

```python
product = Product(name="Laptop", price=99, quantity=10, obj_name="Product1")
print(product.total_sum())

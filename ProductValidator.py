class ProductValidator:
    def verify_name(self, name, min_length, max_length):
        if not isinstance(name, str):
            raise ValueError("Name must be a string")
        if not (min_length <= len(name) <= max_length):
            raise ValueError(
                f"Name must be between {min_length} and {max_length} characters long"
            )

    def verify_price(self, price, min_price, max_price):
        if not isinstance(price, (int, float)):
            raise ValueError("Price must be a number")
        if not (min_price <= price <= max_price):
            raise ValueError(f"Price must be between {min_price} and {max_price}, given price: {price}")

    def verify_quantity(self, quantity, min_quantity, max_quantity):
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Quantity must be a positive integer")
        if not (min_quantity <= quantity <= max_quantity):
            raise ValueError(
                f"Quantity must be between {min_quantity} and {max_quantity}"
            )

    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __set__(self, instance, value):
        class_name = instance.__class__.__name__
        obj_name = getattr(instance, "_obj_name", "Unknown Object")  # Object's name

        # Validate attribute values
        if self.name == "_name":
            self.verify_name(value, **self.kwargs)
        elif self.name == "_price":
            self.verify_price(value, **self.kwargs)
        elif self.name == "_quantity":
            self.verify_quantity(value, **self.kwargs)

        # Log changes
        with open(f"log_{class_name}.log", "a+", encoding="utf-8") as f:
            f.write(
                f"Object '{obj_name}' of class {class_name} changed attribute '{self.name[1:]}' "
                f"to '{value}'\n"
            )

        # Set new attribute value
        setattr(instance, self.name, value)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name)


class Logger:
    def __call__(self, cls):
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if callable(attr) and not attr_name.startswith("__"):
                setattr(cls, attr_name, self.decorator(attr))
        return cls  # Return class after decorating its methods

    def decorator(self, func):
        def wrapper(instance, *args, **kwargs):
            class_name = instance.__class__.__name__
            obj_name = getattr(instance, "_obj_name", "Unknown Object")  # Object's name
            with open(f"log_{class_name}.log", "a+", encoding="utf-8") as f:
                f.write(
                    f"Object '{obj_name}' of class '{class_name}' called method '{func.__name__}' with parameters {args} {kwargs}\n"
                )
            return func(instance, *args, **kwargs)

        return wrapper


@Logger()
class Product:
    name = ProductValidator(min_length=3, max_length=50)
    price = ProductValidator(min_price=1, max_price=10000000000000)
    quantity = ProductValidator(min_quantity=1, max_quantity=100000000000)

    def __init__(self, name, price, quantity, obj_name="UnnamedProduct"):
        self._obj_name = obj_name  # Object's name
        self.name = name
        self.price = price
        self.quantity = quantity

        # Get class name and instance attributes
        class_name = self.__class__.__name__
        attributes = self.__dict__

        # Log initialization of the object
        with open(f"log_{class_name}.log", "a+", encoding="utf-8") as f:
            f.write(
                f"Object '{self._obj_name}' of class {class_name} "
                f"was initialized with attributes:\n"
            )
            for attr, value in attributes.items():
                f.write(f"{attr}: {value}\n")

    def total_sum(self):
        return self.price * self.quantity


# Example usage
product = Product(name="Laptop", price=99, quantity=10, obj_name="Product1")
print(product.name)  # "Laptop"
print(product.price)  # 999
print(product.quantity)  # 10

# Modifying attributes
product.price = 1200  # This change will be logged
print(product.total_sum())

# Example validation error
# product = Product(name="L", price=999, quantity=10, obj_name="Product2")  # Error: Name must be between 3 and 50 characters long

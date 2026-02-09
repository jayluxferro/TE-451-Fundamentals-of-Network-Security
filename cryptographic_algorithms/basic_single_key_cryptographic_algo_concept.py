"""
Simple Single Key Cryptographic Algorithm Concept

Description:
The symbols of a particular message are transformed using a transformation function.
The same transformation function can be used to revert back to the original message.
"""

__author__ = "Jay Lux Ferro"
__email__ = "jay@knust.edu.gh"

def transform(data: str) -> str:
    _data = [ord(c) * 3 for c in tuple(data)]
    return ''.join([chr(c) for c in _data])

def revert(transformed_data: str) -> str:
    _data = [int(ord(c) / 3) for c in tuple(transformed_data)]
    return ''.join([chr(c) for c in _data])


message = input("Enter a message: ")
print("Input message:", message)

transformed_message = transform(message)
print("Transformed message:", transformed_message)

print("Reverted message:", revert(transformed_message))

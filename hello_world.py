#!/usr/bin/env python3
"""
Simple Hello World Program
A basic Python program demonstrating clean code practices.
"""

def main():
    """
    Main function that prints a greeting message.
    """
    print("Hello, World!")
    print("This is a sample Python program created in the workspace.")
    
    # Demonstrate basic functionality
    name = input("What's your name? ")
    greet_user(name)

def greet_user(name: str) -> None:
    """
    Greet a user by name.
    
    Args:
        name (str): The user's name
    """
    if name.strip():
        print(f"Nice to meet you, {name}!")
    else:
        print("Hello there, anonymous user!")

if __name__ == "__main__":
    main()
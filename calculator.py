# calculator.py

def add(a, b):
    """Menambahkan dua angka."""
    # Bug: Tidak ada konversi tipe data, akan menggabungkan string
    return a + b

def subtract(a, b):
    """Mengurangkan dua angka."""
    # Fungsi ini sengaja dibuat benar sebagai kontrol
    return int(a) - int(b)

def multiply(a, b):
    """Mengalikan dua angka."""
    # Bug: Operator yang digunakan salah
    return a + b

def divide(a, b):
    """Membagi dua angka."""
    # Bug: Tidak ada penanganan untuk pembagian dengan nol
    return int(a) / int(b)

if __name__ == '__main__':
    print("Testing Calculator Functions:")
    print(f"Add '5' + '3' = {add('5', '3')}") # Seharusnya 8, tapi akan menghasilkan '53'
    print(f"Subtract 10 - 2 = {subtract(10, 2)}") # Benar
    print(f"Multiply 5 * 3 = {multiply(5, 3)}") # Seharusnya 15, tapi akan menghasilkan 8
    try:
        print(f"Divide 10 / 0 = {divide(10, 0)}") # Akan menyebabkan crash
    except Exception as e:
        print(f"Error dividing by zero: {e}")
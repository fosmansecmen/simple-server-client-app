import socket, threading
from _thread import *
from product import Product
from basket import Basket

# Predefine the products and append them on a list, as we dont have a DB
pen = Product('PEN', 'Lana Pen', 5)
tshirt = Product('TSHIRT', 'Lana Tshirt', 20)
mug = Product('MUG', 'Lana Mug', 7.5)
products = [pen, tshirt, mug]
# Predefine a list that will save the Basket instances
baskets = []


# print_lock = threading.Lock()
port = 12359

def remove_basket(basket_name):
    for basket in baskets:
        if basket.name == basket_name:
            baskets.remove(basket)

def checkout(basket_name):
    for basket in baskets:
        if basket.name == basket_name:
            txt = ''
            total = 0
            for product in basket.products:
                txt += product.code + ','
                total += product.price

            info = {'text': txt[:-1], 'amount': str(total)+'€'}
            return info

    return None

def add_product_to_basket(option, basket_name):
    if option=='pen':
        product = pen
    elif option=='tshirt':
        product = tshirt
    elif option=='mug':
        product = mug

    for basket in baskets:
        if basket.name == basket_name:
            basket.add_product(product)
            print('basket:', basket.name)
            print('products:', basket.print_products())


def handle_input(c, data):
    if data=='help':
        txt = """Available commands:
            quit
            help
            create basket {basketname}
            remove basket {basketname}
            add product {options} {basketname}
                * available options are: pen, tshirt, mug
            checkout {basketname}
        """
        c.send(txt.encode('ascii'))
    elif 'create basket' in data:
        basket_name = data.split(" ")[2]
        c.send(('Creating basket with name ' + basket_name).encode('ascii'))
        basket_name = Basket(basket_name)
        baskets.append(basket_name)
        print('Basket is created')
        print('baskets:', baskets)
    elif 'remove basket' in data:
        basket_name = data.split(" ")[2]
        c.send(('Removing basket with name ' + basket_name).encode('ascii'))
        remove_basket(basket_name)
        print('Basket is removed')
        print('baskets:', baskets)
    elif 'add product' in data:
        data = data.split(" ")
        product = data[2]
        basket_name = data[3]
        c.send(('Adding ' + product + ' to ' + basket_name).encode('ascii'))
        add_product_to_basket(product, basket_name)
        print(product + ' is added to the ' + basket_name)
    elif 'checkout' in data:
        basket_name = data.split(" ")[1]
        c.send(('Gathering checkout info for ' + basket_name).encode('ascii'))
        info = checkout(basket_name)
        print('checkout:', info)
    else:
        c.send('This is beyond my knowledge'.encode('ascii'))


# thread function
def threaded(c):
    data = c.recv(1024)
    data = str(data.decode('ascii'))
    print('Received from the client :', data)
    c.send('Welcome message'.encode('ascii'))
    while True:
        # data received from client
        data = c.recv(1024)
        data = str(data.decode('ascii'))
        print('The client says :', data)
        if data=='quit':
            print('Bye')
            # lock released on exit
            # print_lock.release()
            break
        else:
            handle_input(c, data)

    # connection closed
    c.close()


def main():
    host = ""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")

    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        c, addr = s.accept()

        # lock acquired by client
        # print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))
    s.close()

if __name__ == '__main__':
    main()



import socket, threading, json
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
port = 12363

# for debugging purposes
def get_basket_names():
    basket_names = ""
    for basket in baskets:
        basket_names += basket.name + ', '

    return basket_names[:-1]

# for debugging purposes
def product_codes():
    product_codes = ""
    for product in products:
        product_codes += product.code + ', '

    return product_codes[:-1]

# check basket name if it exists, and return the instance, else return None
def get_basket(basket_name):
    for basket in baskets:
        if basket.name.lower() == basket_name.lower():
            return basket
    return None

# check product name if it exists, and return the instance, else return None
def get_product(product_name):
    for product in products:
        if product.code.lower() == product_name.lower():
            return product
    return None
"""
This is to send the same message to the client and print on server's debugging log
"""
def print_message(message, client):
    client.send(message.encode('ascii'))
    print(message)

# validate input and handle it
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
        if len(data.split(" "))<3:
            print_message('Missing argument, please check it', c)
        else:
            basket_name = data.split(" ")[2]
            # get the basket instance
            basket = get_basket(basket_name)
            # check if it already exists
            if not basket==None:
                print_message('A basket with this name already exists.', c)
            else:   # if not, create it
                new_basket = Basket(basket_name)
                baskets.append(new_basket)
                print_message('Basket is created. Baskets: ' + get_basket_names(), c)
    elif 'remove basket' in data:
        if len(data.split(" "))<3:
            print_message('Missing argument, please check it', c)
        else:
            basket_name = data.split(" ")[2]
            # get the basket instance
            basket = get_basket(basket_name)
            # check if it exists
            if basket==None:
                print_message('Basket does not exist. Baskets: ' + get_basket_names(), c)
            else:
                baskets.remove(basket)
                del basket
                print_message('Basket is removed. Baskets: ' + get_basket_names(), c)
    elif 'add product' in data:
        if len(data.split(" "))<4:
            print_message('Missing argument, please check it', c)
        else:
            data = data.split(" ")
            product_name = data[2]
            # get the product instance
            product = get_product(product_name)
            if product==None:
                # TO BE TESTED
                print_message('Product does not exist. Products: ' + product_codes(), c)
            else:
                basket_name = data[3]
                # get the basket instance
                basket = get_basket(basket_name)
                # check if it exists
                if basket==None:
                    print_message('Basket does not exist. Baskets: ' + get_basket_names(), c)
                else:
                    basket.add_product(product)
                    print_message(product_name + ' is added to the ' + basket_name, c)
    elif 'checkout' in data:
        if len(data.split(" "))<2:
            print_message('Missing argument, please check it', c)
        else:
            basket_name = data.split(" ")[1]
            # get the basket instance
            basket = get_basket(basket_name)
            # check if it exists
            if basket==None:
                print_message('Basket does not exist. Baskets: ' + get_basket_names(), c)
            else:
                info = basket.checkout()
                info = '\nItems: ' + info.get('ITEMS') + '\n' + 'Total: ' + str(info.get('TOTAL'))
                print_message(info, c)
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



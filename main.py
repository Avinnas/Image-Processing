
import imageio
import imghdr
import bmpContainer
def __main__():

    image = bmpContainer.bmpContainer('test.bmp')
    choice = -1
    while(choice!= 0):
        print_menu()
        choice = int(input())
        if choice == 1:
            path = input("Path of image to load:\n")
            image = bmpContainer.bmpContainer(path)
        elif choice == 2:
            image.show_data()
        elif choice == 3:
            index = int(input("Before which index?\n"))
            how_many = int(input("How many bytes?\n"))
            image.insert_random_bytes(index, how_many)
        elif choice == 4:
            image.remove_data_from_header()
            image.remove_first_gap()
            image.remove_second_gap()
            image.remove_last_gap()
        elif choice == 5:
            image.display_color_tables()
        elif choice == 6:
            image.display_icc_profiles()
        elif choice == 7:
            path = input("Choose path to save image:\n")
            image.save_image(path)
def print_menu():
    print("\n\nMenu of Image processing program: ")
    print("\t 1 - Load image (default - test.bmp is loaded)")
    print("\t 2 - Show image information")
    print("\t 3 - Add random bytes to image")
    print("\t 4 - Remove unnecessary information")
    print("\t 5 - Show color tables")
    print("\t 6 - Show ICC profiles")
    print("\t 7 - Save image")
    print("Choose one of these numbers:\n\n")







__main__()
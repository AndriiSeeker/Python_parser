import requests
from bs4 import BeautifulSoup as BS


def record_to_file(full_list):
    with open("records.txt", "a", encoding="utf-8") as file:
        for el in full_list:
            for key, value in el.items():
                file.write(f"The price of the house: {key} ({value[0]}, {value[1]}), link: {value[2]}\n")


def editing_str_size(size):
    correct_str = ""
    for char in size:
        if (char == "²" and size[-1] != "²") or char == "и":
            correct_str = correct_str + char + ", "
        else:
            correct_str += char
    return correct_str


def correcting_price(price):
    for num in price:
        if not num.isdigit() and num != 0:
            price = price.replace(num, "")
        else:
            break
    return price


def converting_to_int(price):
    correct_price = price
    correct_price = correct_price.replace("$", "").replace(" ", "").replace("від", "")
    correct_price = int(correct_price)
    return correct_price


def sorting(house_full_price, house_price, house_size, house_url):
    full_list = []
    for num in range(len(house_full_price)):
        house = {house_full_price[num].text: [editing_str_size(house_size[num].text), correcting_price(house_price[num].text),
                                              "https://dom.ria.com/" + house_url[num].get('href')]}
        tech_house_price = converting_to_int(house_full_price[num].text)
        # setting the desired price
        if (tech_house_price < 100000) and (tech_house_price > 70000):
            full_list.append(house)
    record_to_file(full_list)


def main():
    # setting the necessary pages to view
    page_number = 1
    last_page = 5
    while page_number <= last_page:
        url = "https://dom.ria.com/uk/prodazha-domov/?page=" + str(page_number)
        response = requests.get(url)
        if response.status_code == 200:
            pass
        else:
            continue

        html_soup = BS(response.text, "html.parser")
        lxml_soup = BS(response.content, features='lxml')

        house_full_price = html_soup.find_all('b', class_="size18")
        house_size = html_soup.find_all('div', class_="mt-10 chars grey")
        house_price = html_soup.find_all('span', class_="size14 grey")
        house_url = lxml_soup.findAll(class_="realty-photo all-clickable is_shadow")

        sorting(house_full_price, house_price, house_size, house_url)
        page_number += 1
    print("The work is done")


if __name__ == '__main__':
    main()

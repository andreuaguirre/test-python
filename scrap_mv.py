from bs4 import BeautifulSoup
import requests

OFF_TOPIC = "off-topic"
HILO = "sanchez-considera-autonomia-sahara-para-resolver-conflicto-684716"
PAGE = 1

def get_hilo_html(subforo, name, page):
    response = requests.get(f"https://www.mediavida.com/foro/{subforo}/{name}/{page}")
    return response.text

def get_users(html):
    soup = BeautifulSoup(html, 'html.parser')
    username_links = soup.select('a.autor')
    usernames = []
    for link in username_links:
        usernames.append(link.text)

    return usernames

def get_last_page(subforo, hilo):
    first_page = get_hilo_html(subforo, hilo, 1)
    soup = BeautifulSoup(first_page, 'html.parser')
    last = soup.select_one('ul.side-pages').select(":last-child")[-1].text
    return int(last)

def get_all_users(subforo, hilo):
    last_page = get_last_page(subforo, hilo)
    total_users = []
    for page in range(last_page):
        users_on_page = get_users(get_hilo_html(subforo, hilo, page))
        total_users = total_users + users_on_page

    return total_users

result = get_all_users(OFF_TOPIC, HILO)

print(result)

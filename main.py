import json
import re
import requests
import bs4


def get_connection(url, headers):
    response = requests.get(url, headers=headers)
    html = response.text
    return html


def parse_vacancies(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    vacancies = soup.find_all("div", class_="vacancy-search-item__card")

    parse_data = []

    for vacancy in vacancies:
        try:
            link = vacancy.find("a", class_="bloko-link").get("href")

            company_ = vacancy.find("a", class_="bloko-link bloko-link_kind-secondary").text.strip()
            company = " ".join(company_.split())

            city_ = vacancy.find("span", {"data-qa": "vacancy-serp__vacancy-address"}).text.strip()
            city = " ".join(city_.split())

            salary_tag = vacancy.find("span",
                                      class_="fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni "
                                             "compensation-text--kTJ0_rp54B2vNeZ3CTt2 "
                                             "separate-line-on-xs--mtby5gO4J0ixtqzW38wh")

            salary_ = salary_tag.text.strip() if salary_tag else "Не указана"
            salary = " ".join(salary_.split())

            html_vacancy = get_connection(link, headers=headers)
            soup_vacancy = bs4.BeautifulSoup(html_vacancy, 'html.parser')
            description = soup_vacancy.find("div", class_="g-user-content").text.lower()

            pattern = r"django|flask"
            result = re.search(pattern, description)
            if result:
                parse_data.append({
                    "link": link,
                    "company": company,
                    "salary": salary,
                    "city": city
                })
        except AttributeError as error:
            print(f"Ошибка при парсинге вакансий: {error}")
            continue
    return parse_data


if __name__ == '__main__':
    url = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"
    headers = {
        "User-Agent": "Chrome/126.0.6478.127, (****@***.**)"
    }
    html = get_connection(url, headers)
    vacancies_info = parse_vacancies(html)
    with open("info.json", "w", encoding="utf-8") as f:
        json.dump(vacancies_info, f, ensure_ascii=False, indent=2)

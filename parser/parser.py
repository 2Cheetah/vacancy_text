import httpx
import re
import json
import html
from markdownify import markdownify as md
from formatter import format, formatter


def parse_text(groq_client, url):
    r = fetchHtml(url)
    trimmed = trimUnnecessary(r)
    trimmed = '{"' + trimmed
    writeToFile(trimmed, './data/vacancies.json')
    text = read_from_file('./data/vacancies.json')
    ready_text = prepare_data(groq_client, text, url)
    return ready_text


def trimUnnecessary(r):
    m = re.search(r"(topLevelSite.*)</template", r.text)
    return m.group(1)


def fetchHtml(url):
    c = {
        'hhrole': 'anonymous',
        'regions': '1',
        'display': 'desktop',
        'region_clarified': 'hh.ru',
        'GMT': '4',
        'redirect_host': 'hh.ru',
    }

    h = {
        'accept': 'text/html,application/xhtml+xml,application/xml',
        'accept-language': 'en,ru-RU',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }
    r = httpx.get(url=url, headers=h, cookies=c)
    return r


def writeToFile(s, filename):
    with open(filename, 'w+', encoding='utf-8') as f:
        f.write(s)


def read_from_file(filename):
    with open(filename, "r", encoding='utf-8') as f:
        text = f.read()
    return text


def prepare_data(groq_client, text, url):
    data = json.loads(text)
    vacancy_name = parse_title(data)
    company_name = parce_company_name(data)
    compensation = parse_compensation(data)
    location = parse_location(data)
    description = parse_description(groq_client, data)
    footer = parse_footer(url)

    ready_text = f"""{vacancy_name}

{company_name}
{compensation}
{location}

{description}

{footer}
"""
    return ready_text


def parse_title(data):
    try:
        vacancy_name = data["vacancyView"]["name"]
        return f"*Вакансия: {vacancy_name}*"
    except KeyError:
        return ""


def parce_company_name(data):
    try:
        company_name = data["vacancyView"]["company"]["name"]
        return f"*Компания:* {company_name}"
    except KeyError:
        return ""


def parse_location(data):
    try:
        display_name = data["vacancyView"]["address"]["displayName"]
        return f"*Локация:* {display_name}"
    except KeyError:
        return ""


def parse_compensation(data):
    try:
        compensation_from = data["vacancyView"]["compensation"]["from"]
        compensation_string = f"*ЗП:* от {compensation_from}"
    except KeyError:
        return "*ЗП:* не указана"

    try:
        compensation_to = data["vacancyView"]["compensation"]["to"]
        compensation_string += f" до {compensation_to}"
    except KeyError:
        pass

    try:
        gross = data["vacancyView"]["compensation"]["gross"]
        if gross:
            compensation_string += " до вычета налогов"
        elif not gross:
            compensation_string += " после вычета налогов"
        return compensation_string
    except KeyError:
        return compensation_string
    

def parse_description(groq_client, data):
    try:
        description = data["vacancyView"]["description"]
        description = html.unescape(description)
        description = description.replace('\u200b', '')

        formatted_description = formatter.format_text(groq_client, description, format.FORMAT)
        return formatted_description

    except KeyError:
        return ""


def parse_footer(url: str) -> str:
    footer = f"*Откликнуться:* f{url}"
    return footer
    

if __name__ == "__main__":
    text = read_from_file('./vacancies.json')
    data_hash = prepare_data(text)
    print(data_hash["vacancy_name"], data_hash["company_name"])

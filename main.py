import re
from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


# TODO 1: выполните пункты 1-3 ДЗ

for i in range(1, len(contacts_list)):
    contact = contacts_list[i]
    new_full_name_str = " ".join(contact[:3])
    new_full_name_list = new_full_name_str.split(" ")
    contacts_list[i][:3] = new_full_name_list[:3]

phone_pattern = re.compile(
    r"(\+7|8)?\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})(?:[\s-]*\(?доб\.?\s*(\d+)\)?)?"
)
phone_substitution = r"+7(\2)\3-\4-\5 доб.\6"

for contact in contacts_list[1:]:
    if "доб." not in contact[5]:
        new_phone_substitution = phone_substitution.replace(' доб.', '')
        contact[5] = re.sub(phone_pattern, new_phone_substitution, contact[5])
    else:
        new_contact = contact[5].replace(" доб.", "")
        contact[5] = re.sub(phone_pattern, phone_substitution, new_contact)

# pprint(contacts_list)

contacts_dict = {}
for contact in contacts_list[1:]:
    key = (contact[0], contact[1])
    if key in contacts_dict:
        existing_contact = contacts_dict[key]
        for i in range(3, len(contact)):
            if not existing_contact[i]:
                existing_contact[i] = contact[i]
            elif contact[i] and existing_contact[i] != contact[i]:
                existing_contact[i] += f"; {contact[i]}"
    else:
        contacts_dict[key] = contact

contacts_list = [contacts_list[0]] + list(contacts_dict.values())



# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    # Вместо contacts_list подставьте свой список
    datawriter.writerows(contacts_list)

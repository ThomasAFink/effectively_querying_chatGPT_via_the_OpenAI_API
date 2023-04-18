import os
import csv
import openai
import time

openai.api_key = "YOUR_API_SECRET_KEY"

OS_PATH = os.path.dirname(os.path.realpath('__file__'))
input_csv_file_path = OS_PATH + "/data/munich_company_list_input.csv"
output_csv_file_path = OS_PATH + "/output/munich_company_list_output.csv"


def get_keywords_from_gpt3(company_name, GPTModel):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Give me exactly 50 simple keywords only separated by commas for the following company. Include no periods at the end.  Include the entire company name, all parts of the company name, stock market symbol, city, state, country, and CEO name. No hashtags. No sentences. No sentence fragments. No special characters.\n \n  {company_name}"}
    ]

    while True:
        try:
            completion = openai.ChatCompletion.create(
                model=GPTModel,
                messages=messages,
                max_tokens=200,
                temperature=0.01,
            )

            keywords = completion.choices[0].message.content.strip()
            if keywords.count(',') >= 30:  # Check if there are at least 30 keywords
                return keywords
            else:
                # Add a new message to the conversation, stating it didn't follow the instructions
                messages.append({"role": "user", "content": f"Give me exactly 41 simple keywords only separated by commas for the following company. Include no periods at the end.  Include the entire company name, all parts of the company name, stock market symbol, city, state, country, and CEO name. No hashtags. No sentences. No sentence fragments. No special characters.\n \n  {company_name}"})
        except openai.error.RateLimitError as e:
            print("Rate limit error. Waiting for 61 seconds.")
            time.sleep(61)
        except openai.error.APIError as e:
            print("APIError encountered. Waiting for 30 seconds before retrying.")
            time.sleep(30)
        except openai.error.InvalidRequestError as e:
            print("APIError encountered. Waiting for 30 seconds before retrying.")
            time.sleep(30)

def get_description_from_gpt3(company_name, GPTModel):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Give me a 190 character limit description starting with 'Munich, Bavaria, Germany - March 31 2023: ', for the following company. The start of the description is irrelevant to the actual description, but this prefix counts in the character count. No hashtags.\n \n   {company_name}"}
    ]

    while True:
        try:
            completion = openai.ChatCompletion.create(
                model=GPTModel,
                messages=messages,
                max_tokens=200,
                temperature=0.1,
            )

            description = completion.choices[0].message.content.strip()
            return description
        except openai.error.RateLimitError as e:
            print("Rate limit error. Waiting for 61 seconds.")
            time.sleep(61)
        except openai.error.APIError as e:
            print("APIError encountered. Waiting for 30 seconds before retrying.")
            time.sleep(30)
        except openai.error.InvalidRequestError as e:
            print("APIError encountered. Waiting for 30 seconds before retrying.")
            time.sleep(30)

def get_location_from_gpt3(company_name, GPTModel):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Give me the location for the following company. The format should be: city, state, country\n \n   {company_name}"}
    ]

    while True:
        try:
            completion = openai.ChatCompletion.create(
                model=GPTModel,
                messages=messages,
                max_tokens=200,
                temperature=0.1,
            )

            location = completion.choices[0].message.content.strip()
            return location
        except openai.error.RateLimitError as e:
            print("Rate limit error. Waiting for 61 seconds.")
            time.sleep(61)
        except openai.error.APIError as e:
            print("APIError encountered. Waiting for 30 seconds before retrying.")
            time.sleep(30)
        except openai.error.InvalidRequestError as e:
            print("APIError encountered. Waiting for 30 seconds before retrying.")
            time.sleep(30)

def main():
    GPTModel = "gpt-3.5-turbo"

    with open(input_csv_file_path, mode='r') as input_csvfile:
        reader = csv.DictReader(input_csvfile)

        with open(output_csv_file_path, mode='w', newline='') as output_csvfile:
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(output_csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:

                company_name = row['Name']

                print("\n")
                print("******************************* "+ company_name + " ************************************")

                keywords = get_keywords_from_gpt3(company_name, GPTModel)
                print("Keywords : " + keywords)
                row['Keywords'] = keywords

                print("-------------------------------------------------------------------")
                description = get_description_from_gpt3(company_name, GPTModel)
                print("Description : " + description)
                row['Description'] = description

                print("-------------------------------------------------------------------")
                location = get_location_from_gpt3(company_name, GPTModel)
                print("Location : " + location)
                row['Location'] = location

                writer.writerow(row)

if __name__ == '__main__':
    main()
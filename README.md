# Effectively Querying ChatGPT via the OpenAI API

## Intro to Language Processing Models
The GPT (Generative Pre-trained Transformer) architecture, as its name implies, uses a Transformer architecture rather than an RNN (Recurrent Neural Network) as the foundation for ChatGPT-3. Due to their propensity for parallelization and their capacity for handling long-range dependencies, transformers have replaced RNNs as the preferred option for natural language processing tasks.

Traditional RNN
![image](https://github.com/ThomasAFink/effectively_querying_chatGPT_via_the_OpenAI_API/blob/main/img/rnn.jpg)

The Transformer architecture was introduced by a team of researchers from Google Brain and Google Research in a paper titled "Attention is All You Need." The paper was published in 2017, and the Transformer architecture has since become a significant milestone in the field of natural language processing. You can read it here: https://doi.org/10.48550/arXiv.1706.03762

GPT-3, an improved version of earlier GPT models, is generally considered to lack a separate encoder component, as indicated in the following OpenAI paper from 2018: https://paperswithcode.com/paper/improving-language-understanding-by. Therefore based on known information, contrary to the original Transformer architecture presented in the Google paper, GPT-3 is designed as a decoder-only variant. However, there is still some ongoing debate regarding this aspect because as it looks GPT-3 code won't be open sourced and it's hard to fathom it being a decoder-only variant. If true though, it is trained to predict the next token in a sequence based on the preceding tokens.

Encoder-Decoder Architecture:

* Input tokens are first processed by the encoder, which creates meaningful representations of the input sequence.
* The final representation from the encoder is passed to the decoder.
* The decoder generates output tokens one by one, often using an attention mechanism to weigh the importance of different input tokens when generating each output token.
* The process continues until an end-of-sequence token is produced or a predefined maximum length is reached.

Input Text → [Encoder] → Context Vector → [Decoder] → Output Text
![image](https://github.com/ThomasAFink/effectively_querying_chatGPT_via_the_OpenAI_API/blob/main/img/encoder_decoder.jpg)

Decoder-Only Architecture (e.g., GPT-3):

* The input tokens are directly fed into the decoder, which generates output tokens one by one.
* The decoder uses self-attention layers to weigh the importance of different input tokens when generating each output token.
* This is passed on to a Feed Forward Network, both work in combination with each other.
* The process continues until an end-of-sequence token is produced or a predefined maximum length is reached.

Input Prompt → [Decoder] → Output Text
![image](https://github.com/ThomasAFink/effectively_querying_chatGPT_via_the_OpenAI_API/blob/main/img/transformer_decoder.jpg)

With a chatbot, the model generates a response to a given input by treating the conversation history and the user's input as a prompt, and then predicting the most likely next tokens to form a coherent response.

Based on the 2018 OpenAI paper mentioned earlier, GPT-3, being a Transformer-based model, does not have a traditional context vector like the one used in the encoder-decoder architecture. Instead, GPT-3 employs a mechanism called self-attention to capture contextual information from the input tokens, which is then used to generate the output tokens.

Self-attention, is a form of soft attention, as it computes attention weights using a continuous function (softmax function in this case) rather than selecting a single input or a fixed set of inputs to attend to, as in hard attention. Soft attention allows the model to learn different levels of importance for each input token during training, enabling it to capture relationships and dependencies across various positions in the input sequence. This characteristic makes soft attention more flexible and expressive than hard attention.

When visualizing hard versus soft attention, it's helpful to think of them as different ways of assigning importance or weights to elements in a sequence (e.g., words in a sentence).

For soft attention imagine you have a sentence, "The cat is sitting on the mat." When applying soft attention, you might assign continuous importance weights to each word, with some words having more weight than others. These weights typically sum to 1. For example:

        The (0.05)
        cat (0.20)
        is (0.05)
        sitting (0.25)
        on (0.10)
        the (0.05)
        mat (0.30)
In this example, the words "sitting," "cat," and "mat" are assigned more importance than the other words. The continuous weights enable the model to learn varying levels of importance for each word.

For hard attention consider the same sentence, "The cat is sitting on the mat." With hard attention, you assign binary importance weights to each word, indicating whether it should be attended to (1) or not (0). For example:

        The (0)
        cat (1)
        is (0)
        sitting (1)
        on (0)
        the (0)
        mat (1)
In this example, only the words "cat," "sitting," and "mat" are attended to, while the other words are ignored. Hard attention forces the model to select a single input or a fixed set of inputs to attend to, making it less flexible than soft attention.

![image](https://github.com/ThomasAFink/effectively_querying_chatGPT_via_the_OpenAI_API/blob/main/img/attention.jpg)

Much of the provided explanation is based on inferences about the GPT-3 model's workings, drawing from the underlying Transformer architecture and available information from research papers and documentation. It is important to note that the specific implementation details and optimizations within GPT-3 are not fully disclosed, and the given explanations might not cover all aspects of the model's behavior.

## Sort Explanation of the Code

So basically ChatGPT is a wee bit more creative database you can use to help approach problems a traditional search engine cannot solve. For example maybe you need a description of something or a third opinion. Another usecase is of course fictional writing. Any factual answers received should be taken with a grain of salt at this point because they are still often incorrect. The following code tries to demonstrate how query ChatGPT more effectively.

## Our List of 20 Companies

We going through a list of companies, some are subsidaries, and generate a description, keywords, and location using ChatGPT-3.

        Name,Keywords,Description,Location
        BMW Group,,,
        Siemens AG,,,
        Allianz SE,,,
        MAN Truck & Bus AG,,,
        Munich Re Group,,,
        Linde AG,,,
        Infineon Technologies AG,,,
        Osram Licht AG,,,
        Rohde & Schwarz GmbH & Co KG,,,
        MTU Aero Engines AG,,,
        Sixt SE,,,
        ProSiebenSat.1 Media SE,,,
        Wacker Chemie AG,,,
        KraussMaffei Group GmbH,,,
        HypoVereinsbank,,,
        Fujitsu Technology Solutions GmbH,,,
        PwC Germany,,,
        KPMG AG,,,
        Airbus Defence and Space GmbH,,,
        Amazon Development Center Germany GmbH,,,
munich_company_list_input.csv

## Installation and Setting Things up

You don't need a ChatGPT pro account to access the api. They are two different products billed seperately.

        "Please note that the ChatGPT API is not included in the ChatGPT Plus subscription and are billed separately. The API has its own pricing, which can be found at https://openai.com/pricing. The ChatGPT Plus subscription covers usage on chat.openai.com only and costs $20/month."

You can get an api token at: https://platform.openai.com/account/api-keys 
![image](https://github.com/ThomasAFink/effectively_querying_chatGPT_via_the_OpenAI_API/blob/main/img/key.png)
Each query costs a small few cent fee but the first $18.00 are a free trial: https://openai.com/pricing
Monitor your usage at: https://platform.openai.com/account/usage
![image](https://github.com/ThomasAFink/effectively_querying_chatGPT_via_the_OpenAI_API/blob/main/img/pricing.png)

## Diving Into the Python Code

Before starting we need to install OpenAI Python library:

        pip3 install os
        pip3 install csv
        pip3 install openai
        pip3 install time

Then to start our file we need to import our installed packages:

        import os
        import csv
        import openai
        import time

The first section of the code sets the API key for accessing OpenAI's GPT-3 model, and defines the file paths for the input and output CSV files that will be used to store the data. 

        openai.api_key = "YOUR_API_SECRET_KEY"

        OS_PATH = os.path.dirname(os.path.realpath('__file__'))
        input_csv_file_path = OS_PATH + "/data/munich_company_list_input.csv"
        output_csv_file_path = OS_PATH + "/output/munich_company_list_output.csv"


The next section contains four functions, each of which sends a prompt to GPT-3 and returns the output generated by the model. The structure of these function is generally the same.

We use the standard model gpt-3.5-turbo, but other models such as GPT-4 are available as listed on the OpenAI website: https://platform.openai.com/docs/models/gpt-3-5. To get the results we want we need to be very exact with our prompts.

In the context of natural language processing, tokens refer to the individual units of a text that are used for analysis. They are the basic building blocks of a language and are generally defined as a sequence of characters that represent a meaningful unit, such as a word, number, or punctuation mark.

The process of separating a text into tokens or words is known as tokenization. This is frequently carried out as the first step in tasks involving natural language processing, such as sentiment analysis, text classification, and language modeling. Because so many natural language processing algorithms base their analyses on individual tokens, tokenization is required.

For example, in the sentence "I love to play tennis.", the tokens are "I", "love", "to", "play", "tennis", and ".". By breaking down the text into these individual units, natural language processing algorithms analyze the text more effectively and accurately. A smaller set for max tokens can sometimes help us narrow down precision for the response. As explained above with the transformer decoder.

The temperature parameter is a hyperparameter that controls the degree of randomness and creativity in the text generated by GPT-3. When the temperature parameter is set to a low value, such as 0.1 as in this code, the generated text will be very conservative and predictable. This means that the text will be more likely to contain common phrases and structures that are found in human language. On the other hand, when the temperature parameter is set to a high value, the generated text will be more creative and unpredictable, and it may contain unexpected phrases, structures, or even errors.

Since the api has a limit of 3 queries per minute we handle this error with a try catch to continue querying down the list.

get_keywords_from_gpt3(company_name): This function prompts GPT-3 to generate a list of 50 simple keywords for a given company name. The function creates a conversation between a user and a system in which the user asks for the keywords, and GPT-3 responds with the generated list. The function ensures that there are at least 30 keywords in the list before returning it, and if there are not, it prompts GPT-3 again with the same conversation prompt.

        def get_keywords_from_gpt3(company_name):
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Give me exactly 50 simple keywords only separated by commas for the following company. Include no periods at the end.  Include the entire company name, all parts of the company name, stock market symbol, city, state, country, and CEO name. No hashtags. No sentences. No sentence fragments. No special characters.\n \n  {company_name}"}
            ]

            while True:
                try:
                    completion = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
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

get_description_from_gpt3(company_name): This function prompts GPT-3 to generate a 190 character limit description for a given company name. The function creates a conversation between a user and a system in which the user asks for the description, and GPT-3 responds with the generated text. The returned text is then stripped of any leading or trailing whitespace and returned by the function.

        def get_description_from_gpt3(company_name):
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Give me a 190 character limit description starting with 'Munich, Bavaria, Germany - March 31 2023: ', for the following company. The start of the description is irrelevant to the actual description, but this prefix counts in the character count. No hashtags.\n \n   {company_name}"}
            ]

            while True:
                try:
                    completion = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
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

get_location_from_gpt3(company_name): This function prompts GPT-3 to generate the location (city, state, country) for a given company name. The function creates a conversation between a user and a system in which the user asks for the location, and GPT-3 responds with the generated text. The returned text is then stripped of any leading or trailing whitespace and returned by the function.

        def get_location_from_gpt3(company_name):
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Give me the location for the following company. The format should be: city, state, country\n \n   {company_name}"}
            ]

            while True:
                try:
                    completion = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
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

After defining these functions, the code opens the input CSV file and reads the data row by row. For each row, it extracts the company name and passes it to each of the four functions defined earlier to generate the keywords, description, and location. Each generated value is added to the corresponding column in the output CSV file.

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

## The Output Generated From ChatGPT-3
![image](https://github.com/ThomasAFink/effectively_querying_chatGPT_via_the_OpenAI_API/blob/main/img/output.png?raw=true)
munich_company_list_output.csv

## A Short Summary
This code shows an example of how to effectively query ChatGPT using the OpenAI API. It defines three functions that prompt GPT-3 to generate keywords, a description, and a location for a given company name. These functions use a conversation between a user and a system, and the generated outputs are added to an output CSV file. We can conclude that ChatGPT is better at creative tasks such as writing a description or a collection of keywords than it is at precision such as find a location or stock market ticker symbol.

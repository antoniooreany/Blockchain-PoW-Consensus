# # # # # # # #   Copyright (c) 2024, Anton Gorshkov
# # # # # # # #   All rights reserved.
# # # # # # # #
# # # # # # # #   This code is for a test_gpt and its unit tests.
# # # # # # # #   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com
# # # # # # #
# # # # # # #
# # # # # # # import openai
# # # # # # #
# # # # # # # # Ваш API-ключ
# # # # # # # openai.api_key = "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"
# # # # # # #
# # # # # # # try:
# # # # # # #     response = openai.Completion.create(
# # # # # # #         model="gpt-4",
# # # # # # #         prompt="Test if GPT-4 is available",
# # # # # # #         max_tokens=10
# # # # # # #     )
# # # # # # #     print("GPT-4 is available.")
# # # # # # # except openai.error.InvalidRequestError as e:
# # # # # # #     print(f"Error: {e}")
# # # # # # #     print("GPT-4 is not available for your account.")
# # # # # # from venv import logger
# # # # # #
# # # # # # import openai
# # # # # # import os
# # # # # #
# # # # # # # Получаем API ключ из переменной окружения
# # # # # # openai.api_key = os.getenv("GAS_OPENAI_API_KEY")
# # # # # # logger.info(f"API key: {openai.api_key}")
# # # # # #
# # # # # # try:
# # # # # #     # Используем новый метод completions.create
# # # # # #     # response = openai.completions.create(
# # # # # #     #     model="gpt-3.5-turbo",  # Используйте gpt-3.5-turbo или gpt-4, если доступен
# # # # # #     #     prompt="Test if the model is working",
# # # # # #     #     max_tokens=50
# # # # # #     # )
# # # # # #
# # # # # #     response = openai.Completion.create(
# # # # # #         model="gpt-4",  # указываем модель gpt-4
# # # # # #         prompt="Ваш запрос",
# # # # # #         max_tokens=100
# # # # # #     )
# # # # # #
# # # # # #     print(response['choices'][0]['text'].strip())
# # # # # #
# # # # # # except openai.error.OpenAIError as e:
# # # # # #     # Правильная обработка ошибок с использованием OpenAIError
# # # # # #     print(f"An error occurred: {e}")
# # # # # #
# # # # #
# # # # # import openai
# # # # # import os
# # # # #
# # # # # # Получаем API ключ из переменной окружения
# # # # # openai.api_key = os.getenv("GAS_OPENAI_API_KEY")
# # # # #
# # # # # try:
# # # # #     # Используем правильный метод chat_completions.create для GPT-4
# # # # #     response = openai.chat_completions.create(
# # # # #         model="gpt-4",  # указываем модель gpt-4
# # # # #         messages=[
# # # # #             {"role": "system", "content": "You are a helpful assistant."},
# # # # #             {"role": "user", "content": "Test if GPT-4 is available"},
# # # # #         ],
# # # # #         max_tokens=100
# # # # #     )
# # # # #
# # # # #     # Печатаем результат
# # # # #     print(response['choices'][0]['message']['content'].strip())
# # # # #
# # # # # except openai.error.OpenAIError as e:
# # # # #     # Правильная обработка ошибок с использованием OpenAIError
# # # # #     print(f"An error occurred: {e}")
# # # # #
# # # # #
# # # #
# # # #
# # # #
# # # # import openai
# # # # import os
# # # #
# # # # # Получаем API ключ из переменной окружения
# # # # openai.api_key = os.getenv("GAS_OPENAI_API_KEY")
# # # #
# # # # try:
# # # #     # Используем правильный метод ChatCompletion.create для GPT-4
# # # #     response = openai.ChatCompletion.create(
# # # #         model="gpt-4",  # указываем модель gpt-4
# # # #         messages=[
# # # #             {"role": "system", "content": "You are a helpful assistant."},
# # # #             {"role": "user", "content": "Test if GPT-4 is available"},
# # # #         ],
# # # #         max_tokens=100
# # # #     )
# # # #
# # # #     # Печатаем результат
# # # #     print(response['choices'][0]['message']['content'].strip())
# # # #
# # # # except openai.error.OpenAIError as e:
# # # #     # Правильная обработка ошибок с использованием OpenAIError
# # # #     print(f"An error occurred: {e}")
# # # #
# # # #
# # # from venv import logger
# # #
# # # import openai
# # # import os
# # #
# # # # Получаем API ключ из переменной окружения
# # # openai.api_key = os.getenv("GAS_OPENAI_API_KEY")
# # # logger.info(f"API key: {openai.api_key}")
# # #
# # # try:
# # #     # Используем правильный метод openai.completions.create
# # #     response = openai.completions.create(
# # #         model="gpt-4",  # указываем модель gpt-4
# # #         messages=[
# # #             {"role": "system", "content": "You are a helpful assistant."},
# # #             {"role": "user", "content": "Test if GPT-4 is available"},
# # #         ],
# # #         max_tokens=100
# # #     )
# # #
# # #     # Печатаем результат
# # #     print(response['choices'][0]['message']['content'].strip())
# # #
# # # except openai.OpenAIError as e:
# # #     # Правильная обработка ошибок с использованием OpenAIError
# # #     print(f"An error occurred: {e}")
# # #
# # #
# #
# # import os
# # import openai
# #
# # # Access the environment variable
# # openai.api_key = os.getenv("GAS_OPENAI_API_KEY")
# #
# # if not openai.api_key:
# #     raise ValueError("API key not found! Please set the GAS_OPENAI_API_KEY environment variable.")
# #
# # try:
# #     response = openai.ChatCompletion.create(
# #         model="gpt-4",  # You may replace this with the model you're using
# #         messages=[
# #             {"role": "system", "content": "You are a helpful assistant."},
# #             {"role": "user", "content": "Test if GPT-4 is available."},
# #         ],
# #         max_tokens=100
# #     )
# #
# #     print(response['choices'][0]['message']['content'].strip())
# #
# # except openai.OpenAIError as e:
# #     print(f"An error occurred: {e}")
# #
# #
#
# import os
#
# # Print out the environment variable to verify if it's available
# api_key = os.getenv("GAS_OPENAI_API_KEY")
# print(f"API Key from environment: {api_key}")
#
# if not api_key:
#     raise ValueError("API key not found! Please set the GAS_OPENAI_API_KEY environment variable.")
#
# # Continue with your openai setup
# import openai
# openai.api_key = api_key
#
#


import openai

# Manually set your API key for testing purposes
openai.api_key = "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"

# Now, run your openai commands as normal
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Test if GPT-4 is available."},
    ],
    max_tokens=100
)

print(response['choices'][0]['message']['content'].strip())



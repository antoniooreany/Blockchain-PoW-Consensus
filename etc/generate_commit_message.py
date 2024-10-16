# # #   Copyright (c) 2024, Anton Gorshkov
# # #   All rights reserved.
# # #
# # #   This code is for a generate_commit_message and its unit tests.
# # #   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com
# # import os
# # from venv import logger
# #
# import openai
import subprocess
# #
# #
# # import os
# # import openai
# #
# # # Получаем API ключ из переменной окружения
# # api_key = os.getenv("GAS_OPENAI_API_KEY")
# #
# # if api_key:
# #     openai.api_key = api_key
# # else:
# #     raise ValueError("API ключ не найден! Проверьте переменные окружения или укажите API ключ напрямую.")
# #
# # # Ваш код для работы с OpenAI API
# #
# #
# #
# # # Установите ваш OpenAI API ключ
# # api_key = os.getenv("GAS_OPENAI_API_KEY")
# # logger.debug(f"API key: {api_key}")
# #
def get_git_diff():
    # Получение списка изменений через git diff
    diff = subprocess.check_output(['git', 'diff', '--cached'], universal_newlines=True)
    return diff
# #
# # def generate_commit_message(diff):
# #     # Пример запроса на генерацию осмысленного коммит-сообщения
# #     prompt = f"Generate a concise and meaningful commit message for the following git diff:\n{diff}\n"
# #     response = openai.Completion.create(
# #         engine="text-davinci-003",  # Или GPT-4, если доступно
# #         prompt=prompt,
# #         max_tokens=100,  # Максимальная длина сообщения
# #         n=1,
# #         stop=None,
# #         temperature=0.5
# #     )
# #     return response.choices[0].text.strip()
# #
# # def main():
# #     diff = get_git_diff()
# #     commit_message = generate_commit_message(diff)
# #     print(f"Suggested commit message: {commit_message}")
# #
# #     # Автоматическая передача сгенерированного сообщения в git
# #     subprocess.call(['git', 'commit', '-m', commit_message])
# #
# # if __name__ == '__main__':
# #     main()
# #
#
#
# import openai
# import os
#
# # Получаем API ключ из переменной окружения
# openai.api_key = os.getenv("GAS_OPENAI_API_KEY")
#
#
# def generate_commit_message(diff):
#     prompt = f"Generate a concise and meaningful commit message for the following git diff:\n{diff}\n"
#
#     # Используем новую модель GPT-3.5-turbo
#     response = openai.ChatCompletion.create(
#         # model="gpt-3.5-turbo",
#         model="gpt-4",
#         messages=[
#             {"role": "system", "content": "You are an assistant that generates git commit messages."},
#             {"role": "user", "content": prompt}
#         ]
#     )
#
#     return response.choices[0].message['content'].strip()
#
#
# def main():
#     diff = get_git_diff()
#     commit_message = generate_commit_message(diff)
#     print(f"Suggested commit message: {commit_message}")
#     # Автоматическая передача сгенерированного сообщения в git
#     subprocess.call(['git', 'commit', '-m', commit_message])
#
#
# if __name__ == '__main__':
#     main()
#


# import openai
# import os
#
# # Получаем API ключ из переменной окружения
# openai.api_key = os.getenv("GAS_OPENAI_API_KEY")
#
# def generate_commit_message(diff):
#     prompt = f"Generate a concise and meaningful commit message for the following git diff:\n{diff}\n"
#
#     # Используем GPT-4 для создания завершений
#     response = openai.ChatCompletion.create(
#         model="gpt-4",  # Используем модель GPT-4
#         messages=[
#             {"role": "system", "content": "You are an assistant that generates git commit messages."},
#             {"role": "user", "content": prompt}
#         ]
#     )
#
#     return response['choices'][0]['message']['content'].strip()
#
# def main():
#     diff = get_git_diff()  # Получаем git diff (предполагается, что у вас есть эта функция)
#     commit_message = generate_commit_message(diff)
#     print(f"Suggested commit message: {commit_message}")
#     # Коммит с сообщением
#     subprocess.call(['git', 'commit', '-m', commit_message])
#
# if __name__ == '__main__':
#     main()



import openai
import os

# Получаем API ключ из переменной окружения
openai.api_key = os.getenv("GAS_OPENAI_API_KEY")

def generate_commit_message(diff):
    prompt = f"Generate a concise and meaningful commit message for the following git diff:\n{diff}\n"

    # Новый синтаксис для создания завершений
    response = openai.completions.create(
        model="gpt-4",  # Используйте модель GPT-4, если у вас есть к ней доступ
        prompt=prompt,
        max_tokens=100
    )

    return response['choices'][0]['text'].strip()

def main():
    diff = get_git_diff()  # Предположим, что у вас есть функция для получения git diff
    commit_message = generate_commit_message(diff)
    print(f"Suggested commit message: {commit_message}")
    # Автоматическая передача сгенерированного сообщения в git
    subprocess.call(['git', 'commit', '-m', commit_message])

if __name__ == '__main__':
    main()



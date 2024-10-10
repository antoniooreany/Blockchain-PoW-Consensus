# # # # # #   Copyright (c) 2024, Anton Gorshkov
# # # # # #   All rights reserved.
# # # # # #   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com
#
#
# # #             if re.match(r'^\s*#.*(Copyright|All rights reserved|contact).*', line):
# # #             elif not re.match(r'^\s*#\s*[A-Za-z]+.*', line) and not re.match(r'^\s*#.*TODO.*', line):
# # import re
# # def remove_commented_code(file_path):
# #     with open(file_path, 'r', encoding='utf-8') as file:
# #         lines = file.readlines()
# #     with open(file_path, 'w', encoding='utf-8') as file:
# #         for line in lines:
# #             if re.match(r'^\s*#.*(Copyright|All rights reserved|contact).*', line):
# #                 file.write(line)
# #             elif not re.match(r'^\s*#\s*[A-Za-z]+.*', line) and not re.match(r'^\s*#.*TODO.*', line):
# #                 if not line.lstrip().startswith('#'):
# #                     file.write(line)
# #             else:
# #                 file.write(line)
# # file_path = 'gpt/full_blockchain.py'  # Replace with your file path
# # remove_commented_code(file_path)
#
#
# import re
#
#
# def remove_commented_code(file_path):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         lines = file.readlines()
#
#     with open(file_path, 'w', encoding='utf-8') as file:
#         inside_comment_block = False
#         for line in lines:
#             # Exclude lines with copyright and important information
#             if re.match(r'^\s*#.*(Copyright|All rights reserved|contact).*', line):
#                 file.write(line)
#             # Handle multi-line comments
#             elif line.strip().startswith('#'):
#                 if re.match(r'^\s*#\s*[A-Za-z]+.*', line) or re.match(r'^\s*#.*TODO.*', line):
#                     file.write(line)
#                 else:
#                     if not inside_comment_block:
#                         inside_comment_block = True
#             else:
#                 if inside_comment_block:
#                     inside_comment_block = False
#                 file.write(line)
#
#
# file_path = 'remove_comments.py'  # Replace with your file path
# remove_commented_code(file_path)


# def remove_commented_code(file_path):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         lines = file.readlines()
#
#     with open(file_path, 'w', encoding='utf-8') as file:
#         inside_comment_block = False
#         for line in lines:
#             if re.match(r'^\s*#.*(Copyright|All rights reserved|contact).*', line):
#                 file.write(line)
#             elif line.strip().startswith('#'):
#                 if re.match(r'^\s*#\s*[A-Za-z]+.*', line) or re.match(r'^\s*#.*TODO.*', line):
#                     file.write(line)
#                 else:
#                     if not inside_comment_block:
#                         inside_comment_block = True
#             else:
#                 if inside_comment_block:
#                     inside_comment_block = False
#                 file.write(line)


import re


def remove_commented_code(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(file_path, 'w', encoding='utf-8') as file:
        inside_comment_block = False
        for line in lines:
            # Exclude lines with copyright and important information
            if re.match(r'^\s*#.*(Copyright|All rights reserved|contact).*', line):
                file.write(line)
            # Handle multi-line comments
            elif line.strip().startswith('#'):
                if re.match(r'^\s*#\s*[A-Za-z]+.*', line) or re.match(r'^\s*#.*TODO.*', line):
                    file.write(line)
                else:
                    if not inside_comment_block:
                        inside_comment_block = True
            else:
                if inside_comment_block:
                    inside_comment_block = False
                file.write(line)


file_path = '../blockchain.py'  # Replace with your file path
remove_commented_code(file_path)

# def select_file():
#     file_path = filedialog.askopenfilename()
#     if file_path:
#         try:
#             remove_commented_code(file_path)
#             messagebox.showinfo("Success", "Comments removed successfully!")
#         except Exception as e:
#             messagebox.showerror("Error", f"An error occurred: {e}")
#
#
# app = tk.Tk()
# app.title("Remove Commented Code")
#
# frame = tk.Frame(app, padx=10, pady=10)
# frame.pack(padx=10, pady=10)
#
# label = tk.Label(frame, text="Select a file to remove commented code:")
# label.pack(pady=5)
#
# button = tk.Button(frame, text="Select File", command=select_file)
# button.pack(pady=5)
#
# app.mainloop()

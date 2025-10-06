import os

#6.09
# folder_structure = {
#     "S_6.09 HTML": {
#         "Assets": ["6.09.png"],
#         "FinalBRDs": ["applejuice.brd", "comicstrip.brd", "gail.brd", "groundhog.brd", "postoffice.brd",
#                       "roadtrip.brd"],
#         "HTML": {
#             "Assets": ["6.09.css"],
#             "": ["6.09.html"]
#         },
#         "MassProduction": []  # Empty folder
#     }
# }

#6.08
# folder_structure = {
#     "S_6.08 HTML": {
#         "Assets": ["6.08.png"],
#         "FinalBRDs": ["1.brd", "2.brd", "3.brd", "4.brd", "5.brd", "6.brd", "7.brd", "8.brd"],
#         "HTML": {
#             "Assets": ["6.08.css"],
#             "": ["6.08.html"]
#         },
#         "MassProduction": ["6_08_table.txt", "6.08_new_table.txt", "finalMassProdtable.txt",
#                            "finalTemplate.brd", "finalTemplateNew.brd", "mass_pro.brd",
#                            "template_6_06_08_10.brd", "translatable.txt"]
#     }
# }

#6.07
# folder_structure = {
#     "S_6.07 HTML": {
#         "Assets": ["6.07.png"],
#         "FinalBRDs": [
#             "bank-account.brd", "birthday.brd", "entertainment.brd", "fleece.brd",
#             "gardening.brd", "post-office.brd", "softball.brd", "vacation.brd"
#         ],
#         "HTML": {
#             "Assets": ["6.07.css"],
#             "": ["6.07.html"]
#         },
#         "MassProduction": [
#             "6_07_bank-account_finalMassProduction.txt", "6_07_bank-account_finalTemplate.brd",
#             "6_07_birthday_finalMassProduction.txt", "6_07_birthday_finalTemplate.brd",
#             "6_07_entertainment_finalMassProduction.txt", "6_07_entertainment_finalTemplate.brd",
#             "6_07_fleece_finalMassProduction.txt", "6_07_fleece_finalTemplate.brd",
#             "6_07_gardening_finalMassProduction.txt", "6_07_gardening_finalTemplate.brd",
#             "6_07_post-office_finalMassProduction.txt", "6_07_post-office_finalTemplate.brd",
#             "6_07_softball_finalMassProduction.txt", "6_07_softball_finalTemplate.brd",
#             "6_07_vacation_finalMassProduction.txt", "6_07_vacation_finalTemplate.brd"
#         ]
#     }
# }

#6.06
folder_structure = {
    "S_6.06 HTML": {
        "Assets": ["6.06.png"],
        "FinalBRDs": [
            "1-amy.brd", "2-molly.brd", "3-sydney.brd", "4-allison.brd",
            "5-charlie.brd", "6-jordan.brd", "7-martin.brd", "8-paul.brd",
            "9-lauren.brd"
        ],
        "HTML": {
            "Assets": [],  # Assuming no files listed directly under HTML/Assets based on the structure
            "": ["6.06.html"]
        },
        "MassProduction": [
            "6_06_table.txt", "6.06_new_table.txt", "finalMassProdtable.txt",
            "finalTemplate.brd", "finalTemplateNew.brd", "mass_pro.brd",
            "template_6_06_08_10.brd", "translatable.txt"
        ]
    }
}




base_directory = "/path/to/your/files"
target_directory = "/path/to/your/target"


def create_and_move_files(base_dir, target_dir, structure):
    for folder, contents in structure.items():
        folder_path = os.path.join(target_dir, folder)
        os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist

        if isinstance(contents, dict):
            # Recursive call to handle subdirectories
            create_and_move_files(base_dir, folder_path, contents)
        else:
            for file in contents:
                src = os.path.join(base_dir, file)
                dst = os.path.join(folder_path, file)
                if os.path.exists(src):
                    os.rename(src, dst)  # Move file
                else:
                    print(f"Warning: {src} does not exist and cannot be moved.")


create_and_move_files("S_6.06HTML", "6.06", folder_structure)

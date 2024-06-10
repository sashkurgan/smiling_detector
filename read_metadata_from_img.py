from sdparsers import ParserManager
import pandas as pd
import openpyxl
import os

images_folder = 'not_smiling_images' #parsed images from civitai
prompt_file = 'non_smiling_prompts.xlsx' # xlsx file for prompts

imgs=os.listdir(f'{images_folder}')




for i in range(len(imgs)):
    parser_manager = ParserManager()
    #get metadata from images
    prompt_info = parser_manager.parse(f"{images_folder}/{imgs[i]}")

    try:
        for prompt_parameters in prompt_info.prompts:
            id=imgs[i].split('.')[0]
            prompt = (prompt_parameters[0].value).replace('\n', ' ')
            prompt_table = pd.read_excel(f'{prompt_file}')
            prompt_table = prompt_table.append({"id": id, "prompt" : prompt}, ignore_index=True)
            prompt_table.to_excel(f'{prompt_file}', index=False)
            print(prompt_table)
            print(id, prompt)
    except:
        print(f"проблема с элементом номер {i}")
        continue
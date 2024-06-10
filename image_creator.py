import json
import os
import time

from torch import autocast
from diffusers import StableDiffusionKDiffusionPipeline
import webuiapi
import requests
import base64
import io
import ast
import pandas as pd
import openpyxl

prompts=pd.read_excel('non_smiling_prompts.xlsx')
prompts = prompts.iloc[:,:]


local_url='http://127.0.0.1:7860/'
batch_size = 10
for i in range(len(prompts)):
    if i%15 == 0:
        time.sleep(60)
    time.sleep(2)
    id_= prompts.iloc[i,0]
    prompt = prompts.iloc[i,1]
    if (prompt != 'NaN'):
        print(id_, prompt)
        positive_prompt = f"cinematic, complex background, 4k textures, {prompt}"
        negative_prompt = "(deformed, distorted, disfigured:1.3), totem, poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, (mutated hands and fingers:1.4), disconnected limbs, mutation, mutated, ugly, disgusting, blurry, amputation"

        txt2img_request= {
            #"enable_hr" : true,
            "prompt": positive_prompt,
            "negative_prompt" : negative_prompt,
            #"seed" : 2818096276,
            "width": 768,
            "height": 768,
            "steps": 5,
            "cfg_scale" : 1.5,
            "sampler_name": "DPM++ SDE",
            "use_karras_sigmas" : "yes",
            "Schedule type" : "Karras",
            #"batch_count" : 2,
            "batch_size" : batch_size
        }

        response = requests.post(url='http://127.0.0.1:7860/sdapi/v1/txt2img', json=txt2img_request)


        r = response.json()

        #get seeds
        info_str = (r['info'])
        info = json.loads(info_str)
        seeds = (info['all_seeds'])


        # Decode and save the image.

        for i in range(batch_size):
            seed = seeds[i]
            print(seed)
            with open(f"synthetic_images_non_smiling/{seed}.png", 'wb') as f:

                f.write(base64.b64decode(r['images'][i]))

        time.sleep(10)




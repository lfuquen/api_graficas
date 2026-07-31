#!/bin/bash

source /home/lfuquen/cioh_26/api_graficas/gr_env/bin/activate

uvicorn app.main:app --reload
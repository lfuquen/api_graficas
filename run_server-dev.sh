#!/bin/bash

source /home/lfuquen/cioh_26/api_graficas/graficador_env/bin/activate

uvicorn app.main:app --reload
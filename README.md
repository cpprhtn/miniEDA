# miniEDA

## Preparing for Change (Streamlit -> FastAPI / Flask)
Preparing for Change (Streamlit -> FastAPI / Flask)
In order to support big data, large-scale files were processed by supporting parquet in streamlit as a temporary measure, but we are preparing to migrate to FastAPI or Flask because we clearly feel the limitations of streamlit's single thread or session communication.

**If the data is less than 200MB or up to 1GB, it's also pleasant in the Streamlight version. It can be installed and built in the [Streamlight branch](https://github.com/cpprhtn/miniEDA/tree/streamlit)**


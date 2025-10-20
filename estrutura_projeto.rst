Project Structure
====================

The project structure is as follows:

.. code-block:: none

   project/
   ├── api/
   │   ├── __init__.py
   │   ├── main.py
   │   ├── constants/
   │   │   ├── __init__.py
   │   │   └── prompts.py
   │   ├── endpoints/
   │   │   ├── __init__.py
   │   │   ├── base.py
   │   │   ├── files.py
   │   │   ├── chat.py
   │   │   ├── documents.py
   │   │   └── skills.py
   │   ├── log/
   │   │   └── log_file.log
   │   ├── models/
   │   │   ├── __init__.py
   │   │   └── file_info.py
   │   └── services/
   |       ├── container_file_processor/
   |       |   └── file_processor.py
   │       ├── __init__.py
   │       ├── base_service.py
   │       ├── blob_storage_service.py
   │       ├── config.py
   │       ├── embedding_service.py
   │       ├── llm_service.py
   │       ├── temp_file_manager.py
   │       └── user_history_service.py
   ├── streamlit_app/
   │   └── app.py
   ├── requirements.txt
   ├── .env
   └── README.md
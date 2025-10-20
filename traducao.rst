=======================================
Flask to Azure Functions Translation
=======================================

This document presents a detailed analysis of the main distinctions between a project developed using the Flask framework and its corresponding implementation in Azure Functions. Additionally, it addresses the necessary procedures for migration. The transition covers aspects ranging from file organization to variations in environment variable management, service instance handling, and endpoint adaptation.

.. contents:: Index
   :depth: 2
   :local:

Overview
===========

Projects developed with Flask, which adopt the paradigm of creating a centralized application with dynamic attributes, have a file structure and a method for configuring and instantiating objects that differ substantially from those used in Azure Functions. In the latter, the organization is function-oriented, structured in folders containing function.json files, while environment variable management is conducted through the Azure Portal. This documentation aims to highlight the main differences and provide a step-by-step guide for migration.

1. Differences in File Structure
======================================

The main distinction between the two approaches lies in how the framework identifies and organizes endpoints, service instantiation, and environment variable configuration.

Example of structure in Flask:

.. code-block:: text

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

Example of Structure Adapted for Azure Functions:

.. code-block:: text

   .github
   └── workflows
       └── eva_azure_functions_skill_template_ue2dcxs06fazf04(teste-eva-sco).yml
   app
   ├── config
   │   ├── __init__.py
   │   ├── logger.py
   │   └── settings.py
   ├── functions
   │   ├── __init__.py
   │   └── http_trigger_base.py
   ├── services
   │   ├── __init__.py
   │   ├── base_service.py
   │   ├── blob_storage_service.py
   │   ├── embedding_service.py
   │   ├── file_processor.py
   │   ├── llm_service.py
   │   └── user_history_service.py
   ├── skill_prompts
   └── HttpTrigger1
       ├── __init__.py
       └── function.json
   .env

Notes:

- In Azure Functions, the presence of a function.json file (or a dedicated folder, such as HttpTrigger1) is essential for the Azure Portal to correctly recognize the function during the deployment process.
- In the endpoints, the modeling of Flask blueprints is replaced by HTTP functions triggered by triggers, which implies the need to adapt the way responses are returned. For example, the HttpResponse class from the Azure Functions library should be used instead of the jsonify function.
- The services (such as base, blob_storage, embedding, among others) remain virtually unchanged, except for the necessary adjustments in import paths and the centralization of instances.

2. Setting Environment Variables
=====================================

In a Flask project, the configuration and retrieval of environment variables are performed through a .env file, which is loaded using the dotenv library, and the variables are accessed with the ``os.getenv`` function. Below, we present an example extracted from the Flask template:

.. code-block:: python

   from dotenv import load_dotenv
   import os

   # Carrega as variáveis de ambiente
   load_dotenv()

   class Config:
       OPENAI_API_KEY = os.getenv("API_KEY")
       OPENAI_API_ENDPOINT = os.getenv("CUSTOM_ENDPOINT")
       OPENAI_API_VERSION = os.getenv("API_VERSION")
       DIRECTORY_PATH = os.getenv("DIRECTORY_PATH", "./temp_docs")
       OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "default-model")
       TESTE = not bool(os.getenv("TESTE", "0"))
       # Outras variáveis – inclusive as referentes a BLOB e aos modelos de embedding

In the transition to Azure Functions, the configuration of environment variables is done through the Azure Portal. Access to these variables is achieved using the decouple library, as demonstrated in the ``settings.py`` file:

.. code-block:: python

   from decouple import config
   import logging
   from app.services.file_processor import FileProcessor
   # Outras importações

   class Settings:
       # Variáveis para Blob Storage
       BLOB_CONNECTION_STRING = config("BLOB_CONNECTION_STRING", default="")
       BLOB_CONTAINER_NAME = config("BLOB_CONTAINER_NAME", default="")
       BLOB_INDEX_BLOB = config("BLOB_INDEX_BLOB", default="faiss_index.bin")
       BLOB_METADATA_BLOB = config("BLOB_METADATA_BLOB", default="faiss_metadata.pkl")

       # Variáveis para LLM
       OPENAI_API_KEY = config("API_KEY")
       OPENAI_API_ENDPOINT = config("CUSTOM_ENDPOINT")
       OPENAI_API_VERSION = config("API_VERSION")
       OPENAI_MODEL_NAME = config("OPENAI_MODEL_NAME", default="default-model")

       # Variáveis para Embedding
       OPENAI_API_ENDPOINT_EMBEDDING_MODEL = config("CUSTOM_ENDPOINT_EMBEDDING_MODEL")
       OPENAI_API_KEY_EMBEDDING_MODEL = config("API_KEY_EMBEDDING_MODEL")
       OPENAI_API_VERSION_EMBEDDING_MODEL = config("API_VERSION_EMBEDDING_MODEL")
       OPENAI_EMBEDDING_MODEL = config("OPENAI_EMBEDDING_MODEL", default="text-embedding-ada-002")

       TESTE = not bool(config("TESTE", default="0"))
       # Instanciações posteriores são realizadas nesta mesma classe

Main Differences:

- In Flask, ``os.getenv`` is used to access environment variables; in Azure Functions, with the decouple library, access is done through the ``config()`` function.
- In the Azure Functions template, environment variables and service instances are centralized in a single class, eliminating the need to prefix accesses with "config."

3. Instantiation of Main Objects
========================================

In the Flask template, the ``create_app()`` function (located in ``main.py``)  is responsible for instantiating the services and dynamically attaching them to the ``app`` object. Below, we present an example:

.. code-block:: python

   def create_app():
       app = Flask(__name__)
       config = Config()
       app.file_processor = FileProcessor(config.DIRECTORY_PATH)
       app.llm_service = LLMService(
           client=AzureOpenAI(
               api_key=config.OPENAI_API_KEY,
               api_version=config.OPENAI_API_VERSION,
               azure_endpoint=config.OPENAI_API_ENDPOINT
           ),
           model_name=config.OPENAI_MODEL_NAME
       )
       # Demais instâncias e registro de blueprints...
       return app

In the Azure Functions environment, there is no central object, like the ``app`` object in Flask, to which services can be dynamically attached. Instead, all instances are created in the ``Settings`` class, and the services are organized in a dictionary, which facilitates access through the endpoints:

.. code-block:: python

   class Settings:
       # [Get de variáveis de ambiente conforme seção anterior]

       DIRECTORY_PATH = "."
       file_processor = FileProcessor(DIRECTORY_PATH)

       llm_service = LLMService(
           client=AzureOpenAI(
               api_key=OPENAI_API_KEY,
               api_version=OPENAI_API_VERSION,
               azure_endpoint=OPENAI_API_ENDPOINT
           ),
           model_name=OPENAI_MODEL_NAME
       )

       embedder = EmbeddingService(
           client=AzureOpenAI(
               api_key=OPENAI_API_KEY_EMBEDDING_MODEL,
               api_version=OPENAI_API_VERSION_EMBEDDING_MODEL,
               azure_endpoint=OPENAI_API_ENDPOINT_EMBEDDING_MODEL
           ),
           model=OPENAI_EMBEDDING_MODEL
       )

       # Instanciação dos demais serviços, como o BaseService e UserHistoryService,
       # agrupadas em um dicionário para facilitar o acesso nos endpoints:
       if BLOB_CONNECTION_STRING and BLOB_CONTAINER_NAME:
           from app.services.blob_storage_service import BlobStorageService
           blob_storage_service = BlobStorageService(
               BLOB_CONNECTION_STRING,
               BLOB_CONTAINER_NAME,
               TESTE
           )
       else:
           blob_storage_service = None

       base_service = BaseService(
           index_path=BLOB_INDEX_BLOB,
           metadata_path=BLOB_METADATA_BLOB,
           embedder=embedder,
           blob_storage_service=blob_storage_service
       )

       user_history_service = UserHistoryService(blob_storage_service, local_dir=DIRECTORY_PATH)

       services = {
           "file_processor": file_processor,
           "llm_service": llm_service,
           "embedder": embedder,
           "base_service": base_service,
           "user_history_service": user_history_service
       }

   settings = Settings()

Notes:

- There is no "app" object to dynamically attach attributes; for this reason, centralization is done in an object or dictionary.
- Any modification or addition of new services must be reflected in both the ``Settings`` class and the services dictionary.

4. Step-by-Step Translation
==========================

Below is a detailed guide to assist in translating a Flask template to Azure Functions:

Step 1 – Copy the Configuration Class
-----------------------------------------

To perform the requested task, you should copy the section from the ``Config`` file in the  ``config.py`` of the Flask template and then, at the beginning of the ``Settings`` class in the Azure Functions template, replace the calls to ``os.getenv`` with ``config()`` from the decouple library. Additionally, for variable calls that have a default value, the corresponding second parameter should be included. 

Going from this


.. image:: _static/imagem_1_1.png
    :alt: Descrição da imagem
    :width: 400px
    :align: center


for this

.. image:: _static/imagem_2_1.png
    :alt: Descrição da imagem
    :width: 400px
    :align: center


Step 2 – Instantiation of Services
-----------------------------------

In the Flask template, services are dynamically instantiated in the ``main.py`` In the Flask template, services are dynamically instantiated in the ``Settings`` class of the Azure Functions template.


.. image:: _static/imagem_3_1.png
    :alt: Descrição da imagem
    :width: 400px
    :align: center



.. image:: _static/imagem_3_2.png
    :alt: Descrição da imagem
    :width: 400px
    :align: center



During this copying, the following should be done:

- Remove the ``app.`` prefix from each instance, as there is no Flask object for dynamic assignment.
- Ensure that the imports are updated according to the new relative paths, for example, ``from app.services.file_processor import FileProcessor``.

Step 3 – Centralization of Variables
-------------------------------------

Since access to environment variables occurs in the same class where the instances are created, all references within the class should be made without the ``config.`` prefix. Therefore, you should use the variables directly, such as ``OPENAI_API_KEY``, instead of ``config.OPENAI_API_KEY``.

.. image:: _static/imagem_5_1.png
    :alt: Descrição da imagem
    :width: 400px
    :align: center

Step 4 – Adjustment of Endpoints
-----------------------------

When translating endpoints from Flask to Azure Functions, you should make the following adjustments:

- Remove references to ``current_app`` and access services directly through the ``Settings`` dictionary or object.
- Since the HttpTrigger function in Azure Functions does not have an equivalent mechanism to Flask for returning responses, you should convert responses to use the ``HttpResponse`` class from the Azure Functions library.
- Any specific use of Flask, such as blueprints, should be adapted so that each function is invoked by the HTTP trigger with its respective ``function.json`` file.

Step 5 – Updating Services
----------------------------------

Note that the services (such as ``blob_storage_service``, ``llm_service`` , among others) have the same logic, except for the necessary adjustments in imports and file paths. Therefore, it is essential to preserve the content of the services unchanged, making only the necessary modifications to the paths and the centralized instance in the ``settings.py`` file.

Step 6 – Additional Considerations
----------------------------------
- If there is a need to add new functionalities or services, remember to:

- **Update the imports:**  In the new Azure Functions template, ensure that all necessary imports for the new functionalities or services are correctly updated and reflected in the appropriate files.
- **Instantiate the new class:** In the ``settings.py`` file, instantiate the new class and add it to the dictionary (or central object) that facilitates access in the endpoints. This will ensure that the services are available for use in the functions.

Additionally, the identification of functions in the Azure structure depends on the ``function.json`` file present in each function directory (for example, in the HttpTrigger1 folder). Ensure that the bindings are correctly configured for proper deployment. The ``function.json`` file should contain the necessary definitions for the function to be triggered correctly, such as the trigger type, allowed HTTP methods, and any additional parameters.

Conclusion
=========

The translation of a Flask project to the Azure Functions model is not limited to merely changing files and paths; it requires a deep understanding of architectural differences:

- In Flask, there is centralization and dynamic coupling of services to the application object.
- In Azure Functions, each function operates as an autonomous unit, and configuration, including environment variables, is performed through the Azure Portal and centralized configuration classes.

By following the described steps and making the necessary adjustments to the endpoints, service instantiation, and environment variable management, it is possible to migrate the application while keeping most of the service logic unchanged, thus ensuring a smooth transition to the Azure Functions environment.

This document should serve as a guide for translating Flask applications to the serverless environment of Azure Functions, covering the main adaptation points and the practical details necessary for a successful migration.
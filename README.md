# Generate an SQL assignment based on user's context

## Important!
This app is for learning/fun purpose only.
Its use-case is pretty much non-existent, and the data is definitely not the best for the job. But it is easily and freely accessible so... I used it.
As you might see, this app is encountering one of the few problems of RAG technique - the app will only be as good as the context it gets from the vector store, and if the user's query is vogue, the similarity search will fail.

## How to run:
### Step 1
Download and install Ollama, through [Ollama official website](https://ollama.com).

After installation, pull `mistral` and/or `llama2` models with the following terminal command:

`ollama pull mistral`

`ollama pull llama2`

Make sure the ollama local server is up and running using `ollama serve`. The following error means the server is on, and you are ready for the next step: `Error: listen tcp 127.0.0.1:11434: bind: address already in use`.

### Step 2
Clone repository and *cd* into it

```
git clone [repo's url]
cd cs_comps
```

### Step 3
(Not mandatory)

Create a virtual environment, based on python3.10 or above, activate it and install all requirements:

*Mac/Linux:*
```
python -m venv venv
source venv/bin/activate
```

*Windows:*
```
python -m venv venv
cd venv
Scripts/activate
cd ../
```

### Step 4
Install requirements:
`pip install -r requirements.txt`

### Step 5
Run the main app file:

`streamlit run app.py`

The first run can take some long long time, since the app builds the vector-store with local resources. After that, it will always be loaded instead of created.
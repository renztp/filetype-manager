# Setup
1. Install the required packages:
```bash
pip install -r requirements.txt
```

# Usage
1. Create a yaml file on `~/Documents` (change the path in the code if you want it to be somewhere else)
2. Define the following variables in the yaml file:
   - `watch_directory`: The main folder to watch
   - `filetypes`: A list of file types to watch (default: ['.py', '.txt'])

**Sample yaml file:**
```yaml
watch_directory: "~/Downloads"

filetypes:
  jpg: "/home/dev/Pictures"
  png: "/home/dev/Pictures"
  txt: "/home/dev/Documents/new_texts"
  pdf: "/home/dev/Documents/new_pdfs"
```

3. Run the script:
```bash
python3 filewatcher.py
```

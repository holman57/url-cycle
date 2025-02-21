# URL-Cycle

`url-cycle` is a Python utility designed to help users cycle through a list of URLs with flexibility and control. It is especially useful for scenarios where prioritizing certain URLs in the cycling order is critical. This tool allows customization by using a JSON file to manage the URL list and offers options to adjust cycling behavior directly from the command line.

---

## Key Features

- **URL Management:**
  - Cycle through a list of URLs seamlessly.
  - Higher priority can be given to specific URLs as needed.

- **Customizable via JSON:**
  - URL lists can be managed with a JSON file, giving users a simple and structured way to define URLs and their priority levels.

- **Manual Control:**
  - The utility leverages the `wait_key()` function to allow manual intervention during the cycle, providing users the flexibility to pause and resume.

- **Console Output Control:**
  - The `cls()` function ensures the console remains clean by clearing irrelevant or outdated output during each cycle.

- **Command-Line Configuration:**
  - Modify cycling behaviors and preferences using command-line arguments to suit your workflow requirements.

---

## How It Works

1. **Setup the URL List:**
   - Define your list of URLs in a JSON file, specifying any priorities if required.

2. **Run the Script:**
   - Execute the script using Python, providing any necessary command-line arguments to fine-tune the cycling behavior.

3. **Cycle and Control:**
   - URLs will cycle based on the defined rules and priority. Use `wait_key()` for manual control when needed, and enjoy a clutter-free terminal facilitated by the use of `cls()`.

---

## Installation

To use `url-cycle`, ensure you have Python installed on your system. Clone the repository or download the script and ensure dependencies (if any) are installed.

```bash
# Clone the repository
git clone https://github.com/your-username/url-cycle.git

# Navigate to the directory
cd url-cycle

# Install any required dependencies
pip install -r requirements.txt
```

---

## Usage

1. **Prepare the JSON File:**
   - Create a `urls.json` file with your URLs and their optional priority settings. For example:
     ```json
     {
       "urls": [
         {"url": "http://example1.com", "priority": 1},
         {"url": "http://example2.com", "priority": 2}
       ]
     }
     ```

2. **Run the Script:**
   - Execute the script using the following command:
     ```bash
     python url_cycle.py --json-file urls.json --other-options
     ```

3. **Control the Cycling:**
   - Use the keyboard to manually control when to cycle to the next URL if needed.

---

## Command-Line Arguments

- `--json-file`: Path to the JSON file containing the URL list.
- `--priority`: Enable or disable URL priority in the cycle.
- Other options may include setting timeout intervals or specific cycling conditions.

---

## Example JSON Format

An example of how the JSON file could look:
```json
{
  "urls": [
    {"url": "http://example.com", "priority": 1},
    {"url": "http://anotherexample.com", "priority": 2}
  ]
}
```

The priority attribute is optional. By default, URLs have equal cycling weight.

---

## Key Functions

- **`wait_key()`**: Allows users to manually pause and control the cycling through URLs.
- **`cls()`**: Keeps the console output clean for better visibility and less clutter.

---

## Contributions

Contributions to the project are welcome! Feel free to fork the repository, make changes, and submit pull requests. For bugs or feature requests, create an issue in the repository.

---

## License

This project is licensed under the MIT License. For more details, see the LICENSE file.

---

## Acknowledgments

Special thanks to all contributors and open-source resources that helped in shaping this project.

---

### Disclaimer

The `url-cycle` tool is optimized for simplicity and manual control. For advanced or automated URL cycling needs, consider extending the functionality as per your requirements.
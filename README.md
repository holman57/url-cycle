# URL-Cycle

`url-cycle` is a terminal application implemented with Python that is designed to help users cycle through a list of URLs with flexibility and control. It is especially useful for scenarios where prioritizing certain URLs in the cycling order is critical. This tool allows customization by using a JSON file to manage the URL list and offers options to adjust cycling behavior directly from the command line.

---

## Key Features

- **URL Management:**
  - Cycle through a list of URLs seamlessly.
  - Higher priority can be given to specific URLs as needed.

- **Customizable via JSON or YAML:**
  - URL lists can now be managed with either a JSON or YAML file, giving users more flexibility in defining URLs and their priority levels.

- **Manual Control:**
  - The utility leverages the `wait_key()` function to allow manual intervention during the cycle, providing users the flexibility to pause and resume.

- **Console Output Control:**
  - The `cls()` function ensures the console remains clean by clearing irrelevant or outdated output during each cycle.

- **Command-Line Configuration:**
  - Modify cycling behaviors and preferences using command-line arguments, including support for timeout intervals and enhanced cycling rules.

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

To use `url-cycle`, clone the repository or download the script and ensure dependencies are installed.

```bash
# Clone the repository
git clone https://github.com/holman57/url-cycle.git

# Navigate to the directory
cd url-cycle

# Install any required dependencies
pip install -r requirements.txt
```

---

## Usage

1. **Prepare the JSON or YAML File:**
   - Create a `url.json` or `url.yaml` file with your URLs and their optional priority settings. 

2. **Run the Script:**
   - Execute the script using the following command:
     ```bash
     python url_cycle.py --filename url.json --size 86
     ```
     or
     ```bash
     python url_cycle.py --filename url.yaml --size 86
     ```

3. **Control the Cycling:**
   - Use the keyboard to manually control when to cycle to the next URL.

---

## Command-Line Arguments

- `--filename`: Path to the JSON or YAML file containing the URL list.
- `--size`: Increase or Decrease the percentage of urls removed (default: 86 % removed after prioritization removal)

---

## Example JSON Format

An example of how the JSON file could look:
```json
{
  "High Priority": [
    "http://example.com",
    "http://anotherexample.com"
  ],
  "Normal Priority": [
    "http://normalexample.com",
    "http://anothernormalexample.com"
  ],
  "Low Priority": [
    "http://lowpriorityexample.com"
  ],
  "Extra": [
    "http://extraexample.com"
  ]
}
```

---

## Key Functions

- **`wait_key()`**: Allows users to manually pause and control the cycling through URLs.
- **`cls()`**: Keeps the console output clean for better visibility and less clutter.

---

## Contributions
Contributions to the project are welcome! Feel free to fork the repository, make changes, and submit pull requests. Please ensure compatibility with both JSON and YAML input formats. For bugs or feature requests, create an issue in the repository.

---

## License

This project is licensed under the MIT License. For more details, see the LICENSE file.

---

## Acknowledgments

Special thanks to all contributors and open-source resources that helped in shaping this project.

---

The `url-cycle` tool is optimized for simplicity and manual control. For advanced or automated URL cycling needs, consider extending the functionality with batch processing or external API integration.


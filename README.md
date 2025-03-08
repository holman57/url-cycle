# URL-Cycle

`cycle.py` is a terminal application implemented with the Curses module in Python that is designed to help users cycle through a list of URLs with flexibility and control. It is especially useful for scenarios where prioritizing certain URLs in the cycling order is critical. This tool allows customization by using a JSON file to manage the URL list and offers options to adjust cycling behavior directly from the command line.

The application runs in Windows, Mac, Linux terminals

---

## Key Features

- **URL Management:**
  - Cycle through a list of URLs seamlessly.
  - Higher priority can be given to specific URLs as needed.

- **Customizable via JSON or YAML:**
  - URL lists can now be managed with either a JSON or YAML file, giving users more flexibility in defining URLs and their priority levels.

- **Command-Line Configuration:**
  - Modify cycling behaviors and preferences using command-line arguments, including support for timeout intervals and enhanced cycling rules.

---

## How It Works

1. **Setup the URL List:**
   - Define your list of URLs in a JSON file, specifying any priorities if required.

2. **Run the Script:**
   - Execute the script using Python, providing any necessary command-line arguments to fine-tune the cycling behavior.

---

## Installation

To use `cycle`, clone the repository or download the script and ensure dependencies are installed.

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
     python cycle.py --filename url.json --size 86
     ```
     or
     ```bash
     python cycle.py --filename url.yaml --size 86
     ```

3. **Control the Cycling:**
   - Use the keyboard to manually control when to cycle to the next URL.

---

## Command-Line Arguments

- `--filename`: Path to the JSON or YAML file containing the URL list.
- `--size`: Increase or Decrease the percentage of urls removed (default: 93 % removed after prioritization removal)

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
    "http://lowpriorityexample.com",
    "http://www.anotherlowexample.com"
  ],
  "Extra": [
    "http://extraexample.com",
    "http://extraextraexample.com"
  ]
}
```

---

## Contributions
Contributions to the project are welcome! Feel free to fork the repository, make changes, and submit pull requests. Please ensure compatibility with both JSON and YAML input formats. For bugs or feature requests, create an issue in the repository.

---

## License

This project is licensed under the MIT License. For more details, see the LICENSE file.

---

The `cycle` tool is optimized for simplicity and manual control. For advanced or automated URL cycling needs, consider extending the functionality with batch processing or external API integration.


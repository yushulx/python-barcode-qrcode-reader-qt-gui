# Python GUI Barcode Reader
This is a `cross-platform` GUI barcode reader implemented with `Python 3`, `PyQt`, and [Dynamsoft Python Barcode SDK](https://www.dynamsoft.com/barcode-reader/programming/python/). You can use it on `Windows`, `Linux`, `macOS` and `Raspberry Pi OS`.

## Requirements
- OpenCV

    ```
    python3 -m pip install opencv-python
    ```
- Dynamsoft Barcode Reader

    ```
    python3 -m pip install dbr
    ```
- PySide6
    - Windows, Linux and macOS

        ```
        python3 -m pip install PySide6
        ```

## Dynamsoft Barcode SDK License
Apply for a [free trial license](https://www.dynamsoft.com/customer/license/trialLicense) and save it to `license.txt`.

## Usage

- Simple demo:

    ```
    python3 app.py license.txt
    ```

    ![Python Barcode Reader](./screenshots/simple-demo.png)

- Advanced demo:

    ```
    pyside6-uic design.ui -o design.py
    python3 app_advanced.py license.txt
    ```

    ![Python Barcode Reader](./screenshots/advanced-demo.png)

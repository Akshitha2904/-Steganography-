# Secure Data Hiding in Image Using Steganography

This project demonstrates how to hide and extract data (text messages) in images using **Least Significant Bit (LSB)** Steganography. The technique embeds the data into the least significant bits of the pixels of an image, making it difficult to detect without knowledge of the method.

This project provides basic functionality without encryption (for simplicity), meaning the data is hidden in its raw form and can be extracted by anyone who knows how the steganography technique works.

<div align="justify">

## Features:
- **Encode Text into Image**: Hide a secret text message within an image.
- **Decode Text from Image**: Extract the hidden message from the image.
- **No Encryption**: The data is hidden without encryption, making it easy to extract with the right method.

</div>

---

## Requirements

- **Python 3.x**
- **Pillow**: Python Imaging Library (PIL) fork, for image processing.
- **Install required libraries using pip**:
  ```bash
  pip install pillow

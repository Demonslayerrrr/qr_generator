# 🎯 QR Generator

A simple and customizable QR code generator built with Python. This project allows you to generate QR codes with optional styles, colors, and embedded images — all from the command line!

---

## 📁 Project Structure

```
qr_generator/
│
├── src/
│   └── app.py      # Main QR code generator script
```

---

## 🚀 How to Run

1. **Clone the repository:**

```bash
git clone https://github.com/Demonslayerrrr/qr_generator.git
cd qr_generator/src
```

2. **Run the app with Python:**

```bash
python app.py [flags]
```

---

## ⚙️ Available Flags

| Flag            | Description                                         | Example                       |
|-----------------|-----------------------------------------------------|-------------------------------|
| `--color`       | Set the color of the QR code (in hex or name)       | `--color red`                 |
| `--style`       | Choose QR style: `dots` or `squares`                | `--style dots`                |
| `--v`           | Set QR version (1-40) for controlling size/detail   | `--v 5`                       |
| `--image`       | Path to an image to embed in the center of the QR   | `--image logo.png`            |

---

## ✅ Example Usage

```bash
python app.py --color red --style dots --v --image logo.png
```

This will generate a blue QR code with dotted style, verbose, and embed `logo.png` in the center.

---

## 🧠 Features

- Custom QR code colors
- Switch between "dots" or "squares" styling
- Support for version control (QR detail levels)
- Embed images into the center of the QR code
- Simple CLI interface

---

## 📌 TODO / Future Plans

- Add function to generate animated QR codes
- Add function to hash QR
- Option to export
- Web interface with Flask or FastAPI


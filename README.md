## Project Overview

Recent reports have raised concerns about <u>**suspicious**</u> election results from the 2024 Presidential Venezuelan elections, specifically regarding votes attributed to Nicolás Maduro. 

This project aims to provide a **transparent** analysis of the election results by examining "Actas," which are official documents that contain the vote counts for each voting center. Each Acta has a QR code encoding the votes. By decoding these QR codes from scanned images, this project seeks to compile and verify the vote data for accurate analysis.

**Disclaimer**: My Spanish is not the best, so I apologize for any mistakes in translations.

## How It Works

1. **Scanning Actas**: The project processes scanned images of Actas to extract the QR codes.
2. **Decoding QR Codes**: The QR codes are decoded to retrieve the encoded vote counts for each voting center.
3. **Data Compilation**: The decoded vote data is compiled and associated with the corresponding voting centers for further analysis.

## Data
- **Actas**: The scanned images of the Actas can be found in the `images` directory.
- **Decoded Data**: The decoded data from the QR codes can be found in the `outputs/qr_data.json` file.
- **Combined Data**: The combined data from the decoded Data and their linked voting centers can be found in the `outputs/output.jsonl`.
- **BigQuery**: The combined data is also publicly available in a BigQuery dataset [venezuela-2024-elections.elections](https://console.cloud.google.com/bigquery?project=venezuela-2024-elections&ws=!1m4!1m3!3m2!1svenezuela-2024-elections!2selections).

## Challenges

- **Large Dataset**: The project involves processing over +26,000 Actas.
- **Decoding Issues**: Some QR codes cannot be decoded due to scanning artifacts or poor image quality, which may require manual intervention or improved scanning techniques. The Actas that couldn't be decoded are stored in the `track/cant_decode_qr.txt` file.
- **Duplicates**: A small portion of the scanned images sometime contain duplicates, it is important to de-duplicate them using the `acta_id` field. For example:

  - `021223_652434_0481Acta0128.jpg`
  - `021223_551482_0486Acta0129.jpg`
  - `021223_555685_0491Acta0130.jpg`
  
  All of these generate the same data from their QR code:
  ```
  201301006.01.1.0001!140,7,10,8,1,7,1,0,2,3,0,1,8,1,0,1,0,3,1,1,0,1,0,0,0,0,0,0,1,2,0,0,0,5,7,155,1,1!0!0
  ```
  
  in this case `201301006.01.1.0001` is the Acta ID

## Visualize

Using the decoded data hosted on [BigQuery](https://console.cloud.google.com/bigquery?project=venezuela-2024-elections&ws=!1m4!1m3!3m2!1svenezuela-2024-elections!2selections), a public [Looker dashboard](https://lookerstudio.google.com/u/0/reporting/7aa251e8-0f27-4541-b570-9aa03abe42ac/page/tEnnC) is available to visualize the data. The dashboard provides insights into the election results, including the distribution of votes across different voting centers and candidates.

![Map Results](https://i.imgur.com/sv7sMEW.png)
![Stats](https://i.imgur.com/qMhbVPf.png)

## Usage

1. **Setup**: Ensure that all scanned images of the Actas are placed in the designated directory.
2. **Run the Decoder**: Use the provided scripts to decode the QR codes from the images.
3. **Analyze Results**: The decoded data will be compiled into a JSON file, which can be used for analysis of the election results.

## Goals

- Allow Venezuelans to verify the election results by providing a transparent and accessible method to analyze the Actas.
- To provide an accurate and efficient method for extracting vote data from the Venezuelan 2024 election Actas.
- To address and overcome challenges related to QR code decoding in low-quality scanned images.

## Future Work and if you want to contribute

- Improve the decoding process for Actas with scanning artifacts.
- Explore alternative methods to recover data from Actas with unreadable QR codes.
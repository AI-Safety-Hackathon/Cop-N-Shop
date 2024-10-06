
# Cop N' Shop - AI Police Agents as a Service (PAaaS)

Created by:
- Andres Sepulveda Morales (https://www.linkedin.com/in/andres-sepulveda-morales/)
- Diego Sabajo (https://www.linkedin.com/in/diego-sabajo/)
- Elsa Donnat (https://www.linkedin.com/in/elsa-donnat/)
- Paul Vautravers (https://www.linkedin.com/in/paul-vautravers-060051206/)
- Vaishnavi Pamulapati (https://www.linkedin.com/in/vaishnavi-pamulapati/) 

## Overview
Cop N' Shop is a Streamlit-based Python application developed for the Agent Security Hackathon by Apart Research. This project explores the concept of multi-agent marketplaces and their potential future applications. Our demo focuses on a specific use case: identifying suspicious fluctuations in product pricing and other vendor factors to determine the trustworthiness of products and vendors.

For the purposes of this demo, we utilized spoofed product data and prices to allow ease of implementation. In a real world scenario, one might use similar methods to popular coupon extensions for the police agent to analyze and provide insight into.

View our Demo: 
Read more about the project in our paper: 

See more projects from Apart Research: https://www.apartresearch.com/

## Features

- "Real-time" analysis of product pricing trends
- Vendor trustworthiness assessment
- Anomaly detection in pricing and vendor behavior

## Installation
To run this application, you'll need Python 3.12+ installed on your system. Follow these steps in your terminal to set up the project:

1. Clone the repository:
```
git clone https://github.com/AI-Safety-Hackathon/Cop-N-Shop
cd Cop-N-Shop
```

2. (OPTIONAL) Create a virtual environment 
```
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install required packages
```
pip install -r requirements.txt
```

## Usage 

To run the Streamlit application:
```
streamlit run app.py
```

## Contributing
We welcome contributions to the project. Please feel free to submit issues, feature requests, or pull requests.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer
This application is a proof of concept developed for the Agent Security Hackathon. It is not intended for production use without further development and security auditing.
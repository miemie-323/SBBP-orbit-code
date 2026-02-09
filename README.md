# SBBP-orbit-code

# Project Overview
SBBP-orbit-code is a Python program used for satellite orbit prediction. This project provides scripts for satellite orbit calculations and optimizes the orbit model to improve the accuracy of satellite orbit predictions. Using this program, users can predict the satellite's orbital position on a specific date based on TLE data.

# Environment Dependencies
The required dependencies for the project are listed in the `SBBP-requirements.txt` file.

# Directory Structure Description
- `TLE_error_optimize.py`: The main script responsible for satellite orbit optimization calculations.
  
The main script uses files containing specific satellite information. As an example, I use the starlink-4338 satellite's TLE data from November 6, 2024, to predict the satellite's orbit on November 9, 2024. The detailed file descriptions are as follows:
- `4338-qi-1106.txt`: The TLE data for the starlink-4338 satellite on November 6, 2024.
- `4338-1107-stkcompute.xlsx`: The precise position data for the starlink-4338 satellite on November 7, 2024.
- `4338-1108-stkcompute.xlsx`: The precise position data for the starlink-4338 satellite on November 8, 2024.

# Usage Instructions
Run the main script to update the orbit data.

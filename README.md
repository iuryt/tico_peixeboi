# Surfing the Currents: Analyzing Tico's Journey

This repository contains the data analysis and related codes used for the study "Surfing the currents: the longest distance traveled by a rehabilitated and released West Indian manatee (Trichechus manatus)".

[![Watch the video](https://img.youtube.com/vi/SaIj6LsaQ_o/maxresdefault.jpg)](https://youtu.be/SaIj6LsaQ_o)


# Repository Structure

```bash
|-- data/        # Raw and processed data files
|-- src/         # Scripts for data analysis
|-- img/         # Generated figures and plots
```
# Datasets Used
- **Argos Satellite System Data:** <br> Geographic locations of Tico captured remotely.
- **General Bathymetric Chart of the Oceans (GEBCO):** <br> Bathymetry data used for estimating Tico's local depth and identifying the shelf break.
- **NEMO - Global Ocean Physics Analysis and Forecast data:** <br> Surface current data from the NEMO model provided by CMEMS.
- **HYCOM Global Ocean Forecasting System (GOFS) 3.1 Analysis:** <br> Data for surface velocity estimates.
- **OSCAR - Ocean Surface Current Analyses Real-time:** <br> An observational dataset for surface velocity estimates.
- **Soil Moisture Active Passive (SMAP):** <br> Satellite-derived data for sea surface salinity estimates to identify the position of the Amazon River plume.
- **IMERG:** <br> Data from the Integrated Multi-satellitE Retrievals for GPM for rainfall estimates over Tico's trajectory.

# Data Acquisition

Most of the datasets can be accessed and downloaded by running the src/00-download.ipynb script. However, for OSCAR data, you need to run the following command:

```
podaac-data-downloader -c OSCAR_L4_OC_NRT_V2.0 -d ../data/OSCAR_L4_OC_NRT_V2.0 --start-date 2022-07-06T00:00:00Z --end-date 2022-09-05T00:00:00Z
```

The command [podaac-data-downloader](https://github.com/podaac/data-subscriber/blob/main/Downloader.md) is from command-line utility tool that facilitates the streamlined retrieval of oceanographic datasets from the PO.DAAC (Physical Oceanography Distributed Active Archive Center) repository.

In addition to the sources mentioned, we will be archiving all datasets on Zenodo to provide users with an alternative download option.

## Python environment

This project uses version 0.1.0 of the Coringa environment. For more details, visit the GitHub repository: https://github.com/iuryt/env_coringa.

## Issues and Questions

### Reporting Issues
If you encounter any bugs or issues with the code/repository, please [open an issue](https://github.com/iuryt/tico_peixeboi/issues) to report it. When creating an issue, try to provide a detailed description of the problem, steps to reproduce it, and any relevant information that could help in troubleshooting.

### Questions
For general questions, discussions, or getting help on a particular topic, we encourage you to use [GitHub Discussions](https://github.com/iuryt/tico_peixeboi/discussions). This is a great platform to ask questions, share insights, or discuss best practices with the community.

Ask a question: If you're unsure about something, want clarification, or are experiencing general issues that aren't bugs with the repository, just start a new discussion in the Q&A category.

Share ideas: If you have ideas, feedback, or any thoughts that you'd like to share with the community, you're welcome to start a new discussion in the Ideas category.

Remember, when participating in discussions, please be respectful to others.

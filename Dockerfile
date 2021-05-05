FROM python:3.9.5
EXPOSE 8501
RUN pip install streamlit requests pandas
COPY covid19VaccineSlotTracker.py /var/dashboard/covid19VaccineSlotTracker.py
CMD streamlit run /var/dashboard/covid19VaccineSlotTracker.py

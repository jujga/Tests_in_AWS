FROM python
WORKDIR /tests_project/
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENV ENV=dev
CMD python -m pytest -m ui tests/ui_suite --alluredir=test_results/ -s /tests_project --start_from_jenkins=True
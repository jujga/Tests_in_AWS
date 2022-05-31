FROM python
WORKDIR /tests_project/
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENV ENV=dev
CMD python -m pytest -m rest --alluredir=test_results/ -s /tests_project
# Development

1. Clone the repo
  > git clone https://github.com/3d12/rookognition.git
2. Make new changes, commit to feature branch
3. For dev testing, stand up a local development server using Flask
    > flask --app rookognition run --debug
4. Before submitting PR for merge, ensure new changes are tested and have good coverage
  - Testing:
    > pytest
    or (sometimes needed if pytest won't use new db schema)
    > python -m pytest
  - Coverage:
    > coverage run -m pytest
  - To see coverage results, after running:
    > coverage report
  - To get an html report from coverage, after running:
    > coverage html

# PDF comparison tool

## Introduction
A PDF comparison tool, accepts two PDF files, and generates a resulting PDF showcasing the contents of both files, highlighting it in red if it was removed from the first to the second file, or green if it was added from the first to the second file

## **Installation and Execution**

To run, follow these steps:

1. Clone the repository: **`git clone https://github.com/Hharithsa/pdf-comparison.git`**
2. Navigate to the project directory: **`cd pdf-comparision`**
3. Install dependencies: **`python install -r requirements.txt`** or **`make run-setup`** if Make is installed
4. Start the project: **`python -m uvicorn main:app --reload`** or **`make run`** if Make is installed
5. Head to [Swagger UI docs](http://127.0.0.1:8000/docs/), click on the default endpoint -> try it out -> upload the old and new PDF files
6. download the generated PDF from the same panel under the response tab, or follow the error message and change the input files in case of errors. 

## **Assumptions and Limitations**
1. This tool works only for text-related content. It does not detect changes in images and other content
2. The text difference detection logic is not perfect, if there is a difference in spacing or alignment of text between lines, it will count them as different lines even if they have the same content
3. While text order is maintained, the exact vertical and horizontal text layout is not kept in the final PDF, rather, it is to show the text difference between the two PDF's 

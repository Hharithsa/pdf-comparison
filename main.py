from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from io import BytesIO
from compare import getTextFromPDF, compareTexts, generateNewPDF

import fitz # PyMuPDF
import logging

app = FastAPI()

logging.basicConfig(
    level=logging.INFO,  
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  
)
logger = logging.getLogger(__name__)

@app.post("/compare-pdfs/", 
            summary="Compare Two PDFs and Highlight the Differences",
            description="This endpoint takes two PDF files, compares their text content, and generates a PDF highlighting the differences. The generated PDF shows additions in green, deletions in red, and unchanged lines all respect to the old file.",
            response_description="A PDF with highlighted differences between the two input PDFs")
async def compare_pdfs(oldPDF: UploadFile = File(..., description="The first PDF document to compare."),
                        newPDF: UploadFile = File(..., description="The second PDF document to compare.")):
    try:
        logger.info("Request received")

        if oldPDF.content_type != "application/pdf" or newPDF.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Both files must be PDFs")
        
        oldPDFContent = await oldPDF.read()
        newPDFContent = await newPDF.read()

        try:
            oldPDFText = getTextFromPDF(BytesIO(oldPDFContent))
            newPDFText = getTextFromPDF(BytesIO(newPDFContent))
        except fitz.FileDataError:
            logger.error("Error reading one the file")
            raise HTTPException(status_code=400, detail="Error reading the PDF file")

        if not oldPDFText or not newPDFText:
            logger.error("Text extraction from PDF failed")
            raise HTTPException(status_code=400, detail="Text extraction from PDF failed")

        oldText = "\n".join(oldPDFText)
        newText = "\n".join(newPDFText)

        diff = compareTexts(oldText, newText)

        if not diff:
            logger.warning("No differences found between the documents")
            raise HTTPException(status_code=400, detail="No differences found between the documents")

        diff_pdf = generateNewPDF(diff)

        logger.info("Returning generated PDF")
        return StreamingResponse(diff_pdf, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=highlighted_diff.pdf"})

    except Exception as e:
        logger.error(f"Internal server error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

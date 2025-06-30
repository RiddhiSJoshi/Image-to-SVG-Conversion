#  Image to SVG Converter using StarVector (FastAPI + GraphQL + HTML/JS)

This project is a full-stack web application that allows users to upload raster images (JPG/PNG), converts them into SVG vector graphics using the **[StarVector](https://huggingface.co/starvector/starvector-8b-im2svg)** model, and returns the result through a **GraphQL API**. The application is built with:

-  **StarVector AI Model** (via Hugging Face Transformers)
-  **FastAPI** as the backend framework
- **Strawberry GraphQL** for API handling
-  **HTML, CSS, JavaScript** frontend for user interaction

---

## Features

- Upload images via web interface
- Convert them into SVG using an AI model
- GraphQL mutation to process image
- SVG gallery to view/download converted results
- Secure file upload with image validation
- Optional caching and disk-saving of results

---

## Dependencies
- fastapi
- strawberry-graphql
- uvicorn
- Pillow
- transformers
- torch
- python-multipart (for file uploads)

 ## Future Improvements
- Add user authentication
- Enable batch conversion
- Host on cloud (e.g., Render, Vercel, AWS)
- Add model progress feedback on frontend

   ## Author
Developed by Riddhi S Joshi
AI-Powered Web Application for SVG Generation

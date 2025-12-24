from fastapi import APIRouter, UploadFile, File
from fastapi.responses import HTMLResponse
from app.parser import extract_pages
from app.ai import process_page

router = APIRouter()

#homepage is here
@router.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
    <head>
        <title>PictureBook</title>
        <style>
            html, body {
                margin: 0;
                padding: 0;
                height: 100%;
                font-family: Georgia, serif;
                background: #1e1e1e;
                color: #f0f0f0;
            }

            .container {
                height: 100%;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .card {
                background: #262626;
                padding: 50px 60px;
                border-radius: 12px;
                text-align: center;
                box-shadow: 0 20px 40px rgba(0,0,0,0.6);
                border: 1px solid #333;
            }

            h1 {
                margin-top: 0;
                font-size: 36px;
            }

            .subtitle {
                font-size: 16px;
                color: #bdbdbd;
                margin-bottom: 30px;
            }

            /* Custom file picker */
            .file-label {
                display: inline-block;
                padding: 12px 30px;
                margin-bottom: 12px;
                background: #1e1e1e;
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 8px;
                cursor: pointer;
            }

            .file-label:hover {
                background: #2e2e2e;
            }

            .file-name {
                font-size: 14px;
                color: #bdbdbd;
                margin-bottom: 25px;
            }

            button {
                padding: 14px 36px;
                font-size: 16px;
                font-family: Georgia, serif;
                cursor: pointer;
                background: #1e1e1e;
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 8px;
            }

            button:hover {
                background: #2e2e2e;
            }
        </style>
    </head>

    <body>
        <div class="container">
            <div class="card">
                <h1>🐉 Picture Book 🐉</h1>
                <div class="subtitle">
                    Upload a PDF and read it as an illustrated picture book
                </div>

                <form action="/process-book/" method="post" enctype="multipart/form-data">
                    <input type="file" id="fileInput" name="file" accept=".pdf" hidden required>
                    <label for="fileInput" class="file-label">Choose PDF</label>
                    <div id="fileName" class="file-name">No file selected</div>

                    <button type="submit">Create Picture Book</button>
                </form>
            </div>
        </div>

        <script>
            const fileInput = document.getElementById('fileInput');
            const fileName = document.getElementById('fileName');

            fileInput.addEventListener('change', () => {
                fileName.textContent = fileInput.files.length
                    ? fileInput.files[0].name
                    : 'No file selected';
            });
        </script>
    </body>
    </html>
    """

#reader page here
@router.post("/process-book/", response_class=HTMLResponse)
async def process_book(file: UploadFile = File(...)):
    pages = extract_pages(file)
    results = []

    for i, page_text in enumerate(pages):
        results.append(await process_page(page_text, i))

    html = f"""
    <html>
    <head>
        <title>PictureBook</title>
        <style>
            html, body {{
                margin: 0;
                padding: 0;
                height: 100%;
                font-family: Georgia, serif;
                background: #1e1e1e;
                color: #f0f0f0;
            }}

            h1 {{
                text-align: center;
                margin: 10px 0;
            }}

            .page {{
                display: none;
                height: calc(100vh - 120px);
            }}

            .spread {{
                display: flex;
                width: 100%;
                height: 100%;
            }}

            .text {{
                width: 50%;
                padding: 30px 40px;
                overflow-y: auto;
                font-size: 20px;
                line-height: 1.9;
                text-align: justify;
                box-sizing: border-box;
            }}

            .image {{
                width: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                background: #262626;
            }}

            .image img {{
                width: 100%;
                height: 100%;
                object-fit: contain;
            }}

            .nav {{
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100%;
                height: 60px;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 20px;
                background: #111;
                border-top: 1px solid #333;
            }}

            button {{
                padding: 10px 28px;
                font-size: 16px;
                cursor: pointer;
                background: #1e1e1e;
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 6px;
            }}

            button:hover {{
                background: #2e2e2e;
            }}
        </style>
    </head>

    <body>
        <h1>🐉 Picture Book 🐉</h1>
    """

    # Pages
    for idx, item in enumerate(results):
        if item.get("image"):
            html += f"""
            <div class="page" id="page-{idx}">
                <div class="spread">
                    <div class="text">
                        <h2>Page {item['page']}</h2>
                        {item['full_text'].replace('\\n', '<br>')}
                    </div>
                    <div class="image">
                        <img src="/{item['image']}">
                    </div>
                </div>
            </div>
            """

    # Navigationjs
    html += f"""
        <div class="nav">
            <button onclick="prevPage()">⬅ Previous</button>
            <span id="page-indicator"></span>
            <button onclick="nextPage()">Next ➡</button>
        </div>

        <script>
            let currentPage = 0;
            const totalPages = {len(results)};

            function showPage(i) {{
                document.querySelectorAll('.page').forEach(p => p.style.display = 'none');
                const page = document.getElementById('page-' + i);
                if (page) {{
                    page.style.display = 'block';
                    document.getElementById('page-indicator').innerText =
                        `Page ${{i + 1}} of ${{totalPages}}`;
                }}
            }}

            function nextPage() {{
                if (currentPage < totalPages - 1) {{
                    currentPage++;
                    showPage(currentPage);
                }}
            }}

            function prevPage() {{
                if (currentPage > 0) {{
                    currentPage--;
                    showPage(currentPage);
                }}
            }}

            showPage(0);
        </script>
    </body>
    </html>
    """

    return HTMLResponse(content=html)
